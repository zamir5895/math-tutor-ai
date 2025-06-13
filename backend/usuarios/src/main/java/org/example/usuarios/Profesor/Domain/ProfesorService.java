package org.example.usuarios.Profesor.Domain;

import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Profesor.DTOs.ProfesorRegisterRequestDTO;
import org.example.usuarios.Profesor.DTOs.ResponseProfesor;
import org.example.usuarios.Profesor.Infraestructure.ProfesorRepository;
import org.example.usuarios.User.Domain.Rol;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.ZonedDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ProfesorService {

    @Autowired
    private ProfesorRepository profesorRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public List<Profesor> getAllProfesores() {
        return profesorRepository.findAll();
    }

    public Optional<Profesor> getProfesorById(UUID id) {
        return profesorRepository.findById(id);
    }

    public Profesor saveProfesor(Profesor profesor) {
        profesor.setPasswordHash(passwordEncoder.encode(profesor.getPasswordHash()));
        return profesorRepository.save(profesor);
    }

    public ResponseProfesor guardarProfesor(ProfesorRegisterRequestDTO dto){
        String username = generateUsername(dto.getNombre(), dto.getApellido());
        if (existsByUsername(username)) {
            throw new IllegalArgumentException("El username ya está registrado");
        }
        Profesor profesor = new Profesor();
        profesor.setNombre(dto.getNombre());
        profesor.setApellido(dto.getApellido());
        profesor.setUsername(username);
        profesor.setTelefono(dto.getTelefono());
        profesor.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        profesor.setRole(Rol.TEACHER);
        profesor.setCreatedAt(ZonedDateTime.now());
        Profesor p =profesorRepository.save(profesor);
        return convertToResponse(p);
    }

    private ResponseProfesor convertToResponse(Profesor profesor) {
        ResponseProfesor response = new ResponseProfesor();
        response.setId(profesor.getId());
        response.setNombre(profesor.getNombre());
        response.setApellido(profesor.getApellido());
        response.setUsername(profesor.getUsername());
        response.setTelefono(profesor.getTelefono());
        return response;
    }

    private String generateUsername(String firstName, String lastName) {
        return (firstName + "." + lastName).toLowerCase();
    }

    public void deleteProfesor(UUID id) {
        profesorRepository.deleteById(id);
    }

    public Profesor updateProfesor(UUID id, Profesor profesorDetails) {
        Optional<Profesor> optionalProfesor = profesorRepository.findById(id);
        if (optionalProfesor.isPresent()) {
            Profesor profesor = optionalProfesor.get();
            profesor.setUsername(profesorDetails.getUsername());
            profesor.setTelefono(profesorDetails.getTelefono());
            if (profesorDetails.getPasswordHash() != null && !profesorDetails.getPasswordHash().isEmpty()) {
                profesor.setPasswordHash(passwordEncoder.encode(profesorDetails.getPasswordHash()));
            }
            return profesorRepository.save(profesor);
        }
        return null;
    }

    public boolean existsByUsername(String username) {
        return profesorRepository.existsByUsername(username);
    }

    public boolean existsById(UUID profesorId) {
        return profesorRepository.existsById(profesorId);
    }
}
