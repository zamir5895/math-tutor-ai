package org.example.usuarios.Profesor.DTOs;

public class ProfesorRegisterRequestDTO {
    private String username;

    private String password;

    private String especialidad;
    private String telefono;
    private String role = "teacher";

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getEspecialidad() { return especialidad; }
    public void setEspecialidad(String especialidad) { this.especialidad = especialidad; }
    public String getTelefono() { return telefono; }
    public void setTelefono(String telefono) { this.telefono = telefono; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
}