package org.example.usuarios.Alumno.Infraestructure;

import org.example.usuarios.Alumno.Domain.Alumno;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface AlumnoRepository extends JpaRepository<Alumno, UUID> {
    Optional<Alumno> findByDni(String dni);
    boolean existsByDni(String dni);

    @Query("SELECT a FROM Alumno a WHERE a.salon.id = :salonId")
    List<Alumno> findBySalonId(@Param("salonId") UUID salonId);

    @Query("SELECT a FROM Alumno a WHERE a.salon.seccion = :seccion")
    List<Alumno> findBySeccion(@Param("seccion") String seccion);
}