#include "dectree.h"

// Makefile included in starter:
//    To compile:               make
//    To decompress dataset:    make datasets
//
// Or, to compile manually, use:
//    gcc -o classifier dectree.c classifier.c -g -Wall -std=c99 -lm
//
// Running decision tree generation / validation:
//    ./classifier datasets/training_data.bin datasets/testing_data.bin

/*****************************************************************************/
/* Do not add anything outside the main function here. Any core logic other  */
/* than what is described below should go in `dectree.c`. You've been warned!*/
/*****************************************************************************/

/**
 * main() takes in 2 command line arguments:
 *    - training_data: A binary file containing training image / label data
 *    - testing_data: A binary file containing testing image / label data
 *
 * You need to do the following:
 *    - Parse the command line arguments, call `load_dataset()` appropriately.
 *    - Call `make_dec_tree()` to build the decision tree with training data
 *    - For each test image, call `dec_tree_classify()` and compare the real 
 *        label with the predicted label
 *    - Print out (only) one integer to stdout representing the number of 
 *        test images that were correctly classified.
 *    - Free all the data allocated and exit.
 * 
 *  (You should for the most part be able to re-use code from A1 for this)
 */
int main(int argc, char *argv[]) {
  if (argc != 3){
    perror("Invalid argument count");
    return -1;
  }

  Dataset* training_ds = load_dataset(argv[1]);
  if (training_ds == NULL) {
    return -1;
  }
  Dataset* testing_ds = load_dataset(argv[2]);
  if (testing_ds == NULL) {
    return -1;
  }

  int total_correct = 0;

  if(training_ds->num_items == 0 || testing_ds->num_items == 0) {
    printf("%d\n", total_correct);
    return 0;
  }

  DTNode *root_node = make_dec_tree(training_ds);

  int predicted_label;
  int real_label;
  // do decision tree calculation on each testing image
  for (int ind = 0; ind < (testing_ds->num_items); ind++) {
    predicted_label = dec_tree_classify(
      root_node, &((testing_ds->images)[ind]));
    
    real_label = (testing_ds->labels)[ind];

    if (predicted_label == real_label) {
      total_correct++;
    }
  }
  // Print out answer
  printf("%d\n", total_correct);

  free_dec_tree(root_node);
  free_dataset(training_ds);
  free_dataset(testing_ds);

  return 0;
}