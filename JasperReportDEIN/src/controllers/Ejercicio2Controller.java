package controllers;

import jasper.Informe2;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;

import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.control.RadioButton;
import javafx.scene.control.ToggleGroup;

import javafx.stage.Stage;

public class Ejercicio2Controller {

    @FXML
    private Button btnAceptar;

    @FXML
    private Button btnCancelar;

    @FXML
    private RadioButton rbInformePersonas;

    @FXML
    private RadioButton rbInformePersonasConCalculos;

    @FXML
    private RadioButton rbInformePersonasConSubinformes;

    @FXML
    private ToggleGroup tgInforme;

    /**
     * Boton aceptar y genera informe.
     * @param event
     */
    @FXML
    void aceptar(ActionEvent event) {
    	
    	final RadioButton seleccionado = (RadioButton) tgInforme.getSelectedToggle();
    	
    	if (seleccionado != null) {    		
    		if (seleccionado.equals(rbInformePersonas)) {
    			Informe2.crearInforme("/jrxml/agenda1.jasper");
    		} else if (seleccionado.equals(rbInformePersonasConCalculos)) {
    			Informe2.crearInforme("/jrxml/agenda2.jasper");
    		} else if (seleccionado.equals(rbInformePersonasConSubinformes)) {
    			Informe2.crearInforme("/jrxml/agenda3.jasper");
    		}
    	}
    }

    /**
     * Boton cancelar.
     * @param event
     */
    @FXML
    void cancelar(ActionEvent event) {
    	((Stage)((Node)event.getSource()).getScene().getWindow()).close();
    }

}
