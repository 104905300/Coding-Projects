package gui;
import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Dimension;

import javax.swing.JPanel;


public class PlayingPanelClass extends JPanel{

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	private static PlayingPanelClass instance;
	
	static CardLayout cl = new CardLayout();
	
	public static PlayingPanelClass getInstance(){
		if (instance == null) {
			instance = new PlayingPanelClass();
		}
		return instance;
	}
	
	private PlayingPanelClass () {
		
	}
	
	public void create() {

		// evoke parent class constructor and its parameter, if you don't write this line,
		// parent constructor will still evoke automatically but with no parameter.
		
	
		
		//--------------------------------------------------------------------
		// set up menu stuff 
		MyMenuBarClass menuBarObj = new MyMenuBarClass();
		
		//--------------------------------------------------------------------
		// set up panel stuff
		DisplayPanelClass displayPanelObj = DisplayPanelClass.getInstance();
		displayPanelObj.create();
		//--------------------------------------------------------------------
		// create another JPanel for user interface (JButtons and stuff)
		ControlPanelClass ControlPanelObj = ControlPanelClass.getInstance();
		ControlPanelObj.create();
		
		//--------------------------------------------------------------------
		// create layout for the menu and the two JPanels (NORTH MIDDLE and SOUTH)
		this.setLayout(new BorderLayout());
		this.add(BorderLayout.NORTH, menuBarObj);
		this.add(BorderLayout.CENTER, displayPanelObj);
		this.add(BorderLayout.SOUTH, ControlPanelObj);
		ControlPanelObj.setPreferredSize(new Dimension(1280, 70));
		ControlPanelObj.setBackground(Color.GREEN);
	}
}
