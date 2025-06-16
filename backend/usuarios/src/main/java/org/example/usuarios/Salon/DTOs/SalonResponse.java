package org.example.usuarios.Salon.DTOs;

import lombok.Data;

import java.util.UUID;

@Data
public class SalonResponse {

    private UUID id;
    private String nombre;
    private Integer grado;
    private String seccion;
    private String turno;
    private Integer cantidadAlumnos;
    private String descripcion;
}