module JasperReportDEIN {
	requires javafx.controls;
	requires java.desktop;
	requires javafx.web;
	requires javafx.fxml;
	requires javafx.swing;
	requires javafx.media;
	requires javafx.graphics;
	requires jasperreports;
	requires java.sql;
	opens application to javafx.graphics, javafx.fxml, jasperreports;
	opens controllers to javafx.graphics, javafx.fxml, jasperreports;
}
