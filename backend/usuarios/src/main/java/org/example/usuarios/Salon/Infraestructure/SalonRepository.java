package org.example.usuarios.Salon.Infraestructure;

import org.example.usuarios.Salon.Domain.Salon;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface SalonRepository extends JpaRepository<Salon, UUID> {

    @Query("SELECT s FROM Salon s WHERE s.profesorId = :profesorId")
    List<Salon> findByProfesorId(@Param("profesorId") UUID profesorId);

    List<Salon> findByGrado(String grado);
    List<Salon> findByTurno(String turno);

    @Query("SELECT s FROM Salon s WHERE s.grado = :grado AND s.seccion = :seccion")
    List<Salon> findByGradoAndSeccion(@Param("grado") String grado, @Param("seccion") String seccion);
}

