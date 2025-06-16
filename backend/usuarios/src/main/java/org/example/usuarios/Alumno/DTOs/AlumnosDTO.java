package org.example.usuarios.Alumno.DTOs;


import lombok.Data;

import java.util.UUID;

@Data
public class AlumnosDTO {
    private UUID id;
    private String nombre;
    private String apellido;
    private String dni;
    private String username;
}