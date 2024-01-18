package jasper;

import java.io.InputStream;
import java.util.Map;

import javafx.scene.control.Alert;
import net.sf.jasperreports.engine.JREmptyDataSource;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperReport;
import net.sf.jasperreports.engine.util.JRLoader;
import net.sf.jasperreports.view.JasperViewer;

public class Informe4 {
	public static void crearInforme(Map<String, Object> parameters){
	    try {
	    	InputStream jasper = Informe4.class.getResourceAsStream("/jrxml/medico.jasper");
			try {
				JasperReport report = (JasperReport) JRLoader.loadObject(jasper);
		        JasperPrint jprint = JasperFillManager.fillReport(report, parameters, new JREmptyDataSource());
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
