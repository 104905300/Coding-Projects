package gui;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.util.concurrent.TimeUnit;


public class StartingPanelClass extends JPanel {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	JButton play;
	
	public StartingPanelClass() {
	
		this.setLayout(new GridBagLayout());
		JPanel titleAndPlayHolder = new JPanel();
		titleAndPlayHolder.setLayout(new BoxLayout(titleAndPlayHolder, BoxLayout.Y_AXIS));
		
		JLabel title = new JLabel("BlackJack"); 
		
		play = new JButton("Play");
		// create an actionlistener obj
		PlayButtonActionListener actionListenerObj = new PlayButtonActionListener();
		play.addActionListener(actionListenerObj);
		
		titleAndPlayHolder.add(title);
		titleAndPlayHolder.add(Box.createVerticalStrut(10));
		titleAndPlayHolder.add(play);	
		this.add(titleAndPlayHolder);
		
	}
	public class PlayButtonActionListener implements ActionListener{
		// this is for the play button
		
		// now that the class implements the actionlistener, everytime an event occur
		//(e.g a button is clicked), the program will evoke actionPerformed method
		
		public void actionPerformed(ActionEvent e) {
			
			if (e.getSource().equals(play)) {
				// frame have 2 panel, can change from one to the other using card layout.
				TheFrame aFrameObj = TheFrame.getInstance();
				aFrameObj.cl = (CardLayout) aFrameObj.getContentPane().getLayout();
				aFrameObj.cl.next(aFrameObj.getContentPane());
				
			}
		}
	}
}
