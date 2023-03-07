package gui;
import java.awt.Image;
import javax.swing.ImageIcon;


public class ImageResize {
	public static ImageIcon resizer(ImageIcon imageicon) {
		Image image = imageicon.getImage(); // transform it 
		Image newimg = image.getScaledInstance(180, 180, Image.SCALE_SMOOTH); // scale it the smooth way  
		imageicon = new ImageIcon(newimg);
		
		return imageicon;
	}
}
