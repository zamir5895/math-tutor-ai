package org.example.usuarios.Salon.Domain;

import org.example.usuarios.Alumno.DTOs.AlumnosDTO;
import org.example.usuarios.Alumno.Domain.Alumno;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Profesor.Domain.ProfesorService;
import org.example.usuarios.Salon.DTOs.SalonInfo;
import org.example.usuarios.Salon.DTOs.SalonRequestDTO;
import org.example.usuarios.Salon.DTOs.SalonResponse;
import org.example.usuarios.Salon.Infraestructure.SalonRepository;
import org.springframework.beans.factory.annotation.Autowired;
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

        String jwt = token.startsWith("Bearer ") ? token.substring(7) : token;
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
        response.setNombre(salon.getNombre());
        return response;
    }

    public List<SalonResponse> searchSalonsByName(String name, String token) {
        validateToken(token);
        String jwt = token.startsWith("Bearer ") ? token.substring(7) : token;
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
        String jwt = token.startsWith("Bearer ") ? token.substring(7) : token;
        System.out.println("Estamos aca");
        String role = jwtTokenProvider.extractRole(jwt);
        System.out.println("EL rol es: " + role);
        UUID profesorId = jwtTokenProvider.extractUserId(jwt);
        System.out.println("Estamos aca");
        if ("ADMIN".equals(role)) {
            System.out.println("Acaaa " +profesorId);
            if (profesorId == null) {
                throw new IllegalArgumentException("Falta el ID del profesor");
            }
            if (!profesorService.existsById(profesorId)) {
                throw new IllegalArgumentException("El profesor con el ID proporcionado no existe");
            }
            System.out.println(profesorId);
        } else if ("TEACHER".equals(role)) {
            System.out.println("Acaaa " +profesorId);

            profesorId = jwtTokenProvider.extractUserId(jwt);
        } else {
            throw new SecurityException("No tienes permisos para crear un salón");
        }
        System.out.println(request);
        if (request.getSeccion() == null || request.getGrado() == null || request.getTurno() == null) {
            throw new IllegalArgumentException("Sección, grado y turno son obligatorios");
        }

        Salon salon = new Salon();
        salon.setSeccion(request.getSeccion());
        salon.setGrado(request.getGrado());
        salon.setTurno(request.getTurno() != null ? request.getTurno() : "Mañana");
        salon.setProfesorId(profesorId);
        salon.setDescripcion(request.getDescripcion() != null ? request.getDescripcion() : "Sin descripción");
        salon.setNombre(request.getNombre() != null ? request.getNombre() : "Sin nombre");
        try {
            Salon savedSalon = salonRepository.save(salon);

            SalonResponse response = new SalonResponse();
            response.setId(savedSalon.getId());
            response.setSeccion(savedSalon.getSeccion());
            response.setGrado(savedSalon.getGrado());
            response.setTurno(savedSalon.getTurno());
            response.setDescripcion(savedSalon.getDescripcion());
            response.setCantidadAlumnos(savedSalon.getAlumnos().size());
            response.setNombre(savedSalon.getNombre());

            return response;
        } catch (Exception e) {
            System.err.println("Error saving salon: " + e.getMessage());
            throw new RuntimeException("Error al guardar el salón", e);
        }
    }


    public SalonResponse updateSalon(UUID id, SalonRequestDTO request, String token) {
        validateToken(token);
        String jwt = token.startsWith("Bearer ") ? token.substring(7) : token;
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
        String jwt = token.startsWith("Bearer ") ? token.substring(7) : token;
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
        if (token == null ) {
            throw new IllegalArgumentException("Token de autorización requerido o inválido");
        }
    }


    public SalonResponse getInfoBySalonId(UUID salonID, UUID profesorID) {
        Salon salon = salonRepository.findById(salonID).orElseThrow(() ->
                new IllegalArgumentException("Salón no encontrado"));
        if (!salon.getProfesorId().equals(profesorID)) {
            throw new SecurityException("No tienes permisos para acceder a la información de este salón");
        }
        SalonResponse salonIndo = new SalonResponse();
        salonIndo.setId(salon.getId());
        salonIndo.setSeccion(salon.getSeccion());
        salonIndo.setNombre(salon.getNombre());
        salonIndo.setGrado(salon.getGrado());
        salonIndo.setTurno(salon.getTurno());
        salonIndo.setDescripcion(salon.getDescripcion());
        salonIndo.setCantidadAlumnos(salon.getAlumnos().size());
        for(Alumno a: salon.getAlumnos()){
            salonIndo.getAlumnosIds().add(a.getId());
        }

        return salonIndo;
    }

    public List<AlumnosDTO> obtenerAlumnosRegistradosRecientemente(UUID salonId, UUID profesorId) {
        Salon salon = salonRepository.findById(salonId).orElseThrow(() ->
                new IllegalArgumentException("Salón no encontrado"));
        if (!salon.getProfesorId().equals(profesorId)) {
            throw new SecurityException("No tienes permisos para acceder a los alumnos de este salón");
        }
        List<AlumnosDTO> alumnosDTOList = new ArrayList<>();
        for (Alumno alumno : salon.getAlumnos()) {
            AlumnosDTO dto = new AlumnosDTO();
            dto.setId(alumno.getId());
            dto.setNombre(alumno.getNombre());
            dto.setApellido(alumno.getApellido());
            dto.setUsername(alumno.getUsername());
            dto.setDni(alumno.getDni());
            alumnosDTOList.add(dto);
        }
        return alumnosDTOList;
    }

    public SalonInfo getInfoOfSalonByprofesorId(UUID profesorId){
        List<Salon> s =  salonRepository.findByProfesorId(profesorId);
        if(s.isEmpty()){
            return null;
        }
        SalonInfo salonInfo = new SalonInfo();
        Integer cantidadAlumnos = 0;
        for(Salon salon : s){
            SalonResponse response = getInfoBySalonId(salon.getId(), salon.getProfesorId());
            cantidadAlumnos+=response.getCantidadAlumnos();
            salonInfo.getSalonIds().add(response.getId());
        }
        salonInfo.setCantidadAlumnos(cantidadAlumnos);
        return salonInfo;

    }



}