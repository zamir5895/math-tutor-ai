package org.example.usuarios.Salon.DTOs;


import lombok.Data;

@Data
public class AlumnoRegistroDTO {

    private String username;
    private String contraseña;

    public AlumnoRegistroDTO(String username, String password) {
        this.username = username;
        this.contraseña = password;
    }
}