package org.example.usuarios.Alumno.Application;

import org.example.usuarios.Alumno.DTOs.AlumnoProfileResponseDTO;
import org.example.usuarios.Alumno.DTOs.AlumnoRegisterRequestDTO;
import org.example.usuarios.Alumno.DTOs.AlumnoResponseDTO;
import org.example.usuarios.Alumno.Domain.Alumno;
import org.example.usuarios.Alumno.Domain.AlumnoService;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Salon.DTOs.RegistroMasivoResponse;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.Salon.Domain.SalonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ContentDisposition;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.MediaType;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;
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



    @PostMapping("/register/individual/{salonId}")
    public ResponseEntity<?> registerAlumno( @RequestBody AlumnoRegisterRequestDTO request,
                                             @PathVariable UUID salonId,
                                             @RequestHeader("Authorization") String authorizationHeader) {
        try {

            return ResponseEntity.ok(alumnoService.guardarAlumno(request,salonId));

        }catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @PostMapping("/register/{salonId}")
    public ResponseEntity<?> registerAlumnosBulk(
            @RequestPart("file") MultipartFile file,
            @PathVariable UUID salonId,
            @RequestHeader("Authorization") String authorizationHeader) {

        try {
            if (file.isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(new ApiResponseDTO("El archivo está vacío"));
            }

            RegistroMasivoResponse response = alumnoService.registrarAlumnosDesdeArchivo(file, salonId);

            String csvContent = response.getCsvRespuesta();
            byte[] csvBytes = csvContent.getBytes(StandardCharsets.UTF_8);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.valueOf("text/csv"));
            headers.setContentDisposition(
                    ContentDisposition.builder("attachment")
                            .filename("alumnos_registrados.csv")
                            .build()
            );

            return new ResponseEntity<>(csvBytes, headers, HttpStatus.OK);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error procesando el archivo: " + e.getMessage()));
        }
    }
    @GetMapping("/admin_only/all")
    public ResponseEntity<?> getAllAlumnos() {
        try {
            List<Alumno> alumnos = alumnoService.getAllAlumnos();

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

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo la lista de alumnos"));
        }
    }

    @GetMapping("/student/profile")
    public ResponseEntity<?> getProfile(@RequestHeader("Authorization") String authorizationHeader) {
        try {
            String token = authorizationHeader.substring(7); // "Bearer " es el prefijo, por lo que eliminamos los primeros 7 caracteres

            UUID userId = jwtTokenProvider.extractUserId(token);

            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(userId);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();

                AlumnoProfileResponseDTO response = new AlumnoProfileResponseDTO();
                response.setId(alumno.getId().toString());
                response.setUsername(alumno.getUsername());

                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo el perfil"));
        }
    }

    @GetMapping("/studentbyId/{id}")
    public ResponseEntity<?> getStudentById(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();

                AlumnoProfileResponseDTO response = new AlumnoProfileResponseDTO();
                response.setId(alumno.getId().toString());
                response.setUsername(alumno.getUsername());

                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo el perfil del alumno"));
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

   /* @GetMapping("/salon/{id}")
    public ResponseEntity<?> getAlumnosBySalonId(@PathVariable UUID id) {
        try {
            // Obtener el salón por su ID
            Salon salon = salonService.getSalonById(id).orElse(null);

            if (salon == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Salón no encontrado"));
            }

            // Obtener la lista de alumnoIds del salón
            List<UUID> alumnoIds = salon.getAlumnoIds();

            // Si el salón no tiene alumnos asignados, devolver una lista vacía
            if (alumnoIds == null || alumnoIds.isEmpty()) {
                return ResponseEntity.ok(new ApiResponseDTO("No hay alumnos asignados a este salón"));
            }

            // Crear la respuesta con los alumnoIds
            return ResponseEntity.ok(alumnoIds);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo alumnos"));
        }
    }
*/
    @PutMapping("/admin_only/{id}")
    public ResponseEntity<?> updateAlumno(@PathVariable UUID id, @RequestBody Alumno alumnoDetails) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();

                if (alumnoDetails.getUsername() != null && !alumnoDetails.getUsername().isEmpty()) {
                    alumno.setUsername(alumnoDetails.getUsername());
                }

                if (alumnoDetails.getDni() != null && !alumnoDetails.getDni().isEmpty()) {
                    alumno.setDni(alumnoDetails.getDni());
                }

                if (alumnoDetails.getPasswordHash() != null && !alumnoDetails.getPasswordHash().isEmpty()) {
                    alumno.setPasswordHash(alumnoDetails.getPasswordHash());
                }

                if (alumnoDetails.getSalon() != null) {
                    Optional<Salon> salonOptional = salonService.getSalonById(alumnoDetails.getSalon().getId());
                    if (salonOptional.isPresent()) {
                        alumno.setSalon(salonOptional.get());
                    } else {
                        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                                .body(new ApiResponseDTO("El salón proporcionado no existe"));
                    }
                }

                Alumno updatedAlumno = alumnoService.saveAlumno(alumno);

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

    @PutMapping("/minutos/incrementar/{id}")
    public ResponseEntity<?> incrementarMinutos(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                Integer minutosActuales = alumno.getMinutosTotales() != null ? alumno.getMinutosTotales() : 0;
                alumno.setMinutosTotales(minutosActuales + 1);

                alumnoService.saveAlumno(alumno);

                return ResponseEntity.ok(new ApiResponseDTO("Minutos incrementados correctamente", alumno.getMinutosTotales()));
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error incrementando minutos"));
        }
    }

    @GetMapping("/minutos/{id}")
    public ResponseEntity<?> getMinutosTotales(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                Integer minutos = alumno.getMinutosTotales() != null ? alumno.getMinutosTotales() : 0;

                Map<String, Object> response = new HashMap<>();
                response.put("minutosTotales", minutos);

                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo minutos totales"));
        }
    }

    @PutMapping("/ultima-conexion/{id}")
    public ResponseEntity<?> actualizarUltimaConexion(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                alumno.setUltimaConexion(LocalDateTime.now());

                alumnoService.saveAlumno(alumno);

                return ResponseEntity.ok(new ApiResponseDTO("Última conexión actualizada correctamente", alumno.getUltimaConexion().toString()));
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error actualizando última conexión"));
        }
    }

    @GetMapping("/ultima-conexion/{id}")
    public ResponseEntity<?> getUltimaConexion(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                LocalDateTime ultimaConexion = alumno.getUltimaConexion();

                Map<String, Object> response = new HashMap<>();
                response.put("ultimaConexion", ultimaConexion != null ? ultimaConexion.toString() : null);

                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo última conexión"));
        }
    }

    @PostMapping("/addfecha/{id}")
    public ResponseEntity<?> agregarFechaEjercicio(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                LocalDate hoy = LocalDate.now();

                if (alumno.getFechasEjerciciosResueltos() == null) {
                    alumno.setFechasEjerciciosResueltos(new ArrayList<>());
                }

                if (!alumno.getFechasEjerciciosResueltos().contains(hoy)) {
                    alumno.agregarFechaEjercicioResuelto(hoy);
                    alumnoService.saveAlumno(alumno);

                    return ResponseEntity.ok(new ApiResponseDTO("Fecha de ejercicio agregada correctamente", hoy.toString()));
                } else {
                    return ResponseEntity.ok(new ApiResponseDTO("Ya existe un ejercicio registrado para hoy", hoy.toString()));
                }
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error agregando fecha de ejercicio"));
        }
    }

    @GetMapping("/ejercicios-fechas/{id}")
    public ResponseEntity<?> getFechasEjercicios(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                List<LocalDate> fechas = alumno.getFechasEjerciciosResueltos();

                Map<String, Object> response = new HashMap<>();
                response.put("fechasEjercicios", fechas != null ? fechas : new ArrayList<>());

                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo fechas de ejercicios"));
        }
    }

    @GetMapping("/racha/{id}")
    public ResponseEntity<?> calcularRacha(@PathVariable UUID id) {
        try {
            Optional<Alumno> optionalAlumno = alumnoService.getAlumnoById(id);
            if (optionalAlumno.isPresent()) {
                Alumno alumno = optionalAlumno.get();
                List<LocalDate> fechas = alumno.getFechasEjerciciosResueltos();

                int racha = calcularRachaConsecutiva(fechas);

                Map<String, Object> response = new HashMap<>();
                response.put("racha", racha);
                response.put("mensaje", racha > 0 ?
                        "¡Llevas " + racha + " día" + (racha > 1 ? "s" : "") + " consecutivo" + (racha > 1 ? "s" : "") + "!" :
                        "¡Empieza tu racha resolviendo un ejercicio hoy!");

                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Alumno no encontrado"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error calculando racha"));
        }
    }

    private int calcularRachaConsecutiva(List<LocalDate> fechas) {
        if (fechas == null || fechas.isEmpty()) {
            return 0;
        }

        List<LocalDate> fechasOrdenadas = fechas.stream()
                .distinct() // Eliminar duplicados
                .sorted(Collections.reverseOrder())
                .collect(Collectors.toList());

        LocalDate hoy = LocalDate.now();
        int racha = 0;

        if (!fechasOrdenadas.contains(hoy)) {
            if (!fechasOrdenadas.contains(hoy.minusDays(1))) {
                return 0;
            } else {
                hoy = hoy.minusDays(1);
            }
        }

        LocalDate fechaActual = hoy;
        for (LocalDate fecha : fechasOrdenadas) {
            if (fecha.equals(fechaActual)) {
                racha++;
                fechaActual = fechaActual.minusDays(1);
            } else if (fecha.isBefore(fechaActual)) {
                break;
            }
        }

        return racha;
    }
}