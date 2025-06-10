package org.example.usuarios.Salon.Domain;

import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Profesor.Domain.ProfesorService;
import org.example.usuarios.Salon.DTOs.SalonRequestDTO;
import org.example.usuarios.Salon.DTOs.SalonResponse;
import org.example.usuarios.Salon.Infraestructure.SalonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class SalonService {

    @Autowired
    private SalonRepository salonRepository;

    @Autowired
    private ProfesorService profesorService;
    @Autowired
    private JwtTokenProvider jwtTokenProvider;


    public List<Salon> getSalonesByGrado(Integer grado) {
        return salonRepository.findByGrado(grado);
    }

    public List<Salon> getSalonesByTurno(String turno) {
        return salonRepository.findByTurno(turno);
    }

    public List<Salon> getSalonesByGradoAndSeccion(Integer grado, String seccion) {
        return salonRepository.findByGradoAndSeccion(grado, seccion);
    }

    public Salon saveSalon(Salon salon) {
        return salonRepository.save(salon);
    }

    public void deleteSalon(UUID id) {
        salonRepository.deleteById(id);
    }

    public Salon updateSalon(UUID id, Salon salonDetails) {
        Optional<Salon> optionalSalon = salonRepository.findById(id);
        if (optionalSalon.isPresent()) {
            Salon salon = optionalSalon.get();

            salon.setSeccion(salonDetails.getSeccion());
            salon.setGrado(salonDetails.getGrado());
            salon.setTurno(salonDetails.getTurno());
            salon.setProfesorId(salonDetails.getProfesorId());



            return salonRepository.save(salon);
        }
        return null;
    }

    public SalonResponse createSalon(SalonRequestDTO request, String token) {

        validateToken(token);
        UUID profesorId;

        if ("ADMIN".equals(role)) {
            if (request.getProfesorId() == null) {
                throw new IllegalArgumentException("Falta el ID del profesor");
            }

            profesorId = request.getProfesorId();

            if (!profesorService.existsById(profesorId)) {
                throw new IllegalArgumentException("El profesor con el ID proporcionado no existe");
            }

        } else if ("TEACHER".equals(role)) {
            profesorId = jwtTokenProvider.extractUserId(jwt);
        } else {
            throw new SecurityException("No tienes permisos para crear un salón");
        }

        Salon salon = new Salon();
        salon.setSeccion(request.getSeccion());
        salon.setGrado(request.getGrado());
        salon.setTurno(request.getTurno());
        salon.setProfesorId(profesorId);
        salon.setDescripcion(request.getDesccripcion());
        Salon savedSalon = salonRepository.save(salon);
        SalonResponse response = new SalonResponse();
        response.setId(savedSalon.getId());
        response.setSeccion(savedSalon.getSeccion());
        response.setGrado(savedSalon.getGrado());
        response.setTurno(savedSalon.getTurno());
        response.setDescripcion(savedSalon.getDescripcion());
        response.setCantidadAlumnos(savedSalon.getAlumnos().size());
        return response;
    }
    public List<Salon> getMySalonsAsProfesor(String token) {
        validateToken(token);
        String jwt = token.substring(7);
        UUID profesorId = jwtTokenProvider.extractUserId(jwt);
        if (profesorId == null) {
            throw new IllegalArgumentException("Token inválido o expirado");
        }
        return salonRepository.findByProfesorId(profesorId);
    }



    public Salon updateSalon(UUID id, SalonRequestDTO request, String token) {
        validateToken(token);
        String jwt = token.substring(7);
        UUID profesorId = jwtTokenProvider.extractUserId(jwt);
        if (profesorId == null) {
            throw new IllegalArgumentException("Token inválido o expirado");
        }
        String role = jwtTokenProvider.extractRole(jwt);

        Salon salon = salonRepository.findById(id).orElseThrow(() ->
                new IllegalArgumentException("Salón no encontrado"));

        if (!role.equals("ADMIN") && !salon.getProfesorId().equals(profesorId)) {
            throw new SecurityException("No tienes permisos para actualizar este salón");
        }

        salon.setSeccion(request.getSeccion());
        salon.setGrado(request.getGrado());
        salon.setTurno(request.getTurno());
        salon.setProfesorId(request.getProfesorId());
        return salonRepository.save(salon);
    }

    public void deleteSalon(UUID id, String token) {
        validateToken(token);
        String jwt = token.substring(7);
        UUID profesorId = jwtTokenProvider.extractUserId(jwt);
        if (profesorId == null) {
            throw new IllegalArgumentException("Token inválido o expirado");
        }
        String role = jwtTokenProvider.extractRole(jwt);

        Salon salon = salonRepository.findById(id).orElseThrow(() ->
                new IllegalArgumentException("Salón no encontrado"));

        if (!role.equals("ADMIN") && !salon.getProfesorId().equals(profesorId)) {
            throw new SecurityException("No tienes permisos para eliminar este salón");
        }

        salonRepository.deleteById(id);
    }

    private void validateToken(String token) {
        if (token == null || !token.startsWith("Bearer ")) {
            throw new IllegalArgumentException("Token de autorización requerido o inválido");
        }
    }


}