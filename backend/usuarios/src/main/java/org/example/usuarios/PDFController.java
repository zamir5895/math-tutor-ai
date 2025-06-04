package org.example.usuarios;


import org.example.usuarios.Auth.ApiResponseDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/pdf")
@CrossOrigin(origins = "*")
public class PDFController {

    @GetMapping("/ejercicios/salon/{salonId}")
    public ResponseEntity<?> generarPDFEjerciciosSalon(@PathVariable UUID salonId) {
        try {
            return ResponseEntity.ok(new ApiResponseDTO("PDF de ejercicios para salón generado correctamente"));
        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error generando PDF"));
        }
    }

    @GetMapping("/ejercicios/salon/{salonId}/tema/{tema}")
    public ResponseEntity<?> generarPDFEjerciciosSalonTema(@PathVariable UUID salonId, @PathVariable String tema) {
        try {
            return ResponseEntity.ok(new ApiResponseDTO("PDF de ejercicios por tema para salón generado correctamente"));
        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error generando PDF"));
        }
    }

    @GetMapping("/ejercicios/alumno/{alumnoId}/tema/{tema}")
    public ResponseEntity<?> generarPDFEjerciciosAlumnoTema(@PathVariable UUID alumnoId, @PathVariable String tema) {
        try {
            return ResponseEntity.ok(new ApiResponseDTO("PDF de ejercicios por tema para alumno generado correctamente"));
        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error generando PDF"));
        }
    }
}