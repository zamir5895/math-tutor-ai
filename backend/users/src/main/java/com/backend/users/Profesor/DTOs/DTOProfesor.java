package com.backend.users.Profesor.DTOs;

import lombok.Data;

@Data
public class DTOProfesor {
    private Long id;
    private String nombre;
    private String apellido;
    private String emaill;
    private Integer edad;
}
