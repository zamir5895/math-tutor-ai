package org.example.usuarios.Salon.DTOs;

import lombok.Data;

import java.util.UUID;
import java.util.List;

@Data
public class SalonRequestDTO {
    private String seccion;

    private Integer grado;

    private String turno;

    private String desccripcion;

    private String nombre;

    private UUID profesorId;



}