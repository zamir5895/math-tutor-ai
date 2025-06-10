package org.example.usuarios.User.Application;

import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.User.Domain.User;
import org.example.usuarios.User.Domain.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;
import java.util.UUID;

@RestController
@RequestMapping("/user")
@CrossOrigin(origins = "*")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @GetMapping("/profile")
    public ResponseEntity<?> getUserProfile(HttpServletRequest request) {
        try {
            String token = request.getHeader("Authorization");
            if (token == null || !token.startsWith("Bearer ")) {
                return ResponseEntity.status(401)
                        .body(new ApiResponseDTO("Token de autorización requerido"));
            }

            String jwt = token.substring(7);
            UUID userId = jwtTokenProvider.extractUserId(jwt);

            User user = userService.getUserById(userId).orElse(null);

            if (user == null) {
                return ResponseEntity.notFound().build();
            }

            user.setPasswordHash(null);

            return ResponseEntity.ok(user);
        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error obteniendo perfil"));
        }
    }
}