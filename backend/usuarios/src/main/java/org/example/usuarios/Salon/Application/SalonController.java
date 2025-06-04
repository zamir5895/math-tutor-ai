package org.example.usuarios.Salon.Application;

import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Salon.DTOs.SalonRequestDTO;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.Salon.Domain.SalonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/salon")
@CrossOrigin(origins = "*")
public class SalonController {

    @Autowired
    private SalonService salonService;

    @PostMapping
    public ResponseEntity<?> createSalon( @RequestBody SalonRequestDTO request) {
        try {
            Salon salon = new Salon();
            salon.setSeccion(request.getSeccion());
            salon.setGrado(request.getGrado());
            salon.setTurno(request.getTurno());
            salon.setProfesorId(request.getProfesorId());

            Salon savedSalon = salonService.saveSalon(salon);

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Salón creado exitosamente", savedSalon));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @GetMapping("/{profesor_id}")
    public ResponseEntity<?> getSalonesByProfesor(@PathVariable("profesor_id") UUID profesorId) {
        try {
            List<Salon> salones = salonService.getSalonesByProfesorId(profesorId);
            return ResponseEntity.ok(salones);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo salones"));
        }
    }

    @GetMapping
    public ResponseEntity<?> getAllSalones() {
        try {
            List<Salon> salones = salonService.getAllSalones();
            return ResponseEntity.ok(salones);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo salones"));
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateSalon(@PathVariable UUID id,  @RequestBody SalonRequestDTO request) {
        try {
            Salon salonDetails = new Salon();
            salonDetails.setSeccion(request.getSeccion());
            salonDetails.setGrado(request.getGrado());
            salonDetails.setTurno(request.getTurno());
            salonDetails.setProfesorId(request.getProfesorId());

            Salon updatedSalon = salonService.updateSalon(id, salonDetails);

            if (updatedSalon == null) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok(new ApiResponseDTO("Salón actualizado exitosamente", updatedSalon));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error actualizando salón"));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteSalon(@PathVariable UUID id) {
        try {
            if (!salonService.getSalonById(id).isPresent()) {
                return ResponseEntity.notFound().build();
            }

            salonService.deleteSalon(id);
            return ResponseEntity.ok(new ApiResponseDTO("Salón eliminado exitosamente"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error eliminando salón"));
        }
    }
}
