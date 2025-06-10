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

import java.util.ArrayList;
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

    public List<Salon> getAllSalones() {
        return salonRepository.findAll();
    }

    public Optional<Salon> getSalonById(UUID id) {
        return salonRepository.findById(id);
    }

    public List<SalonResponse> getSalonesByProfesorId(String token) {
        validateToken(token);

        String jwt = token.substring(7);
        UUID profesorId = jwtTokenProvider.extractUserId(jwt);
        String role = jwtTokenProvider.extractRole(jwt);
        if(!role.equals("TEACHER")){
            throw new SecurityException("No tienes permisos para acceder a los salones de un profesor");
        }
        if (profesorId == null) {
            throw new IllegalArgumentException("Token inválido o expirado");
        }

        List<Salon> s =  salonRepository.findByProfesorId(profesorId);
        if(s.isEmpty()){
            return new ArrayList<>();
        }
        List<SalonResponse> responses = new ArrayList<>();
        for (Salon salon : s) {
            SalonResponse response = convertToResponse(salon);
            responses.add(response);
        }
        return responses;
    }

   private SalonResponse convertToResponse(Salon salon) {
        SalonResponse response = new SalonResponse();
        response.setId(salon.getId());
        response.setSeccion(salon.getSeccion());
        response.setGrado(salon.getGrado());
        response.setTurno(salon.getTurno());
        response.setDescripcion(salon.getDescripcion());
        response.setCantidadAlumnos(salon.getAlumnos().size());
        return response;
    }

    public List<SalonResponse> searchSalonsByName(String name, String token) {
        validateToken(token);
        String jwt = token.substring(7);
        UUID profesorId = jwtTokenProvider.extractUserId(jwt);
        String role = jwtTokenProvider.extractRole(jwt);

        if (!role.equals("ADMIN") && !role.equals("TEACHER")) {
            throw new SecurityException("No tienes permisos para buscar salones");
        }

        List<Salon> salones = salonRepository.findByNombreIgnoreCase(name);
        List<SalonResponse> responses = new ArrayList<>();
        for (Salon salon : salones) {
            SalonResponse response = convertToResponse(salon);
            responses.add(response);
        }
        return responses;
    }

    public void deleteSalon(UUID id) {
        salonRepository.deleteById(id);
    }



    public SalonResponse createSalon(SalonRequestDTO request, String token) {
        validateToken(token);
        String jwt = token.substring(7);

        String role = jwtTokenProvider.extractRole(jwt);

        UUID profesorId=jwtTokenProvider.extractUserId(jwt);

        if ("ADMIN".equals(role)) {
            if (profesorId== null) {
                throw new IllegalArgumentException("Falta el ID del profesor");
            }
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



    public SalonResponse updateSalon(UUID id, SalonRequestDTO request, String token) {
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
        salon.setProfesorId(profesorId);
        Salon s = salonRepository.save(salon);
        return convertToResponse(s);
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