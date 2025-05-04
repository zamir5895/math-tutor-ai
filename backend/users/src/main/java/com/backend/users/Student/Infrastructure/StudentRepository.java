package com.backend.users.Student.Infrastructure;

import com.backend.users.Student.Domain.Student;
import com.backend.users.User.Domain.User;
import com.backend.users.User.Infrastructure.UserRepository;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
@Transactional
public interface StudentRepository extends UserRepository<Student> {

    boolean existsStudentByDni(Long dni);
}
