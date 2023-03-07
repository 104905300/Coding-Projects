package gui;

import javax.swing.JButton;
import javax.swing.JLabel;

public class CurrentPoints {
	static int curInd = 0;
	static int result = 0;
	// result2 is for when there is Ace present(Ace could be 1 or 11)
	static int result2 = 0;
	static boolean hasAce = false;
	static int userFinalResult = 0;
	static int compFinalResult = 0;
	static boolean blackJack = false;
	
	/**
	public static void UserStartingPoints() {
		if (DisplayPanelClass.userCards[0])
		
		if(DisplayPanelClass.userCards[0].equals("A") || DisplayPanelClass.userCards[1].equals("A")) {
			
			hasAce = true;
			if(DisplayPanelClass.userCards[0].equals("A") && DisplayPanelClass.userCards[1].equals("A")) {
				result = "1";
				result2 = "11";
			}
			// Blackjack 
			else if (DisplayPanelClass.userCards[0].matches("10|J|Q|K")
					|| DisplayPanelClass.userCards[1].matches("10|J|Q|K")){
				result = "Blackjack! Congraduation, you win!";
			}
			else {
				
			}
		}
	}
	*/
	
	public static String calculatePoints(String[] userOrCompCards) {
		// this method is shared between user and comp point count.
		// return string bc that's what jLabel want when show the result on it.
		
		// if ind is not bigger than length and there is card present in array, add to it
		while(curInd < userOrCompCards.length && userOrCompCards[curInd] != null) {
			
			if (userOrCompCards[curInd].equals("A")) {
				hasAce = true;
				// think about it, why this case use result + 11 but not use result2 to add like the next two cases
				result2 = result + 11;
				result = result + 1;
			} else if (userOrCompCards[curInd].matches("10|J|Q|K")) {
				if (hasAce) {
					result2 = result2 + 10;
				}
				result = result + 10;
			} else {
				if (hasAce) {
					result2 = result2 + Integer.parseInt(userOrCompCards[curInd]);
				}
				result = result + Integer.parseInt(userOrCompCards[curInd]);

			}
			curInd ++;
		}

		// has ace and return both possible points (e.g. 9/19)
		if(hasAce && result2 < 21) {
			return String.valueOf(result) + "/" + String.valueOf(result2);
		// has ace and also 11/21, in this case return 21
		} else if(hasAce && result2 == 21) {
			result = result2;
			return String.valueOf(result);
		} else {
			return String.valueOf(result);
		}
	}
	
	public static boolean winOrBusted() {
		// this method check if win or 21 or busted condition occur, if 
		// yes, show appropriate action, if no, return and user continue the game
		
		boolean wOb = false;
		// blackjack
		ControlPanelClass cpObj = ControlPanelClass.getInstance();
		if (result == 21 && curInd ==2) {
			blackJack = true;
			cpObj.winOrBustedPanel("Blackjack");
			wOb = true;
		} else if(result == 21) {
			cpObj.winOrBustedPanel("21");
			wOb = true;
		} else if(result > 21) {
			cpObj.winOrBustedPanel("Busted");
			wOb = true;
		}
		return wOb;
	}
	
	public static void userTurnEnds() {
		if (hasAce && result2 <= 21) {
			userFinalResult = result2;
		} else {
			userFinalResult = result;
		}
	}
	
	public static void compCountInit() {
		// reset everything first

		curInd = 0;
		result = 0;
		result2 = 0;
		hasAce = false;
	}
	
	public static int compCurrentPoints() {
		// if it's computer turn, then update current point in number format
		if (hasAce && result2 <= 21) {
			return result2;
		} else {
			return result;
		}
	}
	
	public static void compResult() {
		// this method is called when compPoints is 17 or more
		
		// for when there is an ace, use the higher score if it's not busted(over 21)
		if (hasAce && result2 <= 21) {
			compFinalResult = result2;
		} else {
			compFinalResult = result;
		}
		
		if (compFinalResult > 21) {
			CompAndPlayerVarsAndBettingResult.userWin = true;
			ControlPanelClass.currentMessage.setText("Computer busted, you won!");
		} else if (compFinalResult == 21 && curInd ==2) {
			CompAndPlayerVarsAndBettingResult.compWin = true;
			ControlPanelClass.currentMessage.setText(
					"Computer got Blackjack, computer won!");
		} else if (compFinalResult > userFinalResult) {
			CompAndPlayerVarsAndBettingResult.compWin = true;
			ControlPanelClass.currentMessage.setText(
				"Computer got " + compFinalResult + ", computer won!");
		} else if(compFinalResult == userFinalResult) {
			CompAndPlayerVarsAndBettingResult.tieGame = true;
			ControlPanelClass.currentMessage.setText(
					"Computer got " + compFinalResult + ", tie game!");
		} else if (compFinalResult < userFinalResult) {
			CompAndPlayerVarsAndBettingResult.userWin = true;
			ControlPanelClass.currentMessage.setText(
					"Computer got " + compFinalResult + ", you won!");
		}
		// do user money change after result
		ControlPanelClass cpObj = ControlPanelClass.getInstance();
		cpObj.add(ControlPanelClass.nextRound);
		CompAndPlayerVarsAndBettingResult.bettingResult();
		
	}
	public static int getUserFinalPoints() {
		return userFinalResult;
	}
	public static boolean isBlackJack() {
		return blackJack;
	}
	
	public static void reset() {
		curInd = 0;
		result = 0;
		// result2 is for when there is Ace present(Ace could be 1 or 11)
		result2 = 0;
		hasAce = false;
		userFinalResult = 0;
		compFinalResult = 0;
		blackJack = false;
	}
}
