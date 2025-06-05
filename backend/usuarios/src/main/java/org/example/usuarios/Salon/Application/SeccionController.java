package org.example.usuarios.Salon.Application;

import org.example.usuarios.Alumno.DTOs.AlumnoResponseDTO;
import org.example.usuarios.Alumno.Domain.Alumno;
import org.example.usuarios.Alumno.Domain.AlumnoService;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Salon.Domain.SalonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/seccion")
@CrossOrigin(origins = "*")
public class SeccionController {

    @Autowired
    private AlumnoService alumnoService;

    @Autowired
    private SalonService salonService;

    @GetMapping("/alumnos/{id}")
    public ResponseEntity<?> getAlumnosBySeccion(@PathVariable UUID id) {
        try {
            List<Alumno> alumnos = alumnoService.getAlumnosBySalonId(id);

            List<AlumnoResponseDTO> response = alumnos.stream()
                    .map(alumno -> {
                        AlumnoResponseDTO dto = new AlumnoResponseDTO();
                        dto.setId(alumno.getId().toString());
                        dto.setUsername(alumno.getUsername());
                        dto.setDni(alumno.getDni());
                        if (alumno.getSalon() != null) {
                            dto.setSalon(alumno.getSalon().getId());
                        }
                        return dto;
                    })
                    .collect(Collectors.toList());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error obteniendo alumnos de la sección"));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteSeccion(@PathVariable UUID id) {
        try {
            if (!salonService.getSalonById(id).isPresent()) {
                return ResponseEntity.notFound().build();
            }

            salonService.deleteSalon(id);
            return ResponseEntity.ok(new ApiResponseDTO("Sección eliminada correctamente"));
        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error eliminando sección"));
        }
    }
}