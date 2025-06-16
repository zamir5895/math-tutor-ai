package org.example.usuarios.Profesor.Application;

import jakarta.servlet.http.HttpServletRequest;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Profesor.DTOs.ProfesorRegisterRequestDTO;
import org.example.usuarios.Profesor.DTOs.ResponseProfesor;
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
        try {
            ResponseProfesor r = profesorService.guardarProfesor(request);
            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Profesor registrado exitosamente", r));
        }
        catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }

    }

    @GetMapping("/admin_only/all")
    public ResponseEntity<?> getAllProfesores() {
        try {
            List<Profesor> profesores = profesorService.getAllProfesores();
            return ResponseEntity.ok(profesores);
        } catch (Exception e) {
            logger.error("Error obteniendo la lista de profesores", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo profesores"));
        }
    }

    @GetMapping("/admin_only/{id}")
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


    @DeleteMapping("/admin_only/{id}")
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