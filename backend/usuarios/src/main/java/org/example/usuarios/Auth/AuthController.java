package org.example.usuarios.Auth;

import org.example.usuarios.User.Domain.Rol;
import org.example.usuarios.User.Domain.User;
import org.example.usuarios.User.Domain.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.authentication.BadCredentialsException;

import java.util.UUID;

@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private UserService userService;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequestDTO loginRequest) {
        try {
            // Autenticar al usuario
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            loginRequest.getUsername(),
                            loginRequest.getPassword()
                    )
            );

            // Establecer el contexto de seguridad
            SecurityContextHolder.getContext().setAuthentication(authentication);

            // Generar el token JWT
            String token = jwtTokenProvider.generateToken(authentication);

            // Retornar el token JWT
            return ResponseEntity.ok(new JwtAuthenticationResponse(token));

        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(new ApiResponseDTO("Credenciales inválidas"));
        } catch (Exception e) {
            System.out.println("Error en login: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequestDTO request) {
        try {
            if (userService.existsByUsername(request.getUsername())) {
                return ResponseEntity.badRequest()
                        .body(new ApiResponseDTO("El username ya existe"));
            }

            User user = new User();
            user.setUsername(request.getUsername());

            // IMPORTANTE: La contraseña ya debe venir encriptada desde el servicio
            user.setPasswordHash(passwordEncoder.encode(request.getPassword()));

            if (request.getRole() != null) {
                user.setRole(Rol.valueOf(request.getRole().toUpperCase()));
            } else {
                user.setRole(Rol.STUDENT);
            }

            // Usar registerUser que NO encripta de nuevo
            User savedUser = userService.registerUser(user);

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Usuario registrado exitosamente"));

        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                    .body(new ApiResponseDTO("Rol inválido"));
        } catch (Exception e) {
            System.out.println("Error en registro: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }

    @GetMapping("/verify-token")
    public ResponseEntity<?> verifyToken(@RequestHeader("Authorization") String authorizationHeader) {
        try {
            // Obtener el token de la cabecera "Authorization"
            String token = authorizationHeader.substring(7); // "Bearer " es el prefijo, por lo que eliminamos los primeros 7 caracteres

            // Verificar si el token es válido
            if (jwtTokenProvider.isTokenExpired(token)) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("El token ha expirado"));
            }

            // Extraer la información del token (username, role, uuid)
            String username = jwtTokenProvider.extractUsername(token);
            String role = jwtTokenProvider.extractRole(token);
            UUID userId = jwtTokenProvider.extractUserId(token);

            // Crear la respuesta con la información extraída del token
            TokenVerificationResponseDTO response = new TokenVerificationResponseDTO();
            response.setUsername(username);
            response.setRole(role);
            response.setUserId(userId.toString());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error al verificar el token"));
        }
    }
}