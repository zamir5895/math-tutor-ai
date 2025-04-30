package com.backend.users.Security.Auth.Service;


import jakarta.annotation.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.ArrayList;
import java.util.List;

@Service
public class AuthService {

    public ResponseEntity<Resource> processRegisterForStuedents(MultipartFile file) throws Exception{
        List<String[]> result = new ArrayList<>();
        result.add(new String[]{"Nombre", "Apellido", "Usename", "Contraseña", "DNI", "Status", "Message"});
        try (CSVReader){

        }
    }
}
