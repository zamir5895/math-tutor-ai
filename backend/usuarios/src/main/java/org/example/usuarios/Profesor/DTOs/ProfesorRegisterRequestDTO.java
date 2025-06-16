package org.example.usuarios.Profesor.DTOs;

public class ProfesorRegisterRequestDTO {

    private String password;

    private String especialidad;
    private String telefono;
    private String role = "teacher";

    private String nombre;
    private String apellido;

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getEspecialidad() { return especialidad; }
    public void setEspecialidad(String especialidad) { this.especialidad = especialidad; }
    public String getTelefono() { return telefono; }
    public void setTelefono(String telefono) { this.telefono = telefono; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    public String getApellido() { return apellido; }
    public void setApellido(String apellido) { this.apellido = apellido; }
}