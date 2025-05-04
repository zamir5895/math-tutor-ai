package com.backend.users.Profesor.Domain;

import com.backend.users.Profesor.DTOs.DTOProfesor;
import com.backend.users.Profesor.Infrastructure.ProfessorRepository;
import com.backend.users.Security.Auth.DTOs.StudentDTO;
import com.backend.users.Security.Auth.DTOs.StudentRegister;
import com.backend.users.Student.Domain.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
public class ProfessorService {

    @Autowired
    private ProfessorRepository professorRepository;

    @Autowired
    private StudentService studentService;

    public DTOProfesor getProfessorProfile() {
        String email = SecurityContextHolder.getContext().getAuthentication().getName();
        return professorRepository.findByEmail(email)
                .map(professor -> {
                    DTOProfesor dtoProfesor = new DTOProfesor();
                    dtoProfesor.setId(professor.getId());
                    dtoProfesor.setNombre(professor.getFirstName());
                    dtoProfesor.setApellido(professor.getLastName());
                    dtoProfesor.setEmaill(professor.getEmail());
                    dtoProfesor.setEdad(professor.getEdad());
                    return dtoProfesor;
                })
                .orElseThrow(() -> new RuntimeException("Professor not found"));
    }

    public StudentDTO registerOneStudent(StudentRegister dto){
        return studentService.registerOneStudent(dto);
    }

    public void deleteStudent(Long id){
        studentService.deleteStudent(id);
    }
}
