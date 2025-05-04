package com.backend.users.Security.Auth.DTOs;


import lombok.Data;

@Data
public class StudentDTO {
    public String nombre;
    public String apellido;
    public Integer grado;
    public String seccion;
    public String username;
    public String password;

}
