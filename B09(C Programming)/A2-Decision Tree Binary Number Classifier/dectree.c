#include "dectree.h"

/**
 * This function takes in the name of the binary file containing the data and
 * loads it into memory. The binary file format consists of the following:
 *
 *     -   4 bytes : `N`: Number of images / labels in the file
 *     -   1 byte  : Image 1 label
 *     - 784 bytes : Image 1 data (28x28)
 *          ...
 *     -   1 byte  : Image N label
 *     - 784 bytes : Image N data (28x28)
 *
 * You can simply set the `sx` and `sy` values for all the images to 28, we
 * will not test this with different image sizes.
 */
Dataset *load_dataset(const char *filename) {
  
  FILE *file_stream = fopen(filename, "rb");
  if (file_stream == NULL) {
    perror("Failed to open file: ");
    return NULL;
  }

  Dataset *ds = malloc(sizeof(Dataset));
  ds->num_items = 0;

  // first 4 bytes(size of int) represent the number of images in the file
  if (fread(&(ds->num_items), sizeof(int), 1, file_stream) != 1) {
    perror("Failed to read file: ");
    return NULL;
  }
  
  ds->images = malloc(sizeof(Image) * (ds->num_items));
  ds->labels = malloc(sizeof(unsigned char) * (ds->num_items));

  // read a image label (if read correctly will return 1, 
  // else it's end of file or there was an error)
  for(int img_ind = 0; img_ind < ds->num_items; img_ind++) {
    if(fread(&((ds->labels)[img_ind]),
        sizeof(unsigned char), 1, file_stream) != 1) {
      perror("Failed to read file: ");
      return NULL;
    }

    // size of image is always 28*28 which is 784
    ((ds->images)[img_ind]).sx = 28;
    ((ds->images)[img_ind]).sy = 28;
    ((ds->images)[img_ind]).data = malloc(sizeof(unsigned char) * 784);
    // store data into image
    if(fread(((ds->images)[img_ind]).data,
        sizeof(unsigned char), 784, file_stream) != 784){
      perror("Failed to read file: ");
      return NULL;
    }
  }

  if(fclose(file_stream) != 0) {
    // error closing
    perror("Failed to close file: ");
  }

  return ds;
}

/**
 * This function computes and returns the Gini impurity of the M images
 * (with their indices stored in the array) if they were to be split
 * based on the given pixel.
 * 
 * DO NOT CHANGE THIS FUNCTION; It is already implemented for you.
 */
double split_gini_impurity(Dataset *data, int M, int indices[M], int pixel) {
  int a_freq[10] = {0}, a_count = 0;
  int b_freq[10] = {0}, b_count = 0;
  for (int i = 0; i < M; i++) {
    int img_idx = indices[i];
    // The pixels are always either 0 or 255, but using < 128 for generality.
    if (data->images[img_idx].data[pixel] < 128)
      a_freq[data->labels[img_idx]]++, a_count++;
    else
      b_freq[data->labels[img_idx]]++, b_count++;
  }

  double a_gini = 0, b_gini = 0;
  for (int i = 0; i < 10; i++) {
    double a_i = ((double)a_freq[i]) / ((double)a_count);
    double b_i = ((double)b_freq[i]) / ((double)b_count);
    if (a_count) a_gini += a_i * (1 - a_i);       // This was changed
    if (b_count) b_gini += b_i * (1 - b_i);       // This was changed
  }
  // Weighted average of gini impurity of children
  return (a_gini * a_count + b_gini * b_count) / M;
}

/**
 * Given a subset of M images and their corresponding indices, find and return
 * the most frequent label and it's frequency. The last 2 parameters are
 * only for outputs.
 *
 * - The most frequent label should be stored in `*label`
 * - The frequency of this label should be stored in `*freq`
 * 
 * If multiple labels have the same maximal frequency, return the smallest one.
 */
void get_most_frequent(Dataset *data, int M, int indices[M], 
                       int *label, int *freq) {
  int occurrence[10] = {0,0,0,0,0,0,0,0,0,0};
  int current_label;

  // populate the number of occurences for each label(0-10)
  for (int ind = 0; ind < M; ind++) {
    current_label = (data->labels)[indices[ind]];
    (occurrence[current_label])++;
  }
   // find most frequent label and its frequency
  int max_occurrence = occurrence[0];
  int correct_label = 0;
  for (int ind = 1; ind < 10; ind++) {
    if (occurrence[ind] > max_occurrence) {
      max_occurrence = occurrence[ind];
      correct_label = ind;
    }
  }

  *label = correct_label;
  *freq = max_occurrence;
  return;
}

/**
 * Given a subset of M images and their corresponding indices, find and return
 * the best pixel to split the data based on. The best pixel is the one which
 * has the minimum Gini impurity as computed by `split_gini_impurity()`.
 * 
 * The return value should be a number between 0-783 (inclusive), representing
 *  the pixel the M images should be split based on.
 * 
 * If multiple pixels have the same minimal Gini impurity, return the smallest.
 */
