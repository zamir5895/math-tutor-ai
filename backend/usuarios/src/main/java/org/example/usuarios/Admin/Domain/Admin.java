package org.example.usuarios.Admin.Domain;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.User.Domain.User;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name = "admins")
public class Admin extends User {

}
