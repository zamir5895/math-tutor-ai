package com.backend.users.Student.Domain;


import com.backend.users.Salon.Domain.Salon;
import com.backend.users.Salon.Infrastructure.SalonRepository;
import com.backend.users.Security.Auth.DTOs.StudentDTO;
import com.backend.users.Security.Auth.DTOs.StudentRegister;
import com.backend.users.Security.Auth.Service.AuthService;
import com.backend.users.Security.JWT.JwtService;
import com.backend.users.Student.DTOs.DTOStudentProfile;
import com.backend.users.Student.Infrastructure.StudentRepository;
import com.backend.users.User.Domain.Rol;
import com.backend.users.User.Domain.User;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.ZonedDateTime;
import java.util.Optional;

@Service
public class StudentService {


    private final StudentRepository studentRepository;
    private final AuthService authService;
    private final PasswordEncoder passwordEncoder;
    private final SalonRepository salonRepository;
    private final JwtService jwtService;

    public StudentService(StudentRepository studentRepository, AuthService authService, PasswordEncoder passwordEncoder, SalonRepository salonRepository, JwtService jwtService) {
        this.studentRepository = studentRepository;
        this.authService = authService;
        this.passwordEncoder = passwordEncoder;
        this.salonRepository = salonRepository;
        this.jwtService = jwtService;
    }

    public StudentDTO registerOneStudent(StudentRegister register){
        Optional<Student> optionalStudent = studentRepository.findByEmail(authService.generateUsername(register.getNombre(), register.getApellido(), register.getDni()));
        if(optionalStudent.isPresent()){
            throw new RuntimeException("El estudiante ya existe");
        }
        if(studentRepository.existsStudentByDni(Long.valueOf(register.getDni()))){
            throw new RuntimeException("El estudiante ya existe");
        }
        Student studentSave = new Student();
        studentSave.setCreatedAt(ZonedDateTime.now());
        studentSave.setEmail(authService.generateUsername(register.getNombre(), register.getApellido(), register.getDni()));
        studentSave.setUpdatedAt(ZonedDateTime.now());
        studentSave.setRole(Rol.STUDENT);
        studentSave.setFirstName(register.getNombre());
        studentSave.setLastName(register.getApellido());
        studentSave.setPassword(passwordEncoder.encode(register.getDni()));
        Salon salon = salonRepository.findById(register.getSalonId()).orElseThrow(()-> new EntityNotFoundException("Salon no encontrado"));
        studentSave.setSalon(salon);
        studentRepository.save(studentSave);
        return convertToStudentDTO(studentSave);
    }
    private StudentDTO convertToStudentDTO(Student student) {
        StudentDTO studentDTO = new StudentDTO();
        studentDTO.setNombre(student.getFirstName());
        studentDTO.setApellido(student.getLastName());
        Salon salon = salonRepository.findByStudentId(student.getId()).orElseThrow(()-> new EntityNotFoundException("Salon no encontrado"));
        studentDTO.setGrado(salon.getGrado());
        studentDTO.setSeccion(salon.getSeccion());
        return studentDTO;
    }
    public void deleteStudent(Long id){
        Optional<Student> optionalStudent = studentRepository.findById(id);
        if(optionalStudent.isEmpty()){
            throw new RuntimeException("El estudiante no existe");
        }
        Student student = optionalStudent.get();
        studentRepository.delete(student);
    }

    public DTOStudentProfile getStudentProfile() {
        String email = SecurityContextHolder.getContext().getAuthentication().getName();
        Optional<Student> st = studentRepository.findByEmail(email);
        if (st.isEmpty()) {
            throw new RuntimeException("El estudiante no existe");
        }
        Student student = st.get();
        DTOStudentProfile dtoStudentProfile = new DTOStudentProfile();
        dtoStudentProfile.setId(student.getId());
        dtoStudentProfile.setEdad(student.getEdad());
        dtoStudentProfile.setName(student.getFirstName());
        dtoStudentProfile.setApellido(student.getLastName());
        Salon salon = salonRepository.findByStudentId(student.getId()).orElseThrow(() -> new EntityNotFoundException("Salon no encontrado"));
        dtoStudentProfile.setSalon(salon.getGrado());
        dtoStudentProfile.setSeccion(salon.getSeccion());
        return dtoStudentProfile;
    }
}
