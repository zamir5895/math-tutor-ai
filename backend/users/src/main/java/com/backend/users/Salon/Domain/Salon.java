package com.backend.users.Salon.Domain;

import com.backend.users.Profesor.Domain.Professor;
import com.backend.users.Student.Domain.Student;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Salon {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "secccion", nullable = false)
    private String seccion;

    @Column(name="grado", nullable = false)
    private Integer grado;

    @Column(name="turno", nullable = false)
    private String turno;

    @ManyToOne
    @JoinColumn(name="profesor_id", nullable = false)
    private Professor profesor;

    @OneToMany(mappedBy = "salon")
    private List<Student> students = new ArrayList<>();

}
