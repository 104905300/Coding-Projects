package gui;

public class resetClass {
	public static void nextRoundReset() {
		// when next round button is click, reset all the necessary variables
		// clean all the necessary panels
		// then call the PlayingPanel to play again
		DisplayPanelClass.reset();
		CurrentPoints.reset();
		CompAndPlayerVarsAndBettingResult.reset();
		TakeRandomImageFromFolder.reset();
		
		ControlPanelClass cpObj = ControlPanelClass.getInstance();
		cpObj.removeAll();
		cpObj.revalidate();
		cpObj.repaint();
		
		DisplayPanelClass dpObj = DisplayPanelClass.getInstance();
		dpObj.removeAll();
		dpObj.revalidate();
		dpObj.repaint();
		
		PlayingPanelClass ppObj = PlayingPanelClass.getInstance();
		ppObj.removeAll();
		ppObj.revalidate();
		ppObj.repaint();
		
		ppObj.create();
	}
	
	public static void newGameReset() {
		// new game just need next round reset properties plus some extra variables 
		// in CompAndPlayerVarsAndBettingResult class. (Reset variable first though)
		CompAndPlayerVarsAndBettingResult.newGameReset();
		nextRoundReset();
	}
}
