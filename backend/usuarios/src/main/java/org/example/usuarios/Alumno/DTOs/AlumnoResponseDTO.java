package org.example.usuarios.Alumno.DTOs;

public class AlumnoResponseDTO {
    private String id;
    private String username;
    private String dni;
    private String seccion;
    private String role;
    private String createdAt;

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }
    public String getSeccion() { return seccion; }
    public void setSeccion(String seccion) { this.seccion = seccion; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
    public String getCreatedAt() { return createdAt; }
    public void setCreatedAt(String createdAt) { this.createdAt = createdAt; }
}