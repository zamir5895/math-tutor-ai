package com.backend.users.Security.Auth.Service;


import com.backend.users.Security.Auth.DTOs.DtoProfessor;
import com.backend.users.Student.Domain.Student;
import com.backend.users.Student.Infrastructure.StudentRepository;
import com.backend.users.User.Domain.Rol;
import com.opencsv.CSVWriter;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import com.opencsv.CSVReader;

import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class AuthService {

    private final StudentRepository studentRepository;
    private final PasswordEncoder passwordEncoder;



    public AuthService(StudentRepository studentRepository, PasswordEncoder passwordEncoder) {
        this.studentRepository = studentRepository;
        this.passwordEncoder = passwordEncoder;
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


    public void registerProfessor(DtoProfessor professor){


    }

    private String generateUsername(String name, String apellido, String dni){
        return name+apellido+dni.substring(0,3);
    }
}
