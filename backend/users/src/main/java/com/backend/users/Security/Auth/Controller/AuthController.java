package com.backend.users.Security.Auth.Controller;


import com.backend.users.Security.Auth.DTOs.DTOChangePassword;
import com.backend.users.Security.Auth.DTOs.DtoRegister;
import com.backend.users.Security.Auth.DTOs.LoginRequest;
import com.backend.users.Security.Auth.DTOs.ResponseLogin;
import com.backend.users.Security.Auth.Service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.Mapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;



@RestController
@RequestMapping("/api/auth")
public class AuthController {
    @Autowired
    private AuthService authService;

    @PostMapping(value = "/register/students/{profesorId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<?> registerStudents(@PathVariable Long profesorId, @RequestParam("file") MultipartFile file) throws Exception{
        try{
            ByteArrayResource resource = authService.processRegisterForStuedents(file,profesorId);
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=students.csv")
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .body(resource);

        }catch (Exception e){
            return ResponseEntity.status(500).body("Error processing file: " + e.getMessage());
        }

    }

    @PostMapping(value = "/register/profesor", consumes =MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> registerProfesor(@RequestBody DtoRegister dtoRegister) throws Exception{
        try{
            authService.registerProfessor(dtoRegister);
            return ResponseEntity.accepted().body("Profesor registrado exitosamente");
        }catch (Exception e){
            return ResponseEntity.status(404).body("No se pudo registrar al profesor: " + e.getMessage());
        }
    }
    @PostMapping(value = "/register/administrador", consumes =MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> registerAdministrador(@RequestBody DtoRegister dtoRegister) throws Exception{
        try{
            authService.registerAdmin(dtoRegister);
            return ResponseEntity.accepted().body("Administrador registrado exitosamente");
        }catch (Exception e){
            return ResponseEntity.status(404).body("No se pudo registrar al administrador: " + e.getMessage());
        }
    }

    @PostMapping(value = "/login", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> login(@RequestBody LoginRequest dtoRegister) throws Exception{
        try{
            ResponseLogin token = authService.login(dtoRegister);
            return ResponseEntity.ok(token);
        }catch (Exception e){
            return ResponseEntity.status(404).body("No se pudo iniciar sesion: " + e.getMessage());
        }
    }

    @PutMapping(value = "change-password", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> changePassword(@RequestBody DTOChangePassword change) throws Exception{
        try{
            authService.changePassword(change);
            return ResponseEntity.accepted().body("Contraseña cambiada exitosamente");
        }catch (Exception e){
            return ResponseEntity.status(401).body("No se pudo cambiar la contraseña: " + e.getMessage());
        }
    }
    @PostMapping(value = "/logout/{username}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> logout(@PathVariable String username) throws Exception{
        try{
            authService.logout(username);
            return ResponseEntity.accepted().body("Sesion cerrada exitosamente");
        }catch (Exception e){
            return ResponseEntity.status(401).body("No se pudo cerrar la sesion: " + e.getMessage());
        }
    }

    @PostMapping(value = "/refresh-token", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> refreshToken(@RequestBody String token) throws Exception{
        try{
            String newToken = authService.refreshToken(token);
            return ResponseEntity.ok(newToken);
        }catch (Exception e){
            return ResponseEntity.status(401).body("No se pudo refrescar el token: " + e.getMessage());
        }
    }


}
