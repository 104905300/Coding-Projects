package gui;
import java.awt.Color;
import java.awt.GridLayout;

import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JPanel;


public class DisplayPanelClass extends JPanel{
	
	// ignore for now, just a warning if this variable is not here
	private static final long serialVersionUID = 1L;
	
	// Singleton Pattern
	private static DisplayPanelClass instance;
	static JLabel cardslots[];
	static String[] userCards = new String[11];
	static String[] compCards = new String[11];
	static int nextUserSlot = 0;
	static int nextCompSlot = 0;
	// compCard2file was changed in CpActionListener class
	static String compCard2file = "";
	
	private DisplayPanelClass() {
		
	}
	
	public static DisplayPanelClass getInstance(){
		if (instance == null) {
			instance = new DisplayPanelClass();
		}
		return instance;
	}
	
	public void create() {
		
		// create two JPanels(one for user, one for comp) to sort JLabels which is created to fit card images
		JPanel userCardPanel = new JPanel();
		JPanel compCardPanel = new JPanel();

		// set the panel to GridLayout of 2 rows and as many columns as it takes
		compCardPanel.setLayout(new GridLayout(2,0));
		userCardPanel.setLayout(new GridLayout(2,0));
		
		// put comp panel on top, user panel on bottom (null layout manager shrink the whole thing so need gridlayout instead)
		this.setLayout(new GridLayout(0,1));
		this.add(compCardPanel);
		this.add(userCardPanel);

		//--------------------------------------------------------------------
		// put card slots in JLebels (and comp and user name on first slot)
		cardslots = new JLabel[24];
		
		// the weird html and br/ is for displaying two lines of text //
		cardslots[0] = new JLabel("Comp");
		compCardPanel.add(cardslots[0]);
		for (int i=1; i<12; i++) {
			cardslots[i] = new JLabel(Integer.toString(i));
			compCardPanel.add(cardslots[i]);
		}
		
		cardslots[12] = new JLabel("<html><br/><br/>User<br/><br/><html> Money: $" + CompAndPlayerVarsAndBettingResult.userCurMoney);
		userCardPanel.add(cardslots[12]);
		for (int i=13; i<24; i++) {
			cardslots[i] = new JLabel(Integer.toString(i));
			userCardPanel.add(cardslots[i]);
		}
	}
	public void compTurn() {
		// show the second comp card now and calculate the points, keep drawing cards if it's not
		// bigger or equal to 17.
		ControlPanelClass cpObj = ControlPanelClass.getInstance();
		DisplayPanelClass dpObj = DisplayPanelClass.getInstance();
		cpObj.removeAll();
		cpObj.revalidate();
		cpObj.repaint();
		cpObj.currentMessage.setText("");
		cpObj.add(cpObj.currentMessage);
		
		// setup for compturn, basically set some variables to their default value again. 
		CurrentPoints.compCountInit();
		
		
		// compCard2file value was change in some 
		// other class(since it's static), that's why it's not "" anymore
		
		// show comp card #2 then calculate points
		cardslots[2].setIcon(
         	ImageResize.resizer(new ImageIcon("src/pics/Cards/" + compCard2file)));
		CurrentPoints.calculatePoints(DisplayPanelClass.compCards);
	}
	public static void reset() {
		userCards = new String[11];
		compCards = new String[11];
		nextUserSlot = 0;
		nextCompSlot = 0;
		compCard2file = "";
		
	}
}
