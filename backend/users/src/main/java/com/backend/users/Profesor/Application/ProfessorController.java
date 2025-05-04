package com.backend.users.Profesor.Application;


import com.backend.users.Profesor.Domain.ProfessorService;
import com.backend.users.Security.Auth.DTOs.StudentRegister;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/profesor")
public class ProfessorController {
    @Autowired
    private ProfessorService professorService;

    @PreAuthorize("hasRole('TEACHER')")
    @GetMapping("/profile")
    public ResponseEntity<?> getProfessorProfile() {
        try {
            return ResponseEntity.ok(professorService.getProfessorProfile());
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error: " + e.getMessage());
        }
    }
    @PreAuthorize("hasRole('TEACHER')")
    @GetMapping("/registerStudent")
    public ResponseEntity<?> registerStudent(@RequestBody StudentRegister dto) {
        try {
            return ResponseEntity.ok(professorService.registerOneStudent(dto));
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error: " + e.getMessage());
        }
    }

    @PreAuthorize("hasRole('TEACHER')")
    @GetMapping("/deleteStudent/{studentId}")
    public ResponseEntity<?> deleteStudent(@PathVariable Long studentId) {
        try {
            professorService.deleteStudent(studentId);
            return ResponseEntity.ok("Student deleted successfully");
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error: " + e.getMessage());
        }
    }

}
