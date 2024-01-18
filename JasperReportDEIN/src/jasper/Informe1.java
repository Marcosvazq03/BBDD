package jasper;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

import java.sql.Connection;
import java.sql.DriverManager;

import java.util.HashMap;
import java.util.Map;
import java.util.TimeZone;

import net.sf.jasperreports.engine.JasperCompileManager;
import net.sf.jasperreports.engine.JasperExportManager;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperReport;

public class Informe1 {
	public static void main(String[] args) {
	    try {
	    	InputStream template = Informe1.class.getResourceAsStream("/jrxml/naciones.jrxml");
	    	
	    	JasperReport report = JasperCompileManager.compileReport(template);
	    	
	        Map<String, Object> parameters = new HashMap<String, Object>();
	        
	        String cadenaConexion = "jdbc:mysql://localhost/paises?serverTimezone=" + TimeZone.getDefault().getID();
	        Connection conexion = DriverManager.getConnection(cadenaConexion, "admin", "password");

	        JasperPrint print = JasperFillManager.fillReport(report, parameters, conexion);

	    	File pdf = new File("/home/dm2/naciones.pdf");
	    	JasperExportManager.exportReportToPdfStream(print, new FileOutputStream(pdf));
	    } catch (Exception e) {
	    	e.printStackTrace();
	    }
	}
	
}
