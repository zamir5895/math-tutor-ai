package com.backend.users.Security.Auth.Service;


import com.backend.users.Profesor.Domain.Professor;
import com.backend.users.Profesor.Infrastructure.ProfessorRepository;
import com.backend.users.Security.Auth.DTOs.DtoRegister;
import com.backend.users.Security.Auth.DTOs.LoginRequest;
import com.backend.users.Security.Auth.DTOs.ResponseLogin;
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


    public AuthService(StudentRepository studentRepository, PasswordEncoder passwordEncoder, ProfessorRepository professorRepository, @Qualifier("userRepository") UserRepository userRepository, JwtService jwtService) {
        this.studentRepository = studentRepository;
        this.passwordEncoder = passwordEncoder;
        this.professorRepository = professorRepository;
        this.userRepository = userRepository;
        this.jwtService = jwtService;
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


}
