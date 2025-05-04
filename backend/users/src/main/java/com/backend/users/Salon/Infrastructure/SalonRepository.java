package com.backend.users.Salon.Infrastructure;

import com.backend.users.Salon.Domain.Salon;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Transactional
@Repository
public interface SalonRepository extends JpaRepository<Salon, Long> {
    Optional<Salon> findById(Long id);
    @Query("SELECT s FROM Salon s JOIN s.students st WHERE st.id = :studentId")
    Optional<Salon> findByStudentId(@Param("studentId") Long studentId);

    @Query("SELECT s FROM Salon s JOIN s.profesor p WHERE p.id = :professorId")
    List<Salon> findByProfesorId(@Param("professorId") Long professorId);
}
