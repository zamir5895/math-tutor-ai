package org.example.usuarios.Salon.Domain;

import jakarta.persistence.*;
import jakarta.persistence.*;
import org.example.usuarios.Alumno.Domain.Alumno;
import java.util.*;
import java.util.UUID;

@Entity
public class Salon {


    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(nullable = false)
    private String seccion;

    @Column(nullable = false)
    private String grado;

    @Column(nullable = false)
    private String turno;

    @Column(name = "profesor_id")
    private UUID profesorId;

    @OneToMany(mappedBy = "salon", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Alumno> alumnos;

    @ElementCollection
    private List<UUID> alumnoIds = new ArrayList<>();

    // Constructors
    public Salon() {}

    public Salon(String seccion, String grado, String turno, UUID profesorId) {
        this.seccion = seccion;
        this.grado = grado;
        this.turno = turno;
        this.profesorId = profesorId;
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getSeccion() { return seccion; }
    public void setSeccion(String seccion) { this.seccion = seccion; }

    public String getGrado() { return grado; }
    public void setGrado(String grado) { this.grado = grado; }

    public String getTurno() { return turno; }
    public void setTurno(String turno) { this.turno = turno; }

    public UUID getProfesorId() { return profesorId; }
    public void setProfesorId(UUID profesorId) { this.profesorId = profesorId; }

    public List<Alumno> getAlumnos() { return alumnos; }
    public void setAlumnos(List<Alumno> alumnos) { this.alumnos = alumnos; }

    public List<UUID> getAlumnoIds() { return alumnoIds; }
    public void setAlumnoIds(List<UUID> alumnoIds) { this.alumnoIds = alumnoIds; }


}
