#include "knn.h"

typedef struct {
    double distance;      // distance of this Image with the testing Image
    int label;            // the label for this image (from 0-9)
} Distance_info;

const int MAX_FILENAME_LENGTH = 260;
Image *load_image(char *pgm_filename, Image *i);
/**
 * This function takes in the name of the text file containing the image names
 * This function should NOT assume anything about the image resolutions,
 * and may be tested with images of different sizes. You will need to allocate
 * your own data for the struct, and also for the images / labels.
 */
Dataset *load_dataset(const char *filename) {

  FILE *file_stream = fopen(filename, "r");
  if (file_stream == NULL) {
    perror("Failed to open training name list: ");
    return NULL;
  }
  char pgm_filename[MAX_FILENAME_LENGTH];

  Dataset *ds = malloc(sizeof(Dataset));
  ds->num_items = 0;

  // read the file containing all filename. Loop through the list_file twice,
  // first time gets the total number of images, second time use the 
  // total number of images to malloc, so to load the image and label array
  while(fgets(pgm_filename, MAX_FILENAME_LENGTH, file_stream) != NULL) {
    (ds->num_items)++;
  } 

  // rewind the file and start second loop
  rewind(file_stream);

  // now that we know the num_items, malloc accordingly
  ds->images = malloc(sizeof(Image) * (ds->num_items));
  ds->labels = malloc(sizeof(unsigned char) * (ds->num_items));
  int cur_index = 0;
  while(fgets(pgm_filename, MAX_FILENAME_LENGTH, file_stream) != NULL) {
    // remove new line char from pgm_filename!!!
    pgm_filename[strcspn(pgm_filename, "\n")] = 0;

    // find image from name, populate Image 
    // struct, and load the image into dataset
    load_image(pgm_filename, &((ds->images)[cur_index]));

    // find the correct label, which is right befor the dot
    char * dot = strchr(pgm_filename, '.');
    // set label of image for cur ind, 
    //label can be found at the position right before dot - pgm_filename
    int label_ind = ((int)(dot - pgm_filename)) - 1;
    // convert to int since unsign char is int
    (ds->labels)[cur_index] = (pgm_filename[label_ind]) - '0';
    
    cur_index++;
  }

  fclose(file_stream);
  return ds;
}

Image *load_image(char *pgm_filename, Image *i) {

  FILE *pgm_file_stream = fopen(pgm_filename, "r");

  fscanf(pgm_file_stream, "%*s %d %d %*d", &(i->sx), &(i->sy));

  // now scan image body
  // unsigned char * is int * from 0-255
  (i->data) = malloc(sizeof(unsigned char) * ((i->sx) * (i->sy)));
  
  // populate datas into image
  int cur_ind = 0;
  while(fscanf(pgm_file_stream, "%hhd", &((i->data)[cur_ind])) != EOF) {
    cur_ind++;
  }
  
  fclose(pgm_file_stream);
  return i;
}

/****************************************************************************/
/* For all the remaining functions you may assume all the images are of the */
/*     same size, you do not need to perform checks to ensure this.         */
/****************************************************************************/

/** 
 * Return the euclidean distance between the image pixels (as vectors).
 */
double distance(Image *a, Image *b) {
  int length = ((int)(a->sx)) * ((int)(a->sy));
  double buffer = 0;
  double result = 0;

  for(int ind = 0; ind < length; ind++) {
    // (int)((b->data)[ind]) is data for b at index ind
    buffer += pow(((int)((b->data)[ind])) - ((int)((a->data)[ind])), 2);
  }
  result = sqrt(buffer);

  return result; 
}

int most_occurred_labels(Distance_info *di, int di_length) {

  // each index represent label 0-9, the element represent occurrence
  int occurrence[10] = {0,0,0,0,0,0,0,0,0,0};

  // calculate the occurrences for all labels
  for (int ind = 0; ind < di_length; ind++) {
    (occurrence[(di[ind]).label])++;
  }

  // find the index with the most occurrence
  int max_occurrence = occurrence[0];
  int correct_label = 0;
  for (int ind = 1; ind < 10; ind++) {
    if (occurrence[ind] > max_occurrence) {
      max_occurrence = occurrence[ind];
      correct_label = ind;
    }
  }

  return correct_label;
}

/**
 * Given the input training dataset, an image to classify and K,
 *   (1) Find the K most similar images to `input` in the dataset
 *   (2) Return the most frequent label of these K images
 * 
 * Note: If there's multiple images with the same smallest values, pick the
 *      ones that come first. For automarking we will make sure the K smallest
 *      ones are unique, so it doesn't really matter.
 */ 
int knn_predict(Dataset *data, Image *input, int K) {
  // array for storing nearest k image distance info
  // don't need malloc here bc we don't need it after function exits
  Distance_info di_array[K];
  int di_array_ind = 0;

  for(int image_ind = 0; image_ind < (int)(data->num_items); image_ind++) {
    // calculate distance between a training image and input image
    double d = distance(&((data->images)[image_ind]), input);


    // populate di_array if not full, and sort from biggest to smallest
    if (di_array_ind < K) {
      di_array[di_array_ind].distance = d;
      di_array[di_array_ind].label = ((data->labels)[image_ind]);
      di_array_ind++;
    } else {
      // If di_array's full, check if current distance can replace 
      //any of the elements in it(if it's smaller than any element)
      int ind_to_replace = 0;
      // true is 1, false is 0
      int d_can_replace = 0;
      for(int ind = 0; ind < K; ind++) {
        // if current d is smaller than one of the element
        if ((di_array[ind].distance > d) && d_can_replace == 0) {
          ind_to_replace = ind;
          d_can_replace = 1;
        } else if ((di_array[ind].distance > 
              di_array[ind_to_replace].distance) && d_can_replace == 1) {
            ind_to_replace = ind;
        } 
      }
      // replace d with the appropriate element if possible
      if (d_can_replace == 1) {
        di_array[ind_to_replace].distance = d;
        di_array[ind_to_replace].label = ((data->labels)[image_ind]);
      }
    }
  }
  // find correct label
  int result_label = most_occurred_labels(di_array, K);

  return result_label;
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
