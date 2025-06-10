package org.example.usuarios.Alumno.Domain;

import jakarta.persistence.*;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.User.Domain.User;
import org.example.usuarios.User.Domain.Rol;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "alumnos")
public class Alumno extends User {

    @Column(unique = true, nullable = false)
    private String dni;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "salon_id")
    private Salon salon;

    @ElementCollection
    @CollectionTable(name = "fechas_ejercicios_resueltos", joinColumns = @JoinColumn(name = "alumno_id"))
    @Column(name = "fecha")
    private List<LocalDate> fechasEjerciciosResueltos = new ArrayList<>();

    @Column(name = "horas_totales")
    private Integer minutosTotales = 0;

    @Column(name = "ultima_conexion")
    private LocalDateTime ultimaConexion;

    public Alumno() {
        super();
        this.setRole(Rol.STUDENT);
    }

    public Alumno(String username, String passwordHash, String dni) {
        super(username, passwordHash, Rol.STUDENT);
        this.dni = dni;
    }

    // Getters and Setters
    public String getDni() {
        return dni;
    }

    public void setDni(String dni) {
        this.dni = dni;
    }

    public Salon getSalon() {
        return salon;
    }

    public void setSalon(Salon salon) {
        this.salon = salon;
    }

    public List<LocalDate> getFechasEjerciciosResueltos() {
        return fechasEjerciciosResueltos;
    }

    public void setFechasEjerciciosResueltos(List<LocalDate> fechasEjerciciosResueltos) {
        this.fechasEjerciciosResueltos = fechasEjerciciosResueltos;
    }

    public Integer getMinutosTotales() {
        return minutosTotales;
    }

    public void setMinutosTotales(Integer minutosTotales) {
        this.minutosTotales= minutosTotales;
    }

    public LocalDateTime getUltimaConexion() {
        return ultimaConexion;
    }

    public void setUltimaConexion(LocalDateTime ultimaConexion) {
        this.ultimaConexion = ultimaConexion;
    }

    public void agregarFechaEjercicioResuelto(LocalDate fecha) {
        if (this.fechasEjerciciosResueltos == null) {
            this.fechasEjerciciosResueltos = new ArrayList<>();
        }
        this.fechasEjerciciosResueltos.add(fecha);
    }
}