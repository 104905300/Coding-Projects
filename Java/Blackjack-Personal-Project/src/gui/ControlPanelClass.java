package gui;
import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.Timer;


public class ControlPanelClass extends JPanel{

	/**
	 * lol random variable java needs
	 */
	private static final long serialVersionUID = 1L;
	
	
	private static ControlPanelClass instance;
	
	static JButton confirm_bet;
	
	static JLabel currentMessage;
	static JButton hit;
	static JButton stay;
	static JButton compTurnButton;
	static String currentPoints;
	static JTextField bet_input;
	static JButton nextRound;
	
	private ControlPanelClass() {
		
	}
	public static ControlPanelClass getInstance(){
		if (instance == null) {
			instance = new ControlPanelClass();
		}
		// do init here for variables that u want to init 
		nextRound = new JButton("Next round");
		NextRoundActionListenerClass nrLisObj = new NextRoundActionListenerClass();
		nextRound.addActionListener(nrLisObj);
		
		return instance;
	}
	
	public void create() {

		JLabel bet_prompt = new JLabel("Enter your bet!");
		bet_input = new JTextField("", 20);
		confirm_bet = new JButton("Confirm");
		CpActionListenerClass lisObj = new CpActionListenerClass();
		confirm_bet.addActionListener(lisObj);
		JPanel betPanel = new JPanel();
		
		betPanel.add(bet_prompt);
		betPanel.add(bet_input);
		betPanel.add(confirm_bet);
		
		this.add(betPanel);
	}
	
	public void createHitStayPanel() {
		this.removeAll();
		// revalidate will refresh the layout
		this.revalidate();
		// repaint will "clean up" the panel after removing component
		this.repaint();
		
		// init currentMessage so it SHOWS UP
		currentMessage = new JLabel();
		
		// DisplayPanelClass.compCards[0] is the same as dpObj.compCards[0]
		// bc compCards[0] is static
		
		currentPoints = CurrentPoints.calculatePoints(DisplayPanelClass.userCards);
		if (CurrentPoints.winOrBusted() == false) {
			currentMessage.setText(currentPoints);
			
			hit = new JButton("Hit");
			CpActionListenerClass2 lisObj2 = new CpActionListenerClass2();
			hit.addActionListener(lisObj2);
			
			stay = new JButton("Stay");
			CpActionListenerClass3 lisObj3 = new CpActionListenerClass3();
			stay.addActionListener(lisObj3);
		
			this.add(currentMessage);
			this.add(hit);
			this.add(stay);
		}
	}
	
	public void winOrBustedPanel(String winOrBusted) {
		CurrentPoints.userTurnEnds();
		
		DisplayPanelClass dpObj = DisplayPanelClass.getInstance();
		this.removeAll();
		this.revalidate();
		this.repaint();
		
		// if user got blackjack and comp don't have 10 j q k A
		if (winOrBusted.equals("Blackjack")) {
			if (dpObj.compCards[0].matches("10|J|Q|K|A")) {
				compTurnPanel();
				return;
			} else {
				CompAndPlayerVarsAndBettingResult.userWin = true;
				CurrentPoints.blackJack = true;
				CompAndPlayerVarsAndBettingResult.bettingResult();
				currentMessage = new JLabel("Blackjack! Congraduation, you win!");
			}
		} else if (winOrBusted.equals("21")) {
			currentMessage = new JLabel("Congrats, you got 21!");
			compTurnPanel();
			return;
		} else if (winOrBusted.equals("Busted")){
			CompAndPlayerVarsAndBettingResult.compWin = true;
			CompAndPlayerVarsAndBettingResult.bettingResult();
			currentMessage = new JLabel("Oh no, you busted! Better luck next time.");
		}
		
		// if game over(win or busted), then show message and next round button
		this.add(currentMessage);
		this.add(nextRound);
	}
	
	public void compTurnPanel() {
		this.removeAll();
		this.revalidate();
		this.repaint();

		// if user has blackjack(and comp has A K Q J or 10) or 21, automatically ends users turn
		// and move on to comp turn
		if (CurrentPoints.blackJack) {
			currentMessage.setText("Congrats, you got BlackJack! Computer Turn...");
		} else if (CurrentPoints.getUserFinalPoints() == 21) {
			currentMessage.setText("Congrats, you got 21! Computer Turn...");
		} else {
			currentMessage.setText("You got " + CurrentPoints.getUserFinalPoints() + ", Computer Turn...");
		}
		compTurnButton = new JButton("OK");
		CpActionListenerClass4 lisObj4 = new CpActionListenerClass4();
		compTurnButton.addActionListener(lisObj4);
		this.add(currentMessage);
		this.add(compTurnButton);
	}
}
