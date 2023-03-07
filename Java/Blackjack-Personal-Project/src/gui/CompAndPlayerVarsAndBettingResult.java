package gui;

public class CompAndPlayerVarsAndBettingResult {
	static int userCurMoney = 100;
	static int betSizing = 0;
	
	// init to everything false first, change to true after result
	static boolean compWin = false;
	static boolean userWin = false;
	static boolean tieGame = false;
	
	public static void bettingResult () {
		// if comp win, take away money, if user win, add to money, 
		// if user win and have blackjack, the reward being added is 1.5x (50 reward becomes 75)
		if(compWin) {
			userCurMoney = userCurMoney - betSizing;
		} else if (userWin && !CurrentPoints.blackJack) {
			userCurMoney = userCurMoney + betSizing;
		} else if (userWin && CurrentPoints.blackJack) {
			userCurMoney = userCurMoney + (int)Math.round((betSizing * 1.5)) ;
		}
		// change user money according to win/loss. Or no change if it's tie game.
		DisplayPanelClass.cardslots[12].setText("<html><br/><br/>User<br/><br/><html> Money: $" + userCurMoney);
	}
	public static void reset() {
		compWin = false;
		userWin = false;
		tieGame = false;
	}
	public static void newGameReset() {
		userCurMoney = 100;
		betSizing = 0;
	}
}
