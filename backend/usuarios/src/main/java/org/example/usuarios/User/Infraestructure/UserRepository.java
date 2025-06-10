package org.example.usuarios.User.Infraestructure;

import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.User.Domain.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserRepository extends JpaRepository<User, UUID> {
    Optional<User> findByUsername(String username);
    boolean existsByUsername(String username);


    @Query("SELECT s FROM Salon s WHERE LOWER(s.nombre) LIKE LOWER(CONCAT('%', :nombre, '%'))")
    List<Salon> findByNombreIgnoreCase(@Param("nombre") String nombre);

}
