package org.example.usuarios.Profesor.Application;

import jakarta.servlet.http.HttpServletRequest;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Profesor.DTOs.ProfesorRegisterRequestDTO;
import org.example.usuarios.Profesor.Domain.Profesor;
import org.example.usuarios.Profesor.Domain.ProfesorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
@RequestMapping("/profesor")
@CrossOrigin(origins = "*")
public class ProfesorController {

    private static final Logger logger = LoggerFactory.getLogger(ProfesorController.class);

    @Autowired
    private ProfesorService profesorService;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @PostMapping("/register")
    public ResponseEntity<?> registerProfesor(@RequestBody ProfesorRegisterRequestDTO request) {
        logger.debug("Invocando endpoint registerProfesor con username: {}", request.getUsername());

        try {
            if (profesorService.existsByUsername(request.getUsername())) {
                logger.warn("El username ya está registrado: {}", request.getUsername());
                return ResponseEntity.badRequest()
                        .body(new ApiResponseDTO("El username ya está registrado"));
            }

            Profesor profesor = new Profesor();
            profesor.setUsername(request.getUsername());
            profesor.setPasswordHash(request.getPassword());
            profesor.setTelefono(request.getTelefono());

            Profesor savedProfesor = profesorService.saveProfesor(profesor);
            logger.info("Profesor registrado exitosamente: {}", savedProfesor.getUsername());

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Profesor registrado exitosamente", savedProfesor));

        } catch (Exception e) {
            logger.error("Error interno al registrar profesor", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @GetMapping("/all")
    public ResponseEntity<?> getAllProfesores() {
        logger.debug("Invocando endpoint getAllProfesores");

        try {
            List<Profesor> profesores = profesorService.getAllProfesores();
            return ResponseEntity.ok(profesores);
        } catch (Exception e) {
            logger.error("Error obteniendo la lista de profesores", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo profesores"));
        }
    }

    @GetMapping("/a/{id}")
    public ResponseEntity<?> getProfesorById(@PathVariable UUID id) {
        logger.debug("Invocando endpoint getProfesorById con ID: {}", id);

        try {
            Profesor profesor = profesorService.getProfesorById(id).orElse(null);

            if (profesor == null) {
                logger.warn("Profesor no encontrado con ID: {}", id);
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok(profesor);
        } catch (Exception e) {
            logger.error("Error obteniendo profesor con ID: {}", id, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo profesor"));
        }
    }

    @GetMapping("/profile")
    public ResponseEntity<?> getMyProfile(HttpServletRequest request) {
        logger.debug("Invocando endpoint getMyProfile");

        try {
            String token = request.getHeader("Authorization");
            if (token == null || !token.startsWith("Bearer ")) {
                logger.warn("Token de autorización no presente o inválido.");
                return ResponseEntity.status(401)
                        .body(new ApiResponseDTO("Token de autorización requerido"));
            }

            String jwt = token.substring(7);
            UUID userId = jwtTokenProvider.extractUserId(jwt);
            logger.debug("Token válido, userId extraído: {}", userId);

            Profesor profesor = profesorService.getProfesorById(userId).orElse(null);

            if (profesor == null) {
                logger.warn("Profesor no encontrado con ID: {}", userId);
                return ResponseEntity.notFound().build();
            }

            profesor.setPasswordHash(null);
            return ResponseEntity.ok(profesor);
        } catch (Exception e) {
            logger.error("Error obteniendo perfil", e);
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error obteniendo perfil"));
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateProfesor(@PathVariable UUID id, @RequestBody ProfesorRegisterRequestDTO request) {
        logger.debug("Invocando endpoint updateProfesor con ID: {} y username: {}", id, request.getUsername());

        try {
            Profesor profesorDetails = new Profesor();
            profesorDetails.setUsername(request.getUsername());
            profesorDetails.setTelefono(request.getTelefono());
            if (request.getPassword() != null && !request.getPassword().isEmpty()) {
                profesorDetails.setPasswordHash(request.getPassword());
            }

            Profesor updatedProfesor = profesorService.updateProfesor(id, profesorDetails);

            if (updatedProfesor == null) {
                logger.warn("Profesor con ID: {} no encontrado para actualizar", id);
                return ResponseEntity.notFound().build();
            }

            logger.info("Profesor con ID: {} actualizado exitosamente", id);
            return ResponseEntity.ok(new ApiResponseDTO("Profesor actualizado exitosamente", updatedProfesor));
        } catch (Exception e) {
            logger.error("Error actualizando profesor con ID: {}", id, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error actualizando profesor"));
        }
    }

    @PutMapping("/profile")
    public ResponseEntity<?> updateMyProfile(HttpServletRequest request, @RequestBody ProfesorRegisterRequestDTO requestBody) {
        logger.debug("Invocando endpoint updateMyProfile para el profesor");

        try {
            String token = request.getHeader("Authorization");
            if (token == null || !token.startsWith("Bearer ")) {
                logger.warn("Token de autorización no presente o inválido.");
                return ResponseEntity.status(401)
                        .body(new ApiResponseDTO("Token de autorización requerido"));
            }

            String jwt = token.substring(7);
            UUID userId = jwtTokenProvider.extractUserId(jwt);
            logger.debug("Token válido, userId extraído: {}", userId);

            Profesor profesorDetails = new Profesor();
            profesorDetails.setUsername(requestBody.getUsername());
            profesorDetails.setTelefono(requestBody.getTelefono());

            if (requestBody.getPassword() != null && !requestBody.getPassword().isEmpty()) {
                profesorDetails.setPasswordHash(requestBody.getPassword());
            }

            Profesor updatedProfesor = profesorService.updateProfesor(userId, profesorDetails);

            if (updatedProfesor == null) {
                logger.warn("Profesor con ID: {} no encontrado para actualizar", userId);
                return ResponseEntity.notFound().build();
            }

            updatedProfesor.setPasswordHash(null);
            logger.info("Perfil del profesor con ID: {} actualizado exitosamente", userId);
            return ResponseEntity.ok(new ApiResponseDTO("Perfil actualizado exitosamente", updatedProfesor));
        } catch (Exception e) {
            logger.error("Error actualizando perfil del profesor", e);
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error actualizando perfil"));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteProfesor(@PathVariable UUID id) {
        logger.debug("Invocando endpoint deleteProfesor con ID: {}", id);

        try {
            if (!profesorService.getProfesorById(id).isPresent()) {
                logger.warn("Profesor con ID: {} no encontrado para eliminar", id);
                return ResponseEntity.notFound().build();
            }

            profesorService.deleteProfesor(id);
            logger.info("Profesor con ID: {} eliminado exitosamente", id);
            return ResponseEntity.ok(new ApiResponseDTO("Profesor eliminado exitosamente"));
        } catch (Exception e) {
            logger.error("Error eliminando profesor con ID: {}", id, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error eliminando profesor"));
        }
    }
}
