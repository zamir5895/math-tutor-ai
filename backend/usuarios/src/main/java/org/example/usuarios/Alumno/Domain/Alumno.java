package org.example.usuarios.Alumno.Domain;


import jakarta.persistence.*;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.User.Domain.User;
import org.example.usuarios.User.Domain.Rol;

@Entity
@Table(name = "alumnos")
public class Alumno extends User {


    @Column(unique = true, nullable = false)
    private String dni;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "salon_id")
    private Salon salon;

    // Constructors
    public Alumno() {
        super();
        this.setRole(Rol.STUDENT);
    }

    public Alumno(String username, String passwordHash, String dni) {
        super(username, passwordHash, Rol.STUDENT);
        this.dni = dni;
    }

    // Getters and Setters
    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }

    public Salon getSalon() { return salon; }
    public void setSalon(Salon salon) { this.salon = salon; }

}
