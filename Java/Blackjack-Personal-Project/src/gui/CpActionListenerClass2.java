package gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.Timer;

public class CpActionListenerClass2 implements ActionListener{
	//this is for the hit button

	
	public void actionPerformed(ActionEvent e) {
		ControlPanelClass cpObj = ControlPanelClass.getInstance();
		DisplayPanelClass dpObj = DisplayPanelClass.getInstance();
		
		// this string is temp variable
		String userCardName =  TakeRandomImageFromFolder.start("src/pics/Cards");
		// -1 because array start count from zero
		dpObj.userCards[DisplayPanelClass.nextUserSlot-1] = userCardName.substring(0, userCardName.length()-5);
		
		Timer t1 = new Timer(100, new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				// +12 bc user slot is after all 12 comp slot
				// DisplayPanelClass.nextUserSlot when first run this code is 3, so we want 15th spot
	            dpObj.cardslots[DisplayPanelClass.nextUserSlot+12].setIcon(
	            		ImageResize.resizer(new ImageIcon("src/pics/Cards/" + userCardName)));
	            
	            cpObj.currentPoints = CurrentPoints.calculatePoints(DisplayPanelClass.userCards);
	            if (CurrentPoints.winOrBusted() == false) {
	            	cpObj.currentMessage.setText(cpObj.currentPoints);
	            	DisplayPanelClass.nextUserSlot++;
	            }
			}
		});
		t1.start();
		t1.setRepeats(false);
	}
}
