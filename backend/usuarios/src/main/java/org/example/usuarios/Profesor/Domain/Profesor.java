package org.example.usuarios.Profesor.Domain;

import jakarta.persistence.*;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.User.Domain.Rol;
import org.example.usuarios.User.Domain.User;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "profesores")
public class Profesor extends User {


    @Column(name = "telefono")
    private String telefono;

    public Profesor() {
        super();
        this.setRole(Rol.TEACHER);
    }

    public Profesor(String username, String passwordHash) {
        super(username, passwordHash, Rol.TEACHER);
    }

    public Profesor(String username, String passwordHash, String telefono) {
        super(username, passwordHash, Rol.TEACHER);
        this.telefono = telefono;
    }


    public String getTelefono() { return telefono; }
    public void setTelefono(String telefono) { this.telefono = telefono; }

}
