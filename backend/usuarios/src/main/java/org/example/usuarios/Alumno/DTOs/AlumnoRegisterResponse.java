package org.example.usuarios.Alumno.DTOs;

import lombok.Data;

import java.util.UUID;

@Data
public class AlumnoRegisterResponse {

    private String nombre;
    private String apellido;
    private String dni;
    private String username;
    private String contraseña;
    private UUID id;

    public AlumnoRegisterResponse(String nombre, String apellido, String dni, String username, String contraseña, UUID id) {
        this.nombre = nombre;
        this.apellido = apellido;
        this.dni = dni;
        this.username = username;
        this.contraseña = contraseña;
        this.id = id;
    }
}
