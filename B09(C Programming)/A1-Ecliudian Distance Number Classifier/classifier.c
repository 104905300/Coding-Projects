#include "knn.h"

/**
 * Compilation command
 *    gcc -Wall -std=c99 -lm -o classifier classifier.c knn.c
 *
 * Decompress dataset into individual images:
 *    tar xvzf datasets.tgz
 *
 * Running quick test with 1k training and 1k testing images, K = 1:
 *    ./classifier 1 lists/training_1k.txt lists/testing_1k.txt
 *
 * Running full evaulation with all images, K = 7: (Will take a while)
 *    ./classifier 7 lists/training_full.txt lists/testing_full.txt
 */

/*****************************************************************************/
/* Do not add anything outside the main function here. Any core logic other  */
/* than what is described below should go into `knn.c`. You've been warned!  */
/*****************************************************************************/

/**
 * main() takes in 3 command line arguments:
 *    - K : The K value for K nearest neighbours 
 *    - training_list: Name of a text file with paths to the training images
 *    - testing_list:  Name of a text file with paths to the testing images
 *
 * You need to do the following:
 *    - Parse the command line arguments, call `load_dataset()` appropriately.
 *    - For each test image, call `knn_predict()` and compare with real label
 *    - Print out (only) one integer to stdout representing the number of 
 *        test images that were correctly predicted.
 *    - Free all the data allocated and exit.
 */

int main(int argc, char *argv[]) {
  
  if (argc != 4){
    perror("Invalid argument count");
    return 1;
  }

  // argv[1] is k
  int k = (int)strtol(argv[1], NULL, 10);
  if(k == 0) {
    perror("Invalid k value");
    return 1;
  }

  // argv[2] is the training name list 
  Dataset *training_ds = load_dataset(argv[2]);
  if (training_ds == NULL ) {
    perror("Failed to open training name list ");
    return 1;
  }
  
  // argv[3] is the testing name list 
  Dataset *testing_ds = load_dataset(argv[3]);
  if (testing_ds == NULL) {
    perror("Failed to open testing name list ");
    return 1;
  }

  int predicted_label = 0;
  int real_label = 0;
  int total_correct = 0;
  for(int ind = 0; ind < testing_ds->num_items; ind++) {

    // get predicted label
    Image *testing_image = &((testing_ds->images)[ind]);
    predicted_label = knn_predict(training_ds, testing_image, k);

    // get real label
    real_label = (testing_ds->labels)[ind];

    if (real_label == predicted_label) {
      total_correct++;
    }
  }

  // Print out answer
  printf("%d\n", total_correct);
  
  free_dataset(training_ds);
  free_dataset(testing_ds);
  return 0;
}