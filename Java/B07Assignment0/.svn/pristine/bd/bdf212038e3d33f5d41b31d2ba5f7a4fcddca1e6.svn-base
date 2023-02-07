package a0;

//**********************************************************

//Assignment0:
//UTOR user_name: liuhai6
//UT Student #: 1004258000
//Author: Hai Ning Liu
//
//
//Honor Code: I pledge that this program represents my own
//program code and that I have coded on my own. I received
//help from no one in designing and debugging my program.
//I have also read the plagarism section in the course info
//sheet of CSC B07 and understand the consequences. Note that 
//we will be running all your quizzes and assignments for plagarism 
//check starting sometime in November of 2020. If you do not complete this
//honor code, we will give you no credit and award you 0% for this component. 

/*
 * 
 */
public class Rearranging {

	public static void rearranging(int[] items) {
		// set up left and right ind and iterate inward
		int leftInd = 0;
		int rightInd = items.length - 1;

		for (int curInd = 0; curInd <= rightInd; curInd++) {
			int curNum = items[curInd];

			if (curNum > 0) {
				swap(curInd, rightInd, items);
				rightInd--;

				// curInd stays because hasn't check swapped number yet
				curInd--;
			} else if (curNum < 0) {
				swap(curInd, leftInd, items);
				leftInd++;

			}
		}
	}

	private static void swap(int i, int j, int[] items) {
		// store items[i] to a free variable to use later
		int temp = items[i];
		items[i] = items[j];
		items[j] = temp;
	}

	public static void main(String[] args) {
		/*
		 * You can modify the main function in any way you like. We will 
		 * not mark your main function.
		 */
		int[] items = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 0 }; 
		/*
		 * printing the values in the items before 
		 * calling the method rearranging
		 */
		for (int item : items) {
			System.out.println(item);
		}
		System.out.println();

		// calling the rearranging method
		Rearranging.rearranging(items);
		/*
		 * printing the values in the items after 
		 * calling the method rearranging
		 */
		for (int item : items) {
			System.out.println(item);
		}
	}
}
