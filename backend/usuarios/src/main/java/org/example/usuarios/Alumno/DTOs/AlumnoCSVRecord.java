package org.example.usuarios.Alumno.DTOs;

import lombok.Data;

@Data
public class AlumnoCSVRecord {
    private String nombre;
    private String apellido;
    private String dni;

    public AlumnoCSVRecord(String trim, String trim1, String trim2) {
        this.nombre = trim;
        this.apellido = trim1;
        this.dni = trim2;
    }
}