package org.example.usuarios.Alumno.Application;

import org.example.usuarios.Alumno.DTOs.AlumnoProfileResponseDTO;
import org.example.usuarios.Alumno.DTOs.AlumnoRegisterRequestDTO;
import org.example.usuarios.Alumno.DTOs.AlumnoResponseDTO;
import org.example.usuarios.Alumno.Domain.Alumno;
import org.example.usuarios.Alumno.Domain.AlumnoService;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.Salon.Domain.SalonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Optional;
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


    @Autowired
    private JwtTokenProvider jwtTokenProvider;

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
                response.setSalon(savedAlumno.getSalon().getId());
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

            //TODO: Implementar procesamiento de CSV/Excel
            // Por ahora simulamos el registro de 25 alumnos
            int totalRegistrados = 25;

            return ResponseEntity.ok(new ApiResponseDTO("Alumnos registrados correctamente", totalRegistrados));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error procesando el archivo"));
        }
    }

    @GetMapping("/admin_only/all")
    public ResponseEntity<?> getAllAlumnos() {
        try {
            // Obtener todos los alumnos
            List<Alumno> alumnos = alumnoService.getAllAlumnos();

            // Crear la respuesta con los detalles de los alumnos
            List<AlumnoResponseDTO> response = alumnos.stream()
                    .map(alumno -> {
                        AlumnoResponseDTO dto = new AlumnoResponseDTO();
                        dto.setId(alumno.getId().toString());
                        dto.setUsername(alumno.getUsername());
                        dto.setDni(alumno.getDni());
                        dto.setRole(alumno.getRole().toString());
                        dto.setCreatedAt(alumno.getCreatedAt().toString());

                        if (alumno.getSalon() != null) {
                            dto.setSalon(alumno.getSalon().getId());
                        }
                        return dto;
                    })
                    .collect(Collectors.toList());

            return ResponseEntity.ok(response); // Devuelve la lista de alumnos en formato JSON

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo la lista de alumnos"));
        }
    }

    @GetMapping("/student/profile")
    public ResponseEntity<?> getProfile(@RequestHeader("Authorization") String authorizationHeader) {
        try {
            // Obtener el token de la cabecera "Authorization"
            String token = authorizationHeader.substring(7); // "Bearer " es el prefijo, por lo que eliminamos los primeros 7 caracteres

            // Extraer el userId del token
            UUID userId = jwtTokenProvider.extractUserId(token);

            // Buscar el alumno por su ID
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(userId);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();

                // Crear un objeto de respuesta con el perfil del alumno
                AlumnoProfileResponseDTO response = new AlumnoProfileResponseDTO();
                response.setId(alumno.getId().toString()); // Convertimos el UUID a String
                response.setUsername(alumno.getUsername());

                return ResponseEntity.ok(response); // Devuelves la respuesta con el perfil del alumno
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo el perfil"));
        }
    }

    @GetMapping("/student/salon")
    public ResponseEntity<?> getSalonByToken(@RequestHeader("Authorization") String authorizationHeader) {
        try {
            String token = authorizationHeader.substring(7);

            UUID userId = jwtTokenProvider.extractUserId(token);

            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(userId);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                Salon salon = alumno.getSalon();

                if (salon != null) {
                    return ResponseEntity.ok(salon);
                } else {
                    return ResponseEntity.status(HttpStatus.NOT_FOUND)
                            .body(new ApiResponseDTO("El alumno no tiene un salón asignado"));
                }
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo el salón"));
        }
    }

    @GetMapping("/salon/{id}")
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
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo alumnos"));
        }
    }

    @PutMapping("/admin_only/{id}")
    public ResponseEntity<?> updateAlumno(@PathVariable UUID id, @RequestBody Alumno alumnoDetails) {
        try {
            // Buscar el alumno por su ID
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();

                // Actualizar solo los campos que se proporcionan en la solicitud (todo menos el id)
                if (alumnoDetails.getUsername() != null && !alumnoDetails.getUsername().isEmpty()) {
                    alumno.setUsername(alumnoDetails.getUsername());
                }

                if (alumnoDetails.getDni() != null && !alumnoDetails.getDni().isEmpty()) {
                    alumno.setDni(alumnoDetails.getDni());
                }

                if (alumnoDetails.getPasswordHash() != null && !alumnoDetails.getPasswordHash().isEmpty()) {
                    alumno.setPasswordHash(alumnoDetails.getPasswordHash());
                }

                // Verificar que el salón proporcionado existe antes de asignarlo
                if (alumnoDetails.getSalon() != null) {
                    Optional<Salon> salonOptional = salonService.getSalonById(alumnoDetails.getSalon().getId());
                    if (salonOptional.isPresent()) {
                        alumno.setSalon(salonOptional.get());
                    } else {
                        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                                .body(new ApiResponseDTO("El salón proporcionado no existe"));
                    }
                }

                // Guardar el alumno actualizado
                Alumno updatedAlumno = alumnoService.saveAlumno(alumno);

                // Crear la respuesta con los detalles actualizados
                AlumnoResponseDTO response = new AlumnoResponseDTO();
                response.setId(updatedAlumno.getId().toString());
                response.setUsername(updatedAlumno.getUsername());
                response.setDni(updatedAlumno.getDni());
                response.setRole(updatedAlumno.getRole().toString()); // El Role no se modifica
                response.setCreatedAt(updatedAlumno.getCreatedAt().toString());

                if (updatedAlumno.getSalon() != null) {
                    response.setSalon(updatedAlumno.getSalon().getId());
                }

                return ResponseEntity.status(HttpStatus.OK).body(response);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error actualizando el alumno"));
        }
    }


    @DeleteMapping("/admin_only/{id}")
    public ResponseEntity<?> deleteAlumno(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                alumnoService.deleteAlumno(id);
                return ResponseEntity.status(HttpStatus.NO_CONTENT).body(new ApiResponseDTO("Alumno eliminado correctamente"));
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error eliminando el alumno"));
        }
    }

}
