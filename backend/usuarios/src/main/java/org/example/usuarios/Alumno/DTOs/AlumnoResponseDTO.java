package org.example.usuarios.Alumno.DTOs;

import java.util.UUID;

public class AlumnoResponseDTO {
    private String id;
    private String username;
    private String dni;
    private UUID salon;
    private String role;
    private String createdAt;

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }
    public UUID getSalon() { return salon; }
    public void setSalon(UUID seccion) { this.salon = seccion; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
    public String getCreatedAt() { return createdAt; }
    public void setCreatedAt(String createdAt) { this.createdAt = createdAt; }
}