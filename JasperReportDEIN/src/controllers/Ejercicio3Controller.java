package controllers;

import jasper.Informe3;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;

public class Ejercicio3Controller {

    @FXML
    private Button btn1;

    @FXML
    private Button btn2;

    @FXML
    private Button btn3;

    @FXML
    private Button btn4;

    /**
     * Crea informe 1
     * @param event
     */
    @FXML
    void action1(ActionEvent event) {
    	Informe3.crearInforme("/jrxml/productos.jasper");
    }

    /**
     * Crea informe 2
     * @param event
     */
    @FXML
    void action2(ActionEvent event) {
    	Informe3.crearInforme("/jrxml/secciones.jasper");
    }

    /**
     * Crea informe 3
     * @param event
     */
    @FXML
    void action3(ActionEvent event) {
    	Informe3.crearInforme("/jrxml/tabla.jasper");
    }

    /**
     * Crea informe 4
     * @param event
     */
    @FXML
    void action4(ActionEvent event) {
    	Informe3.crearInforme("/jrxml/graficos.jasper");
    }

}

