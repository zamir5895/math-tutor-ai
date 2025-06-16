package org.example.usuarios.Profesor.DTOs;

import lombok.Data;

import java.util.UUID;

@Data
public class ResponseProfesor {
    private UUID id;
    private String nombre;
    private String apellido;
    private String username;
    private String password;
    private String telefono;

}