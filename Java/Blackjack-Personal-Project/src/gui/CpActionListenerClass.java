package gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JOptionPane;
import javax.swing.Timer;


public class CpActionListenerClass implements ActionListener{
	//this is for the confirm bet button
		
	// now that the class implements the actionlistener, everytime an event occur
	//(e.g a button is clicked), the program will evoke actionPerformed method
	
	static String compCardName1;
	static String compCardName2;
	static String userCardName1;
	static String userCardName2;
	
	int[] startingFourSlotNum = {1,2,13,14};
	String[] startingFourCardNames = new String[4];
	int curArrayNum = 0;
	Timer t1;
	
	ControlPanelClass cpObj = ControlPanelClass.getInstance();
	DisplayPanelClass dpObj = DisplayPanelClass.getInstance();
	
	public void actionPerformed(ActionEvent e) {
		
		// validate the bet size. That is, it needs to be a postive whole number, and it can't be over the player current money 
		// if input not valid, do exit out of the method and do nothing
		if (!validateBetZize()) {
			return;
		}
		// after validate, get the num from textfield and set it to bet sizing
		CompAndPlayerVarsAndBettingResult.betSizing = Integer.parseInt(cpObj.bet_input.getText());

		// set the control panel to blank momentarily so user can't click the confirm button again
		cpObj.removeAll();
		cpObj.revalidate();
		cpObj.repaint();
		
		// get four random cards
		compCardName1 = TakeRandomImageFromFolder.start("src/pics/Cards");
		compCardName2 = TakeRandomImageFromFolder.start("src/pics/Cards");
		dpObj.compCard2file = compCardName2;
		userCardName1 = TakeRandomImageFromFolder.start("src/pics/Cards");
		userCardName2 = TakeRandomImageFromFolder.start("src/pics/Cards");
		startingFourCardNames[0] = compCardName1;
		startingFourCardNames[1] = "gray_back.png";
		startingFourCardNames[2] = userCardName1;
		startingFourCardNames[3] = userCardName2;

		
		// delete last 5 chars, the remaining chars are the cards num(2-10, JQKA)
		// substring(0,1) doesn't work bc 10 has two chars
		dpObj.compCards[0] = compCardName1.substring(0, compCardName1.length()-5);
		dpObj.compCards[1] = compCardName2.substring(0, compCardName2.length()-5);
		dpObj.userCards[0] = userCardName1.substring(0, userCardName1.length()-5);
		dpObj.userCards[1] = userCardName2.substring(0, userCardName2.length()-5);

			
		// timer to delay an event. (don't know why it needs another actionListener, oh well)
		// don't show comp card 2 yet, only show the card back for now
		t1 = new Timer(300, new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				// loop through startingFourSlotNum from element 0-3 (1,2,13,14)
				// also loop through startingFourCardNames from element 0-3 (compCardName1, "gray_back.png", userCardName1,userCardName2)
				if(curArrayNum == 1) {
		            dpObj.cardslots[startingFourSlotNum[curArrayNum]].setIcon(
		            		ImageResize.resizer(new ImageIcon("src/pics/Card Back/" + startingFourCardNames[curArrayNum])));
				} else {
		            dpObj.cardslots[startingFourSlotNum[curArrayNum]].setIcon(
		            		ImageResize.resizer(new ImageIcon("src/pics/Cards/" + startingFourCardNames[curArrayNum])));
				}
	            
	            // curArrayNum loop through timer 4 times then stop
	            if (curArrayNum < 3) {
	            	curArrayNum++;
	            } else {
		   			// change control panel to hit stay info panel
		   			cpObj.createHitStayPanel();
		   			// 0th spot is the name, so card slot start from 1
		   			DisplayPanelClass.nextUserSlot = 3;
	            	t1.stop();
	            }
	            
	           	}
			});
		t1.start();

	}
	
	public boolean validateBetZize() {
		boolean validInput = false;
		// get the text from text field
		String stringBet = cpObj.bet_input.getText();
		int bet = 0;
		try {
			bet = Integer.parseInt(stringBet);
			
		} catch (NumberFormatException e) {
			// if input is not a number, return and do nothing
			JOptionPane.showMessageDialog(null, "Please enter a valid input!!!");
			return validInput;
		}
		if (bet <= 0 || bet > CompAndPlayerVarsAndBettingResult.userCurMoney) {
			// if input is not a valid number, return and do nothing
			JOptionPane.showMessageDialog(null, "Please enter a valid number!!!");
			return validInput;
		}
		
		// if no return from above, then the input is valid
		validInput = true;
		return validInput;
	}
}
