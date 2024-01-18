package jasper;

import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.HashMap;
import java.util.Map;
import java.util.TimeZone;

import javafx.scene.control.Alert;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperReport;
import net.sf.jasperreports.engine.util.JRLoader;
import net.sf.jasperreports.view.JasperViewer;

public class Informe2 {
	public static void crearInforme(String ruta) {
	    try {
	    	InputStream jasper = Informe2.class.getResourceAsStream(ruta);
	    	
	        // Parameters for report
	        Map<String, Object> parameters = new HashMap<String, Object>();
	        
	        String cadenaConexion = "jdbc:mysql://localhost/agenda?serverTimezone=" + TimeZone.getDefault().getID();
	        Connection conexion = DriverManager.getConnection(cadenaConexion, "admin", "password");
	        
			try {
				JasperReport report = (JasperReport) JRLoader.loadObject(jasper);
		        JasperPrint jprint = JasperFillManager.fillReport(report, parameters, conexion);
		        JasperViewer viewer = new JasperViewer(jprint, false);
		        viewer.setVisible(true);
			} catch (Exception e) {
	            Alert alert = new Alert(Alert.AlertType.ERROR);
	            alert.setHeaderText(null);
	            alert.setTitle("ERROR");
	            alert.setContentText("Ha ocurrido un error");
	            alert.showAndWait();
	            e.printStackTrace();
	        }
	    } catch (Exception e) {
	    	e.printStackTrace();
	    }
	}
}
