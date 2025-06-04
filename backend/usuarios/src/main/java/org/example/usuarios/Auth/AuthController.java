package org.example.usuarios.Auth;

import org.example.usuarios.User.Domain.User;
import org.example.usuarios.User.Domain.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.example.usuarios.User.Domain.Rol;



@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> register( @RequestBody RegisterRequestDTO request) {
        try {
            // Verificar si el usuario existe
            if (userService.existsByUsername(request.getUsername())) {
                return ResponseEntity.badRequest()
                        .body(new ApiResponseDTO("El username ya existe"));
            }

            // Crear nuevo usuario
            User user = new User();
            user.setUsername(request.getUsername());
            user.setPasswordHash(request.getPassword());

            // Asignar rol
            if (request.getRole() != null) {
                user.setRole(Rol.valueOf(request.getRole().toUpperCase()));
            } else {
                user.setRole(Rol.STUDENT);
            }

            User savedUser = userService.saveUser(user);

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Usuario registrado exitosamente", savedUser));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }




}
