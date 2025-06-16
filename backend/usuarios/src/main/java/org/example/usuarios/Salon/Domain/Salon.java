package org.example.usuarios.Salon.Domain;

import jakarta.persistence.*;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.example.usuarios.Alumno.Domain.Alumno;
import java.util.*;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@Entity
public class Salon {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(nullable = false)
    private String seccion;

    @Column(nullable = false)
    private Integer grado;

    @Column(nullable = false, length = 100)
    private String nombre;

    @Column(nullable = false)
    private String turno;

    @Column(nullable = false, length = 100)
    private String descripcion;
    @Column(name = "profesor_id")
    private UUID profesorId;

    @OneToMany(mappedBy = "salon", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Alumno> alumnos = new ArrayList<>();
}