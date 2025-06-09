package org.example.usuarios.Salon.DTOs;

import java.util.UUID;
import java.util.List;


public class SalonRequestDTO {
    private String seccion;

    private String grado;

    private String turno;

    private UUID profesorId;

    private List<UUID> alumnoIds;

    public List<UUID> getAlumnoIds() { return alumnoIds; }
    public void setAlumnoIds(List<UUID> alumnoIds) { this.alumnoIds = alumnoIds; }

    public String getSeccion() { return seccion; }
    public void setSeccion(String seccion) { this.seccion = seccion; }
    public String getGrado() { return grado; }
    public void setGrado(String grado) { this.grado = grado; }
    public String getTurno() { return turno; }
    public void setTurno(String turno) { this.turno = turno; }
    public UUID getProfesorId() { return profesorId; }
    public void setProfesorId(UUID profesorId) { this.profesorId = profesorId; }
}