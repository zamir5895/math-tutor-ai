package com.backend.users.Profesor.Domain;


import com.backend.users.Salon.Domain.Salon;
import com.backend.users.User.Domain.User;
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
public class Professor extends User {

    @OneToMany(mappedBy = "profesor")
    private List<Salon> salons = new ArrayList<>();
}
