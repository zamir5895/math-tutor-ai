package org.example.usuarios.Salon.Application;

import jakarta.servlet.http.HttpServletRequest;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Profesor.Domain.ProfesorService;
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

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @Autowired
    private ProfesorService profesorService;


    @PostMapping
    public ResponseEntity<?> createSalon(@RequestBody SalonRequestDTO request, HttpServletRequest httpRequest) {
        try {
            // Extraer el token Bearer de la cabecera Authorization
            String token = httpRequest.getHeader("Authorization");

            if (token == null || !token.startsWith("Bearer ")) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("Token de autorización requerido o inválido"));
            }

            // Extraer el JWT sin el prefijo 'Bearer '
            String jwt = token.substring(7);

            // Obtener el rol del usuario desde el token
            String role = jwtTokenProvider.extractRole(jwt); // Método que extrae el rol del token

            UUID profesorId;

            if ("ADMIN".equals(role)) {
                // Si es ADMIN, el profesorId debe venir en el cuerpo de la solicitud
                if (request.getProfesorId() == null) {
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                            .body(new ApiResponseDTO("Falta el ID del profesor"));
                }

                profesorId = request.getProfesorId();  // Usamos el profesorId proporcionado en el cuerpo

                // Verificar si el profesor con el profesorId existe en la base de datos
                if (!profesorService.existsById(profesorId)) {
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                            .body(new ApiResponseDTO("El profesor con el ID proporcionado no existe"));
                }

            } else if ("TEACHER".equals(role)) {
                // Si es un profesor, extraemos el UUID del token para usarlo como profesorId
                profesorId = jwtTokenProvider.extractUserId(jwt); // Usamos el UUID extraído del token
            } else {
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                        .body(new ApiResponseDTO("No tienes permisos para crear un salón"));
            }

            // Crear el salón con el profesorId correspondiente
            Salon salon = new Salon();
            salon.setSeccion(request.getSeccion());
            salon.setGrado(request.getGrado());
            salon.setTurno(request.getTurno());
            salon.setProfesorId(profesorId);

            // Guardar el salón
            Salon savedSalon = salonService.saveSalon(salon);

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Salón creado exitosamente", savedSalon));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }





    @GetMapping("/profesor/my-salons")
    public ResponseEntity<?> getMySalonsAsProfesor(HttpServletRequest request) {
        try {
            // Extraer el token Bearer de la cabecera Authorization
            String token = request.getHeader("Authorization");

            if (token == null || !token.startsWith("Bearer ")) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("Token de autorización requerido o inválido"));
            }

            // Extraer el JWT sin el prefijo 'Bearer '
            String jwt = token.substring(7);

            // Obtener el UUID del profesor desde el token
            UUID profesorId = jwtTokenProvider.extractUserId(jwt); // Este método debe extraer el UUID del token

            if (profesorId == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("Token inválido o expirado"));
            }

            // Obtener los salones del profesor
            List<Salon> salones = salonService.getSalonesByProfesorId(profesorId);

            // Devolver la lista de salones
            return ResponseEntity.ok(salones);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo los salones"));
        }
    }


    @GetMapping("/admin_only/all")
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
    public ResponseEntity<?> updateSalon(@PathVariable UUID id, @RequestBody SalonRequestDTO request, HttpServletRequest httpRequest) {
        try {
            // Extraer el token Bearer de la cabecera Authorization
            String token = httpRequest.getHeader("Authorization");

            if (token == null || !token.startsWith("Bearer ")) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("Token de autorización requerido o inválido"));
            }

            // Extraer el JWT sin el prefijo 'Bearer '
            String jwt = token.substring(7);

            // Obtener el UUID del profesor desde el token
            UUID profesorId = jwtTokenProvider.extractUserId(jwt); // Este método debe extraer el UUID del token

            if (profesorId == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("Token inválido o expirado"));
            }

            // Obtener el rol del usuario desde el token
            String role = jwtTokenProvider.extractRole(jwt); // Este método debe extraer el rol del token

            // Obtener el salón a actualizar
            Salon salon = salonService.getSalonById(id).orElse(null);

            if (salon == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Salón no encontrado"));
            }

            // Verificar si el profesor es ADMIN o el dueño del salón
            if (role.equals("ADMIN") || salon.getProfesorId().equals(profesorId)) {
                // Si el rol es ADMIN o el salón es del profesor, actualizar
                salon.setSeccion(request.getSeccion());
                salon.setGrado(request.getGrado());
                salon.setTurno(request.getTurno());
                salon.setProfesorId(request.getProfesorId());

                Salon updatedSalon = salonService.updateSalon(id, salon);
                return ResponseEntity.ok(new ApiResponseDTO("Salón actualizado exitosamente", updatedSalon));
            } else {
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                        .body(new ApiResponseDTO("No tienes permisos para actualizar este salón"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error actualizando salón"));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteSalon(@PathVariable UUID id, HttpServletRequest httpRequest) {
        try {
            // Extraer el token Bearer de la cabecera Authorization
            String token = httpRequest.getHeader("Authorization");

            if (token == null || !token.startsWith("Bearer ")) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("Token de autorización requerido o inválido"));
            }

            // Extraer el JWT sin el prefijo 'Bearer '
            String jwt = token.substring(7);

            // Obtener el UUID del profesor desde el token
            UUID profesorId = jwtTokenProvider.extractUserId(jwt); // Este método debe extraer el UUID del token

            if (profesorId == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponseDTO("Token inválido o expirado"));
            }

            // Obtener el rol del usuario desde el token
            String role = jwtTokenProvider.extractRole(jwt); // Este método debe extraer el rol del token

            // Obtener el salón a eliminar
            Salon salon = salonService.getSalonById(id).orElse(null);

            if (salon == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponseDTO("Salón no encontrado"));
            }

            // Verificar si el profesor es ADMIN o el dueño del salón
            if (role.equals("ADMIN") || salon.getProfesorId().equals(profesorId)) {
                // Si el rol es ADMIN o el salón es del profesor, eliminar
                salonService.deleteSalon(id);
                return ResponseEntity.ok(new ApiResponseDTO("Salón eliminado exitosamente"));
            } else {
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                        .body(new ApiResponseDTO("No tienes permisos para eliminar este salón"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error eliminando salón"));
        }
    }

}
