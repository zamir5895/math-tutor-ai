package com.backend.users.Security.Auth.DTOs;

import lombok.Data;

@Data
public class LoginRequest {

    private String email;
    private String password;
}
