package a0;
// **********************************************************

// Assignment0:
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

public class Cfiltering {
	// this is a 2d matrix i.e. user*movie
	private int userMovieMatrix[][];
	// this is a 2d matrix i.e. user*movie
	private float userUserMatrix[][];

	/**
	 * Default Constructor.
	 */
	public Cfiltering() {
		// this is 2d matrix of size 1*1
		userMovieMatrix = new int[1][1];
		// this is 2d matrix of size 1*1
		userUserMatrix = new float[1][1];
	}

	/**
	 * Constructs an object which contains two 2d matrices, one of size 
	 * users*movies which will store integer movie ratings and one of size 
	 * users*users which will store float similarity scores between
	 *  pairs of users.
	 * 
	 * @param numberOfUsers  Determines size of matrix variables.
	 * @param numberOfMovies Determines size of matrix variables.
	 */
	public Cfiltering(int numberOfUsers, int numberOfMovies) {
		userMovieMatrix = new int[numberOfUsers][numberOfMovies];
		userUserMatrix = new float[numberOfUsers][numberOfUsers];
	}

	/**
	 * The purpose of this method is to populate the UserMovieMatrix. As input
	 * parameters it takes in a rowNumber, columnNumber and a rating value. The
	 * rating value is then inserted in the UserMovieMatrix at the specified
	 * rowNumber and the columnNumber.
	 * 
	 * @param rowNumber    The row number of the userMovieMatrix.
	 * @param columnNumber The column number of the userMovieMatrix.
	 * @param ratingValue  The ratingValue to be inserted 
	 * in the userMovieMatrix
	 */
	public void populateUserMovieMatrix(
			int rowNumber, int columnNumber, int ratingValue) {

		userMovieMatrix[rowNumber][columnNumber] = ratingValue;
	}

	public void populateUserUserMatrix(
			int rowNumber, int columnNumber, float similarity_score) {

		userUserMatrix[rowNumber][columnNumber] = similarity_score;
	}

	/**
	 * this is where userUserMatrix is made
	 */
	public void calculateSimilarityScoreForAllPairsOfUser() {
		float curScore = 0;
		int row = 0;
		int col = 0;
		// each user will loop through the userMovieMatrix
		for (int[] userA : userMovieMatrix) {
			for (int[] userB : userMovieMatrix) {
				// calculate score then put the score in the matrix
				curScore = calculateSimilarityScore(userA, userB);
				populateUserUserMatrix(row, col, curScore);
				col++;
			}
			col = 0;
			row++;
		}

	}

	/**
	 * Determines how similar each pair of users is based on their ratings. 
	 * This similarity value is represented with with a float value between 
	 * 0 and 1, where 1 is perfect/identical similarity. Stores these values 
	 * in the userUserMatrix.
	 * 
	 * @param COMPLETE THIS IF NEEDED
	 * @param COMPLETE THIS IF NEEDED
	 * @return COMPLETE THIS IF NEEDED
	 */
	public float calculateSimilarityScore(int[] userA, int[] userB) {
		// do first movie for both user, then second... all the way til last.
		int curMovieNum = 0;
		float result = 0;

		/*
		 * SilmilarityScore calculation comprise of three parts: First, do 
		 * calculation inside the square root, then square root it to get the 
		 * distance, lastly 1/(1+distance) to get the SilmilarityScore
		 */
		while (curMovieNum < userA.length) {
			// calculation inside the square root
			result += Math.pow(userA[curMovieNum] - userB[curMovieNum], 2);
			curMovieNum++;
		}
		// square root to get the distance
		result = (float) Math.sqrt(result);
		result = 1 / (1 + result);

		return result;
	}

	public void printUserMoiveMatrix() {
		// this is a helper function for me to debug easier
		for (int[] oneUser : userMovieMatrix) {
			for (int rating : oneUser) {
				System.out.print(rating + " ");
			}
			System.out.println();
		}
	}

