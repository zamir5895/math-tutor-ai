package com.backend.users.Security.Auth.DTOs;

import lombok.Data;

@Data
public class DtoProfessor {
    private String nombre;
    private String apellido;
    private String contraseña;
    private String correo;
}
