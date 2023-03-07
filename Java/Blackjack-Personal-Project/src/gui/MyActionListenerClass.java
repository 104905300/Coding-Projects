package gui;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class MyActionListenerClass implements ActionListener{
	
	// now that the class implements the actionlistener, everytime an event occur
	//(e.g a button is clicked), the program will evoke actionPerformed method
	public void actionPerformed(ActionEvent e) {
		Object source = e.getSource();
		
	}
}

