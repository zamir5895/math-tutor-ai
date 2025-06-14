package org.example.usuarios.Salon.Application;

import jakarta.servlet.http.HttpServletRequest;
import org.example.usuarios.Alumno.DTOs.AlumnosDTO;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Auth.JwtTokenProvider;
import org.example.usuarios.Salon.DTOs.SalonInfo;
import org.example.usuarios.Salon.DTOs.SalonRequestDTO;
import org.example.usuarios.Salon.DTOs.SalonResponse;
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



    @PostMapping
    public ResponseEntity<?> createSalon(@RequestBody SalonRequestDTO request, @RequestHeader("Authorization") String token) {
        try {
            System.out.println(request.getNombre());
            SalonResponse response = salonService.createSalon(request, token);
            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new ApiResponseDTO("Salón creado exitosamente", response));

        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ApiResponseDTO(e.getMessage()));

        } catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error interno del servidor"));
        }
    }



    @GetMapping("/profesor/my-salons")
    public ResponseEntity<?> getMySalonsAsProfesor(HttpServletRequest request) {
        try {
            List<SalonResponse> salones = salonService.getSalonesByProfesorId(request.getHeader("Authorization"));
            return ResponseEntity.ok(salones);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(new ApiResponseDTO(e.getMessage()));
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
    public ResponseEntity<?> updateSalon(
            @PathVariable UUID id,
            @RequestBody SalonRequestDTO request,
            HttpServletRequest httpRequest) {
        try {
            SalonResponse updatedSalon = salonService.updateSalon(id, request, httpRequest.getHeader("Authorization"));
            return ResponseEntity.ok(new ApiResponseDTO("Salón actualizado exitosamente", updatedSalon));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error actualizando salón"));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteSalon(@PathVariable UUID id, HttpServletRequest httpRequest) {
        try {
            salonService.deleteSalon(id, httpRequest.getHeader("Authorization"));
            return ResponseEntity.ok(new ApiResponseDTO("Salón eliminado exitosamente"));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error eliminando salón"));
        }
    }

    @GetMapping("/search")
    public ResponseEntity<?> searchSalonsByName(@RequestParam String nombre, HttpServletRequest httpServletRequest) {
        try {
            List<SalonResponse> salones = salonService.searchSalonsByName(nombre, httpServletRequest.getHeader("Authorization"));
            return ResponseEntity.ok(salones);
        } catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));
        }
        catch (Exception e) {
            return ResponseEntity.status(500)
                    .body(new ApiResponseDTO("Error buscando salones"));
        }

    }

    @GetMapping("/alumnos/{id}")
    public ResponseEntity<?> getAlumnosBySalonId(@PathVariable UUID id, HttpServletRequest httpServletRequest) {
        try {
            String token = httpServletRequest.getHeader("Authorization");
            String jwt = token != null && token.startsWith("Bearer ") ? token.substring(7) : token;
            String userId = jwtTokenProvider.extractUserId(jwt).toString();
            List<AlumnosDTO> alumnos = salonService.obtenerAlumnosRegistradosRecientemente(id, UUID.fromString(userId));
            return ResponseEntity.ok().body(new ApiResponseDTO("Alumnos obtenidos", alumnos));


        }catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ApiResponseDTO(e.getMessage()));
        }

        catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo salón"));
        }
    }
    @GetMapping("/{id}")
    public ResponseEntity<?> getSalonById(@PathVariable UUID id, HttpServletRequest httpServletRequest) {
        try {
            String token = httpServletRequest.getHeader("Authorization");
            String jwt = token != null && token.startsWith("Bearer ") ? token.substring(7) : token;
            String userId = jwtTokenProvider.extractUserId(jwt).toString();
            SalonResponse salon = salonService.getInfoBySalonId(id, UUID.fromString(userId));
            return ResponseEntity.ok().body(new ApiResponseDTO("Salón encontrado", salon));
        }catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));
        }
        catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo salón"));
        }
    }

    @GetMapping("/profesor")
    public ResponseEntity<?> getInfoOfAllSalons(
            @RequestHeader("Authorization") String token) {
        try {
            String jwt = token != null && token.startsWith("Bearer ") ? token.substring(7) : token;
            String userId = jwtTokenProvider.extractUserId(jwt).toString();
            SalonInfo info = salonService.getInfoOfSalonByprofesorId(UUID.fromString(userId));
            return ResponseEntity.ok().body(info);
        } catch (SecurityException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(new ApiResponseDTO(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ApiResponseDTO("Error obteniendo los salones del profesor"));
        }
    }





}