	/**
	 * Prints out the similarity scores of the userUserMatrix, with each row 
	 * and column representing each/single user and the cell position (i,j) 
	 * representing the similarity score between user i and user j.
	 * 
	 * @param COMPLETE THIS IF NEEDED
	 * @param COMPLETE THIS IF NEEDED
	 * @return COMPLETE THIS IF NEEDED
	 */
	public void printUserUserMatrix() {
		int arrPosition = 0;

		System.out.println();
		System.out.println();
		System.out.println("userUserMatrix is:");
		for (float[] one_user : userUserMatrix) {
			System.out.print("[");
			for (float score : one_user) {
				/*
				 * "%.4f" is to round a number to 4 digit decimal. However,
				 *  this only works on printf() and does not change the 
				 *  value of the targeted number.
				 */
				if (arrPosition == userUserMatrix.length - 1) {
					// delete "," at the last position of the array
					System.out.printf("%.4f", score);
				} else {
					System.out.printf("%.4f, ", score);
				}
				arrPosition++;

			}
			System.out.println("]");
			arrPosition = 0;
		}
	}

	public void findandPrintExtremeValue() {
		// set the extreme values to the first possible score by default
		float mostSimilarScore = userUserMatrix[0][1];
		float leastSimilarScore = userUserMatrix[0][1];
		/*
		 * startInd 1 and will increase by 1 for every new row because 
		 * diagonal line and the bottom half of matrix can be ignored
		 */
		int startInd = 1;

		for (float[] curUserScores : userUserMatrix) {
			for (int curInd = startInd;
					curInd < curUserScores.length; curInd++) {

				if (curUserScores[curInd] > mostSimilarScore) {
					/*
					 * if current score is bigger than current 
					 * mostSimilarScore, replace it
					 */
					mostSimilarScore = curUserScores[curInd];
				} else if (curUserScores[curInd] < leastSimilarScore) {
					/*
					 * if current score is smaller than current 
					 * leastSimilarScore, replace it
					 */
					leastSimilarScore = curUserScores[curInd];
				}

			}
			// startInd increase by one for every new row
			startInd++;
		}

		// find and print the user pairs that have the extreme score.
		findAndprintMostSimilarPairOfUsers(mostSimilarScore);
		findAndprintMostDissimilarPairOfUsers(leastSimilarScore);
	}

	/**
	 * This function finds and prints the most similar pair of users in the
	 * userUserMatrix.
	 * 
	 * @param COMPLETE THIS IF NEEDED
	 * @param COMPLETE THIS IF NEEDED
	 * @return COMPLETE THIS IF NEEDED
	 */

	public void findAndprintMostSimilarPairOfUsers(float mostSimilarScore) {
		int startInd = 1;
		// userA/userB value are their user number. (first user is user 1)
		int userANum = 1;
		int userBNum = 2;

		System.out.println();
		System.out.println();
		System.out.println("The most similar pairs of users "
				+ "from above userUserMatrix are: ");
		for (float[] curUserScores : userUserMatrix) {
			for (int curInd = startInd;
					curInd < curUserScores.length; curInd++) {
				// print out the user pairs if it has the mostSimilarScore
				if (curUserScores[curInd] == mostSimilarScore) {
					System.out.println(
							"User" + userANum + " and User" + userBNum);
				}
				userBNum++;
			}
			startInd++;
			userANum++;
			// userBNum always 1 bigger than A for a new row
			userBNum = userANum + 1;
		}
		System.out.printf("with similarity score of %.4f", mostSimilarScore);
		System.out.println();
	}

	/**
	 * This function finds and prints the most dissimilar pair of users in the
	 * userUserMatrix.
	 * 
	 * @param COMPLETE THIS IF NEEDED
	 * @param COMPLETE THIS IF NEEDED
	 * @return COMPLETE THIS IF NEEDED
	 */
	public void findAndprintMostDissimilarPairOfUsers(
			float leastSimilarScore) {
		int startInd = 1;
		// userA/userB value are their user number. (first user is user 1)
		int userANum = 1;
		int userBNum = 2;

		System.out.println();
		System.out.println();
		System.out.println("The most dissimilar pairs" 
				+ " of users from above userUserMatrix are: ");
		for (float[] curUserScores : userUserMatrix) {
			for (int curInd = startInd;
					curInd < curUserScores.length; curInd++) {
				// print out the user pairs if it has the mostSimilarScore
				if (curUserScores[curInd] == leastSimilarScore) {
					System.out.println(
							"User" + userANum + " and User" + userBNum);
				}
				userBNum++;
			}
			startInd++;
			userANum++;
			// userBNum always 1 bigger than A for a new row
			userBNum = userANum + 1;
		}
		System.out.printf("with similarity score of %.4f", leastSimilarScore);
		System.out.println();
		System.out.println();
	}
}
