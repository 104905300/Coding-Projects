package gui;

import java.awt.CardLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class NextRoundActionListenerClass implements ActionListener{
	public void actionPerformed(ActionEvent e) {
		resetClass.nextRoundReset();
	}
}
