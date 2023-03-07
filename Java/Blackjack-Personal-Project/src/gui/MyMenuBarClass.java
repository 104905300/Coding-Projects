package gui;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;


public class MyMenuBarClass extends JMenuBar{
	
	// java need this id number for some reason lol, don't know what it does
	// maybe to distinguish this from other menuBar class? or other manual GUI class? idk 
	private static final long serialVersionUID = 1L;
	JMenuItem newGame;
	JMenuItem about;
	TheFrame frameObj = TheFrame.getInstance();

	public MyMenuBarClass() {
		
		JMenu mu = new JMenu("Option");
		newGame = new JMenuItem("New Game");
		about = new JMenuItem("About");
		
		MenuBarActionListener mbLisObj = new MenuBarActionListener();
		newGame.addActionListener(mbLisObj);
		about.addActionListener(mbLisObj);
		
		mu.add(newGame);
		mu.add(about);
		
		this.add(mu);
	}
	
	public class MenuBarActionListener implements ActionListener{
		
		// add listener to the menu ITEMS, not the menu itself
		// since menu don't need actionlistener
		public void actionPerformed(ActionEvent e) {
			if(e.getSource() == newGame) {
				resetClass.newGameReset();
				// this will show the next panel in the frame, which is the starting panel
				frameObj.cl.next(frameObj.getContentPane());
				
			} else if (e.getSource() == about) {
				// first parameter is where to show it
				JOptionPane.showMessageDialog(frameObj, "Made by Danny Liu");
			}
		}
	}
}
