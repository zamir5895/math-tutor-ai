package org.example.usuarios.Alumno.Application;

import org.example.usuarios.Alumno.DTOs.AlumnoRegisterRequestDTO;
import org.example.usuarios.Alumno.DTOs.AlumnoResponseDTO;
import org.example.usuarios.Alumno.Domain.Alumno;
import org.example.usuarios.Alumno.Domain.AlumnoService;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Salon.Domain.SalonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/alumno")
@CrossOrigin(origins = "*")
public class AlumnoController {

    @Autowired
    private AlumnoService alumnoService;

    @Autowired
    private SalonService salonService;

    @PostMapping("/register")
    public ResponseEntity<?> registerAlumno( @RequestBody AlumnoRegisterRequestDTO request) {
        try {
            // Verificar si el DNI ya existe
            if (alumnoService.existsByDni(request.getDni())) {
                return ResponseEntity.badRequest()
                        .body(new ApiResponseDTO("El DNI ya está registrado"));
            }

            // Crear nuevo alumno
            Alumno alumno = new Alumno();
            alumno.setUsername(request.getUsername());
            alumno.setPasswordHash(request.getPassword());
            alumno.setDni(request.getDni());

            Alumno savedAlumno = alumnoService.saveAlumno(alumno);

            // Crear response
            AlumnoResponseDTO response = new AlumnoResponseDTO();
            response.setId(savedAlumno.getId().toString());
            response.setUsername(savedAlumno.getUsername());
            response.setDni(savedAlumno.getDni());
            response.setRole("student");
            response.setCreatedAt(savedAlumno.getCreatedAt().toString());

            if (savedAlumno.getSalon() != null) {
                response.setSeccion(savedAlumno.getSalon().getSeccion());
            }

            return ResponseEntity.status(HttpStatus.CREATED).body(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @PostMapping("/register-bulk")
    public ResponseEntity<?> registerAlumnosBulk(@RequestParam("file") MultipartFile file) {
        try {
            if (file.isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(new ApiResponseDTO("El archivo está vacío"));
            }

            // TODO: Implementar procesamiento de CSV/Excel
            // Por ahora simulamos el registro de 25 alumnos
            int totalRegistrados = 25;

            return ResponseEntity.ok(new ApiResponseDTO("Alumnos registrados correctamente", totalRegistrados));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error procesando el archivo"));
        }
    }

    @GetMapping("/seccion/{id}")
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
                            dto.setSeccion(alumno.getSalon().getSeccion());
                        }
                        return dto;
                    })
                    .collect(Collectors.toList());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo alumnos"));
        }
    }
}
