package gui;
import java.awt.CardLayout;
import javax.swing.JFrame;


public class TheFrame extends JFrame{
	StartingPanelClass startingPanelObj;
	PlayingPanelClass playingPanelObj;
	CardLayout cl;
	// use singleton pattern  
	private static TheFrame instance;
	
	private TheFrame() {
		
	}
	
	public static TheFrame getInstance(){
		if (instance == null) {
			instance = new TheFrame();
		}
		return instance;
	}
	
	
	public void create() {
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setSize(1280,960);
		this.setVisible(true);
		
		this.setLayout(new CardLayout());
		
		startingPanelObj = new StartingPanelClass();
		playingPanelObj = PlayingPanelClass.getInstance();
		playingPanelObj.create();
		
		// first show startingPanel, then show playingPanel 
		this.add(startingPanelObj);
		this.add(playingPanelObj);
	}
	
	public void removePlayingPanel() {
		this.remove(playingPanelObj);
	}
}
