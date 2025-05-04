package com.backend.users.Security.Auth.Service;


import com.backend.users.Kafka.KafkaProducer;
import com.backend.users.Kafka.UserFinishedEvent;
import com.backend.users.Kafka.UserRegisteredEvent;
import com.backend.users.Profesor.Domain.Professor;
import com.backend.users.Profesor.Infrastructure.ProfessorRepository;
import com.backend.users.Security.Auth.DTOs.*;
import com.backend.users.Security.JWT.JwtService;
import com.backend.users.Student.Domain.Student;
import com.backend.users.Student.Infrastructure.StudentRepository;
import com.backend.users.User.Domain.Rol;
import com.backend.users.User.Domain.User;
import com.backend.users.User.Infrastructure.UserRepository;
import com.opencsv.CSVWriter;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.RequestEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import com.opencsv.CSVReader;

import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class AuthService {

    private final StudentRepository studentRepository;
    private final PasswordEncoder passwordEncoder;
    private final ProfessorRepository professorRepository;
    private final UserRepository userRepository;
    private final JwtService jwtService;
    private final KafkaProducer kafkaProducer;


    public AuthService(StudentRepository studentRepository, PasswordEncoder passwordEncoder, ProfessorRepository professorRepository, @Qualifier("userRepository") UserRepository userRepository, JwtService jwtService, KafkaProducer kafkaProducer) {
        this.studentRepository = studentRepository;
        this.passwordEncoder = passwordEncoder;
        this.professorRepository = professorRepository;
        this.userRepository = userRepository;
        this.jwtService = jwtService;
        this.kafkaProducer = kafkaProducer;
    }

    public ByteArrayResource processRegisterForStuedents(MultipartFile file) throws Exception{
        List<String[]> result = new ArrayList<>();
        result.add(new String[]{"Nombre", "Apellido", "Usename", "Contraseña", "DNI", "Status", "Message"});
        try(CSVReader reader = new CSVReader(new InputStreamReader(file.getInputStream()))){
            String [] line;
            reader.readNext();
            while((line=reader.readNext()) != null){
                String nombre = line[0].trim();
                String apellido = line[1].trim();
                String dni = line[2].trim();
                String grado = line[3].trim();
                String seccion = line[4].trim();
                if(studentRepository.existsStudentByDni(Long.valueOf(dni))) {
                    result.add(new String[]{nombre, apellido, dni, grado, seccion, "Error", "El DNI ya existe, no puede repetirse los dnis"});
                }
                String userName = generateUsername(nombre,apellido, dni);
                String password = passwordEncoder.encode(dni);
                Student student = new Student();
                student.setDni(Long.valueOf(dni));
                student.setGrado(Integer.valueOf(grado));
                student.setSeccion(seccion);
                student.setEmail(userName);
                student.setFirstName(nombre);
                student.setLastName(apellido);
                student.setRole(Rol.STUDENT);
                student.setPassword(password);
                student.setCreatedAt(ZonedDateTime.now());
                studentRepository.save(student);
                result.add(new String[]{nombre, apellido, userName, password, dni, "Success", "El usuario se ha creado correctamente"});
            }

        }
        ByteArrayOutputStream b = new ByteArrayOutputStream();
        try (CSVWriter writer = new CSVWriter(new OutputStreamWriter(b))) {
            writer.writeAll(result);
        }
        ByteArrayResource resource = new ByteArrayResource(b.toByteArray());
        return resource;
    }


    public void registerProfessor(DtoRegister professor){
        Optional<User> optionalProfessor = professorRepository.findByEmail(professor.getCorreo());
        if(optionalProfessor.isPresent()){
            throw new RuntimeException("El profesor ya existe");
        }
        String password = passwordEncoder.encode(professor.getContraseña());
        Professor professorSave = new Professor();
        professorSave.setCreatedAt(ZonedDateTime.now());
        professorSave.setEmail(professor.getCorreo());
        professorSave.setUpdatedAt(ZonedDateTime.now());
        professorSave.setRole(Rol.TEACHER);
        professorSave.setFirstName(professor.getNombre());
        professorSave.setLastName(professor.getApellido());
        professorRepository.save(professorSave);
    }

    public void registerAdmin(DtoRegister register){
        Optional<User> optionalAdmin = userRepository.findByEmail(register.getCorreo());
        if(optionalAdmin.isPresent()){
            throw new RuntimeException("El admin ya existe");
        }
        String password = passwordEncoder.encode(register.getContraseña());
        User adminSave = new Professor();
        adminSave.setCreatedAt(ZonedDateTime.now());
        adminSave.setEmail(register.getCorreo());
        adminSave.setUpdatedAt(ZonedDateTime.now());
        adminSave.setRole(Rol.ADMIN);
        adminSave.setFirstName(register.getNombre());
        adminSave.setLastName(register.getApellido());
        userRepository.save(adminSave);
    }

    public ResponseLogin login(LoginRequest request){
        Optional<User> optionalUser = userRepository.findByEmail(request.getEmail());
        if(optionalUser.isEmpty()){
            throw new RuntimeException("El usuario no existe");
        }
        User user = optionalUser.get();
        if(!passwordEncoder.matches(request.getPassword(), user.getPassword())){
            throw new RuntimeException("La contraseña es incorrecta");
        }
        ResponseLogin login = new ResponseLogin();
        login.setToken(jwtService.generatetoken(user));
        login.setRol(String.valueOf(user.getRole()));
        UserRegisteredEvent userRegisteredEvent = new UserRegisteredEvent();
        userRegisteredEvent.setId(user.getId());
        userRegisteredEvent.setNombre(user.getFirstName());
        userRegisteredEvent.setApellido(user.getLastName());
        userRegisteredEvent.setGrado(String.valueOf(user.getRole()));
        userRegisteredEvent.setSeccion(user.getEmail());
        userRegisteredEvent.setEdad(user.getEdad());
        userRegisteredEvent.setFechaRegistro(ZonedDateTime.now());
        kafkaProducer.timeStartUsingTheApp(userRegisteredEvent);
        return login;
    }

    public void changePassword(String email, String password){
        Optional<User> optionalUser = userRepository.findByEmail(email);
        if(optionalUser.isEmpty()){
            throw new RuntimeException("El usuario no existe");
        }
        User user = optionalUser.get();
        String passwordEncode = passwordEncoder.encode(password);
        user.setPassword(passwordEncode);
        userRepository.save(user);
    }



    private String generateUsername(String name, String apellido, String dni){
        return name+apellido+dni.substring(0,3);
    }

    public void logout(String email){
        Optional<User> optionalUser = userRepository.findByEmail(email);
        if(optionalUser.isEmpty()){
            throw new RuntimeException("El usuario no existe");
        }
        User user = optionalUser.get();
        UserFinishedEvent userFinishedEvent = new UserFinishedEvent();
        userFinishedEvent.setId(user.getId());
        userFinishedEvent.setNombre(user.getFirstName());
        userFinishedEvent.setApellido(user.getLastName());
        userFinishedEvent.setGrado(String.valueOf(user.getRole()));
        userFinishedEvent.setSeccion(user.getEmail());
        userFinishedEvent.setEdad(user.getEdad());
        userFinishedEvent.setFechaSalida(ZonedDateTime.now());
        kafkaProducer.timeEndUsingTheApp(userFinishedEvent);

        jwtService.invalidateToken();
    }

    private Rol obtenerROlByToken(String token){
        String role = jwtService.extractRole(token);
        if(role.equals("STUDENT")){
            return Rol.STUDENT;
        }else if(role.equals("TEACHER")){
            return Rol.TEACHER;
        }else if(role.equals("ADMIN")){
            return Rol.ADMIN;
        }
        return null;
    }
    public String getEmailByToken(String token){
        return jwtService.extractUsername(token);
    }


    public StudentDTO registerOneStudent(StudentRegister register){
        Optional<User> optionalStudent = studentRepository.findByEmail(generateUsername(register.getNombre(), register.getApellido(), register.getDni()));
        if(optionalStudent.isPresent()){
            throw new RuntimeException("El estudiante ya existe");
        }

        Student studentSave = new Student();
        studentSave.setCreatedAt(ZonedDateTime.now());
        studentSave.setEmail(generateUsername(register.getNombre(), register.getApellido(), register.getDni()));
        studentSave.setUpdatedAt(ZonedDateTime.now());
        studentSave.setRole(Rol.STUDENT);
        studentSave.setFirstName(register.getNombre());
        studentSave.setLastName(register.getApellido());
        studentSave.setPassword(passwordEncoder.encode(register.getDni()));
        studentRepository.save(studentSave);
        return convertToStudentDTO(studentSave);
    }
    private StudentDTO convertToStudentDTO(Student student) {
        StudentDTO studentDTO = new StudentDTO();
        studentDTO.setNombre(student.getFirstName());
        studentDTO.setApellido(student.getLastName());
        studentDTO.setGrado(student.getGrado());
        studentDTO.setSeccion(student.getSeccion());
        return studentDTO;
    }



}