int find_best_split(Dataset *data, int M, int indices[M]) {

  int total_pixels = 784;
  // get a starting value to compare with
  double cur_minimum_gini = split_gini_impurity(data, M, indices, 0);
  double cur_gini;
  int result_pixel = 0;

  for (int pixel = 1; pixel < total_pixels; pixel++) {
    cur_gini = split_gini_impurity(data, M, indices, pixel);
    // if there is a smaller gini, 
    //update current smallest gini and result pixel
    if (cur_gini < cur_minimum_gini) {
      cur_minimum_gini = cur_gini;
      result_pixel = pixel;
    }
  }
  return result_pixel;
}

/**
 * This is the recursive function that creates the Decision tree. In each
 * recursive call, we only want to consider some subset of the entire dataset
 * corresponding to the node. To represent this, we pass in an array of indices
 * of these images in the dataset, along with it's length M. Be careful to
 * allocate this on the array for any recursive calls made, and free it when
 * you're done with creating the tree. Here, you need to:
 *
 *    - Compute ratio of most frequent image in current call, terminate if >95%
 *    - Find the best pixel to split on using `split_gini_impurity()`
 *    - Split the data, allocate corresponding arrays, and recurse
 *    - In either case, allocate a new node, set the correct values and return
 *       - If it's a child, set `classification`, and both children = NULL.
 *       - If it's not a child, set `pixel` and `left`/`right` (recursively). 
 */
DTNode *make_helper(Dataset *data, int M, int indices[M]) {
  int label = 0;
  int frequency = 0;
  get_most_frequent(data, M, indices, &label, &frequency);
  double percentage = ((double)frequency)/M;

  DTNode *cur_Node = malloc(sizeof(DTNode));

  // if more than 95% of labels are the same, then it's a leaf node.
  // else, find best split and recurse
  if (percentage > 0.95) {
    // free indices current indices to create more space
    free(indices);
    cur_Node->pixel = -1;
    cur_Node->classification = label;
    cur_Node->left = NULL;
    cur_Node->right = NULL;
    return cur_Node;
    
  } else {
    cur_Node->pixel = find_best_split(data, M, indices);
    cur_Node->classification = -1;
    // create two indices for images that match the 
    // chosen pixel and images that didn't. 
    // The length of these two array is unknown, but we know is less than M
    int *matched_indices = malloc(sizeof(int) * M);
    int *no_matched_indices = malloc(sizeof(int) * M);
    int matched_counter = 0;
    int no_matched_counter = 0;
    for (int ind = 0; ind<M; ind++) {
      int image_ind = indices[ind];
      // check if the value of the chosen pixel for a specific image 
      // is 255 or not (dark or not),if it is, store the image index 
      //in the matched_indices, if not, store it in no_matched_indices
      if (((data->images)[image_ind]).data[cur_Node->pixel] > 128) {
        matched_indices[matched_counter] = image_ind;
        matched_counter++;
      } else {
        no_matched_indices[no_matched_counter] = image_ind;
        no_matched_counter++;
      }
    }
    // free indices current indices to create more space
    free(indices);

    // "right" is the images that matched the chosen pixel(value of pixel: 255)
    // otherwise put it in "left"

    cur_Node->right = make_helper(data, matched_counter, matched_indices);

    cur_Node->left = make_helper(
      data, no_matched_counter, no_matched_indices);
  }

  return cur_Node;
}

/**
 * This is the function exposed to the user. All you should do here is set
 * up the `indices` array correctly for the entire dataset and call 
 * `make_helper()` with the correct parameters.
 */
DTNode *make_dec_tree(Dataset *data) {

  // starting indices is all the images
  int *indices = malloc(sizeof(int) * data->num_items);
  for (int ind = 0; ind < data->num_items; ind++) {
    indices[ind] = ind;
  }

  DTNode *starting_node = make_helper(data, data->num_items, indices);

  return starting_node;
}

/**
 * Given a decision tree and an image to classify, return the predicted label.
 */
int dec_tree_classify(DTNode *root, Image *img) {
  
  DTNode *cur_node_addr = root;

  while ((cur_node_addr->classification) == -1) { // not leaf node
    
    // if the target pixel is "on"(255), go to right child
    // else go to left child 
    if (img->data[cur_node_addr->pixel] > 128) {
      cur_node_addr = cur_node_addr->right;
    } else {
      cur_node_addr = cur_node_addr->left;
    }
  }
  // if exit while loop, mean a leaf node is reached, return its label
  return cur_node_addr->classification;
}

/**
 * This function frees the Decision tree.
 */
void free_dec_tree(DTNode *node) {
  
  // if node is empty it means image file is empty then code won't reach here
  
  // leaf node
  if (node->classification != -1) {
     free(node);
     return;
  } else {
    free_dec_tree(node->left);
    free_dec_tree(node->right);
  }
  free(node);
  return;
}

/**
 * Free all the allocated memory for the dataset
 */
void free_dataset(Dataset *data) {
  for (int i = 0; i < data->num_items; i++) {
    free(data->images[i].data);
  }
  free(data->images);
  free(data->labels);
  free(data);
}