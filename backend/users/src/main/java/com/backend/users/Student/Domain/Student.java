package com.backend.users.Student.Domain;

import com.backend.users.User.Domain.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@NoArgsConstructor
@Getter
@Setter
public class Student extends User {
    @Column(name="dni", unique = true, nullable = false)
    private Long dni;
    @Column(name="grado", nullable = false)
    private Integer grado;

    @Column(name ="seccion", nullable = false)
    private String seccion;
}
