package org.example.usuarios.Profesor.Application;

import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Profesor.DTOs.ProfesorRegisterRequestDTO;
import org.example.usuarios.Profesor.Domain.Profesor;
import org.example.usuarios.Profesor.Domain.ProfesorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/profesor")
@CrossOrigin(origins = "*")
public class ProfesorController {

    @Autowired
    private ProfesorService profesorService;

    @PostMapping("/register")
    public ResponseEntity<?> registerProfesor( @RequestBody ProfesorRegisterRequestDTO request) {
        try {
            // Crear nuevo profesor
            Profesor profesor = new Profesor();
            profesor.setUsername(request.getUsername());
            profesor.setPasswordHash(request.getPassword());
            profesor.setTelefono(request.getTelefono());

            Profesor savedProfesor = profesorService.saveProfesor(profesor);

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Profesor registrado exitosamente", savedProfesor));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @GetMapping
    public ResponseEntity<?> getAllProfesores() {
        try {
            List<Profesor> profesores = profesorService.getAllProfesores();
            return ResponseEntity.ok(profesores);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo profesores"));
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getProfesorById(@PathVariable UUID id) {
        try {
            Profesor profesor = profesorService.getProfesorById(id)
                    .orElse(null);

            if (profesor == null) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok(profesor);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo profesor"));
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateProfesor(@PathVariable UUID id,  @RequestBody ProfesorRegisterRequestDTO request) {
        try {
            Profesor profesorDetails = new Profesor();
            profesorDetails.setUsername(request.getUsername());
            profesorDetails.setTelefono(request.getTelefono());
            if (request.getPassword() != null && !request.getPassword().isEmpty()) {
                profesorDetails.setPasswordHash(request.getPassword());
            }

            Profesor updatedProfesor = profesorService.updateProfesor(id, profesorDetails);

            if (updatedProfesor == null) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok(new ApiResponseDTO("Profesor actualizado exitosamente", updatedProfesor));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error actualizando profesor"));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteProfesor(@PathVariable UUID id) {
        try {
            if (!profesorService.getProfesorById(id).isPresent()) {
                return ResponseEntity.notFound().build();
            }

            profesorService.deleteProfesor(id);
            return ResponseEntity.ok(new ApiResponseDTO("Profesor eliminado exitosamente"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error eliminando profesor"));
        }
    }
}

