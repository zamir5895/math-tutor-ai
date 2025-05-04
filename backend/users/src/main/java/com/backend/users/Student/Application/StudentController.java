package com.backend.users.Student.Application;

import com.backend.users.Student.Domain.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/students")
public class StudentController {
    @Autowired
    private StudentService studentService;
    @PreAuthorize("hasRole('STUDENT')")
    @PostMapping("/profile")
    public ResponseEntity<?> getStudentProfile() {
        try {
            return ResponseEntity.ok(studentService.getStudentProfile());
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error: " + e.getMessage());
        }
    }






}
