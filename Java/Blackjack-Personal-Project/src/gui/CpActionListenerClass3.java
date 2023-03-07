package gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CpActionListenerClass3 implements ActionListener{
	// this is for the stay button
	public void actionPerformed(ActionEvent e) {
		CurrentPoints.userTurnEnds();

		ControlPanelClass cpObj = ControlPanelClass.getInstance();
		
		// setup for compturn, basically set some variables to their default value again.
		cpObj.compTurnPanel();
	}
}

