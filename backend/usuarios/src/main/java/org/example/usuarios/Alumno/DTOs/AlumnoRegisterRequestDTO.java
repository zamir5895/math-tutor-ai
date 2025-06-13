package org.example.usuarios.Alumno.DTOs;

import lombok.Data;

@Data
public class AlumnoRegisterRequestDTO {
    private String nombre;
    private String apellido;
    private String dni;

}
