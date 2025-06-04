package org.example.usuarios.Alumno.DTOs;

public class AlumnoRegisterRequestDTO {
    private String username;

    private String password;

    private String dni;

    private String seccion;
    private String role = "student";

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }
    public String getSeccion() { return seccion; }
    public void setSeccion(String seccion) { this.seccion = seccion; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
}
