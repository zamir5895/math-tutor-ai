package org.example.usuarios.Salon.DTOs;

import lombok.Data;

@Data
public class RegistroMasivoResponse {

    private int cantidadRegistrados;
    private String csvRespuesta;
    public RegistroMasivoResponse(int cantidadRegistrados, String csvRespuesta) {
        this.cantidadRegistrados = cantidadRegistrados;
        this.csvRespuesta = csvRespuesta;
    }
}
