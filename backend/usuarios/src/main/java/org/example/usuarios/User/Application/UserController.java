package org.example.usuarios.User.Application;

import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.User.Domain.User;
import org.example.usuarios.User.Domain.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/user")
@CrossOrigin(origins = "*")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/profile")
    public ResponseEntity<?> getUserProfile(@RequestParam("userId") UUID userId) {
        try {
            User user = userService.getUserById(userId).orElse(null);

            if (user == null) {
                return ResponseEntity.notFound().build();
            }

            // No devolver la contraseña en la respuesta
            user.setPasswordHash(null);

            return ResponseEntity.ok(user);
        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error obteniendo perfil"));
        }
    }
}