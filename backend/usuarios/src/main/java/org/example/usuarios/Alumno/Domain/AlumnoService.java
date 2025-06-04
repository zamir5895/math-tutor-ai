package org.example.usuarios.Alumno.Domain;

import org.example.usuarios.Alumno.Infraestructure.AlumnoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class AlumnoService {

    @Autowired
    private AlumnoRepository alumnoRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public List<Alumno> getAllAlumnos() {
        return alumnoRepository.findAll();
    }

    public Optional<Alumno> getAlumnoById(UUID id) {
        return alumnoRepository.findById(id);
    }

    public Optional<Alumno> getAlumnoByDni(String dni) {
        return alumnoRepository.findByDni(dni);
    }

    public List<Alumno> getAlumnosBySalonId(UUID salonId) {
        return alumnoRepository.findBySalonId(salonId);
    }

    public List<Alumno> getAlumnosBySeccion(String seccion) {
        return alumnoRepository.findBySeccion(seccion);
    }

    public Alumno saveAlumno(Alumno alumno) {
        alumno.setPasswordHash(passwordEncoder.encode(alumno.getPasswordHash()));
        return alumnoRepository.save(alumno);
    }

    public boolean existsByDni(String dni) {
        return alumnoRepository.existsByDni(dni);
    }

    public void deleteAlumno(UUID id) {
        alumnoRepository.deleteById(id);
    }

    public Alumno updateAlumno(UUID id, Alumno alumnoDetails) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(id);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            alumno.setUsername(alumnoDetails.getUsername());
            alumno.setDni(alumnoDetails.getDni());
            if (alumnoDetails.getPasswordHash() != null && !alumnoDetails.getPasswordHash().isEmpty()) {
                alumno.setPasswordHash(passwordEncoder.encode(alumnoDetails.getPasswordHash()));
            }
            return alumnoRepository.save(alumno);
        }
        return null;
    }
}