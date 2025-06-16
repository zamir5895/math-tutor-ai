package org.example.usuarios.Admin.Application;

import org.example.usuarios.Admin.Domain.Admin;
import org.example.usuarios.Admin.Domain.AdminService;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.RegisterRequestDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/admin")
@CrossOrigin(origins = "*")
public class AdminController {

    @Autowired
    private AdminService adminService;

    @PostMapping("/register")
    public ResponseEntity<?> registerAdmin( @RequestBody RegisterRequestDTO request) {
        try {
            Admin admin = new Admin();
            admin.setUsername(request.getUsername());
            admin.setPasswordHash(request.getPassword());

            Admin savedAdmin = adminService.saveAdmin(admin);

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Administrador registrado exitosamente", savedAdmin));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @GetMapping
    public ResponseEntity<?> getAllAdmins() {
        try {
            List<Admin> admins = adminService.getAllAdmins();
            return ResponseEntity.ok(admins);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo administradores"));
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getAdminById(@PathVariable UUID id) {
        try {
            Admin admin = adminService.getAdminById(id).orElse(null);

            if (admin == null) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok(admin);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo administrador"));
        }
    }
}
