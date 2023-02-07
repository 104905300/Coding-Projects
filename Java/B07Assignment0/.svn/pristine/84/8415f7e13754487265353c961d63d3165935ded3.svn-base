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
//check starting sometime in November of 2020. If you do not complete this honor
//code, we will give you no credit and award you 0% for this component. 

package driver;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;

import a0.Cfiltering;

public class CfilteringDriver {

	/**
	 * Reads user movie ratings from a text file, 
	 * calculates similarity scores and prints a score matrix.
	 */
	public static void main(String[] args) {
		try {

			// open file to read
			String fileName;
			Scanner in = new Scanner(System.in);
			System.out.println("Enter the name of input file? ");
			fileName = in.nextLine();
			FileInputStream fStream = new FileInputStream(fileName);
			BufferedReader br = new BufferedReader(
					new InputStreamReader(fStream));

			// Read dimensions: number of users and number of movies
			int numberOfUsers = Integer.parseInt(br.readLine());
			int numberOfMovies = Integer.parseInt(br.readLine());

			/*
			 * create a new Cfiltering object that contains: a) 2d matrix
			 * i.e.userMovieMatrix (#users*#movies) b) 2d matrix 
			 * i.e. userUserMatrix(#users*#users)
			 */
			Cfiltering cfObject = new Cfiltering(
					numberOfUsers, numberOfMovies);

			// this is a blankline being read
			br.readLine();

			// read each line of movie ratings and populate the
			// userMovieMatrix
			String row;
			int curRow = 0;
			int curCol = 0;
			while ((row = br.readLine()) != null) {
				// allRatings is a list of all String numbers on one row
				String allRatings[] = row.split(" ");
				for (String singleRating : allRatings) {
					// make the String number into an integer
					// populate userMovieMatrix

					cfObject.populateUserMovieMatrix(
							curRow, curCol, Integer.parseInt(singleRating));
					curCol++;
				}
				curCol = 0;
				curRow++;
			}
			// close the file
			fStream.close();

			/*
			 * first, calculate all similarity score for all pairs of users. 
			 * Then print out the corresponding userUserMatrix. Lastly, 
			 * find and print the most similar and dissimilar pairs 
			 * of users(I called it "Extreme Value")
			 */
			cfObject.calculateSimilarityScoreForAllPairsOfUser();
			cfObject.printUserUserMatrix();
			cfObject.findandPrintExtremeValue();

		} catch (FileNotFoundException e) {
			System.err.println("Do you have the input file"
					+ " in the root folder " + "of your project?");
			System.err.print(e.getMessage());
		} catch (IOException e) {
			System.err.print(e.getMessage());
		}
	}

}
