package org.example.usuarios.Alumno.DTOs;

import lombok.Data;

import java.util.UUID;

@Data
public class AlumnoResponseDTO {
    private String id;
    private String username;
    private String dni;
    private UUID salon;
    private String role;
    private String createdAt;


}