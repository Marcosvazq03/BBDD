package controllers;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

import jasper.Informe4;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;

import javafx.scene.Node;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.TextInputControl;

import javafx.stage.Stage;

public class Ejercicio4Controller {

    @FXML
    private Button btnGenerarInforme;

    @FXML
    private Button btnLimpiar;

    @FXML
    private Button btnSalir;

    @FXML
    private TextArea taTratamiento;

    @FXML
    private TextField tfCodigoMedico;

    @FXML
    private TextField tfDireccionPaciente;

    @FXML
    private TextField tfEspecialidadMedico;

    @FXML
    private TextField tfNombreMedico;

    @FXML
    private TextField tfNombrePaciente;

    @FXML
    private TextField tfNumeroPaciente;

    /**
     * Crea informe
     * @param event
     */
    @FXML
    void generarInforme(ActionEvent event) {
    	if (validarCampos()) {
    		try {
				Informe4.crearInforme(crearParametros());
			} catch (Exception e) {
	    		Alert alert = new Alert(AlertType.ERROR, e.getMessage(), ButtonType.OK);
	    		alert.show();
	    		e.printStackTrace();
			}
    	}
    }
    
    /**
     * Crea lo parametros
     * @return
     */
    private Map<String, Object> crearParametros() {
    	Map<String, Object> parametros = new HashMap<String, Object>(7);
    	
    	parametros.put("NOM_MEDICO", tfNombreMedico.getText().trim());
    	parametros.put("TRATAMIENTO", taTratamiento.getText().trim());
    	parametros.put("COD_MEDICO", Integer.parseInt(tfCodigoMedico.getText()));
    	parametros.put("ESP_MEDICO", tfEspecialidadMedico.getText().trim());
    	parametros.put("NUM_PACIENTE", Integer.parseInt(tfNumeroPaciente.getText()));
    	parametros.put("NOM_PACIENTE", tfNombrePaciente.getText().trim());
    	parametros.put("DIR_PACIENTE", tfDireccionPaciente.getText().trim());
    	
    	
    	return parametros;
    }

    /**
     * Valida los campos
     * @return
     */
    private boolean validarCampos() {
    	StringBuilder sbErrores = new StringBuilder();
    	validarCampoRequerido(
    			sbErrores,
    			taTratamiento,
    			tfCodigoMedico,
    			tfDireccionPaciente,
    			tfEspecialidadMedico,
    			tfNombreMedico,
    			tfNombrePaciente,
    			tfNumeroPaciente);
    	
    	validarCampoNumerico(sbErrores,
    			tfCodigoMedico,
    			tfNumeroPaciente);
    	
    	if (!sbErrores.isEmpty()) {
    		Alert alert = new Alert(AlertType.ERROR, sbErrores.toString(), ButtonType.OK);
    		alert.show();
    	}
    	
    	return sbErrores.isEmpty();
	}

    /**
     * Boton limpiar
     * @param event
     */
	@FXML
    void limpiar(ActionEvent event) {
    	taTratamiento.clear();
        tfCodigoMedico.clear();
        tfDireccionPaciente.clear();
        tfEspecialidadMedico.clear();
        tfNombreMedico.clear();
        tfNombrePaciente.clear();
        tfNumeroPaciente.clear();
    }

	/**
	 * Boton salir
	 * @param event
	 */
    @FXML
    void salir(ActionEvent event) {
    	((Stage)((Node)event.getSource()).getScene().getWindow()).close();
    }
    
    /**
     * Mensaje de Campo requerido
     * @param <T>
     * @param errores
     * @param campo
     */
    @SafeVarargs
	private static <T extends TextInputControl> void validarCampoRequerido(StringBuilder errores, T... campo) {
    	
    	Arrays.stream(campo).forEach(c -> {
    		if (c.getText().isBlank()) {
    			errores.append("Se requiere el campo " + c.getId() + ".\n");
    		}
    	});
    }
    
    /**
     * Mensaje de Campo numerico
     * @param <T>
     * @param errores
     * @param campo
     */
    @SafeVarargs
	private static <T extends TextInputControl> void validarCampoNumerico(StringBuilder errores, T... campo) {
    	
    	Pattern pattern = Pattern.compile("\\d+");
    	Arrays.stream(campo).forEach(c -> {
    		if (!pattern.matcher(c.getText().trim()).matches()) {
    			errores.append("El campo " + c.getId() + " debe ser un numero.\n");
    		}
    	});
    }
    

}
