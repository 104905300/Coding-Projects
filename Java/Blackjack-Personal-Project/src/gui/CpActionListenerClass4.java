package gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.Timer;


public class CpActionListenerClass4 implements ActionListener {
	// this is for the OK button after user ends their turn
	
	Timer timer;
	String currentCompCardName = "";
	int nextCompSlot = 3;
	public void actionPerformed(ActionEvent e) {
		DisplayPanelClass dpObj = DisplayPanelClass.getInstance();
		dpObj.compTurn();
		
		// timer won't start until timer.start();
		timer = new Timer(800, new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				currentCompCardName =  TakeRandomImageFromFolder.start("src/pics/Cards");
				// -1 because array start count from zero
				dpObj.compCards[nextCompSlot-1] = currentCompCardName.substring(
						0,currentCompCardName.length()-5);
		        dpObj.cardslots[nextCompSlot].setIcon(
		        		ImageResize.resizer(new ImageIcon("src/pics/Cards/" + currentCompCardName)));
		        nextCompSlot++;
		        
		        // after drawing a card, calculate the points again
		       CurrentPoints.calculatePoints(DisplayPanelClass.compCards);
		      
		       
		       if (CurrentPoints.compCurrentPoints() >= 17) {
		   		   //state the computer result after drawing
		   		   CurrentPoints.compResult();
		    	   
		   		   timer.stop();
		       }
			}
		});
		
		// draw card if compCurrentPoints is less than 17, otherwise, go to result
	    if (CurrentPoints.compCurrentPoints() < 17) {
	    	//start timer
	    	//timer thread and main thread are different, keep that in mind.
	    	timer.start();
	    } else {
	    	CurrentPoints.compResult();
	    }
		
	}
}
