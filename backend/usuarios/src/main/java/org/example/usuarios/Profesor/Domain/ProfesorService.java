package org.example.usuarios.Profesor.Domain;

import org.example.usuarios.Profesor.Infraestructure.ProfesorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

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
}
