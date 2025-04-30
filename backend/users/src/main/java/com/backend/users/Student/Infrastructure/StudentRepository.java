package com.backend.users.Student.Infrastructure;

import com.backend.users.Student.Domain.Student;
import com.backend.users.User.Infrastructure.UserRepository;

public interface StudentRepository extends UserRepository<Student> {

    boolean existsStudentByDni(Long dni);
}
