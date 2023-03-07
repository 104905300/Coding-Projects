package gui;

import java.io.File;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;


public class TakeRandomImageFromFolder {
	//static variable mean this variable is share by all instances.
	static List<String> imageNamesList;

	// this will only RUN ONCE ever when the first time the class is called
	// I am just doing this for practice, cus I don't have to use static block
	static {
		File file = new File("src/pics/Cards");
		// file.list() give an array, change to linkedList (since array.asList alone 
		// doesn't allow removing an element) 
		// (we want to remove the card after it's selected bc don't want potential duplicate)
		imageNamesList = new LinkedList<String>(Arrays.asList(file.list()));
	}
	
	public static String start (String path) {
		
		
		Random randObj = new Random();
		int Randomindex = randObj.nextInt(imageNamesList.size());
		String selectedCardName = imageNamesList.get(Randomindex);
		imageNamesList.remove(Randomindex);
		
		return selectedCardName;
	}
	
	public static void reset() {
		File file = new File("src/pics/Cards");
		imageNamesList = new LinkedList<String>(Arrays.asList(file.list()));
	}
}
