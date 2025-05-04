package com.backend.users.Salon.Application;


import com.backend.users.Salon.Domain.SalonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/salon")
public class SalonController {


    @Autowired
    private SalonService salonService;

    @PreAuthorize("hasRole('TEACHER')")
    @GetMapping("/students/{salonId}")
    public ResponseEntity<?> getStudentsBySalonId(@PathVariable Long salonId) {
        try {
            return ResponseEntity.ok(salonService.getStudentsBySalonId(salonId));
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error: " + e.getMessage());
        }
    }

    @PreAuthorize("hasRole('TEACHER')")
    @GetMapping("/cantidadEstudiantes/{salonId}")
    public ResponseEntity<?> getCantidadEstudiantes(@PathVariable Long salonId) {
        try {
            return ResponseEntity.ok(salonService.getCantidadEstudiantes(salonId));
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error: " + e.getMessage());
        }
    }
}
