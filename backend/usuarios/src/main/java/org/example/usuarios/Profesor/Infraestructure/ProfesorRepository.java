package org.example.usuarios.Profesor.Infraestructure;

import org.example.usuarios.Profesor.Domain.Profesor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ProfesorRepository extends JpaRepository<Profesor, UUID> {

}
