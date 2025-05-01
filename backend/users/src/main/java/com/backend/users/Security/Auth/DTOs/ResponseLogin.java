package com.backend.users.Security.Auth.DTOs;

import lombok.Data;

@Data
public class ResponseLogin {

    private String token;
    private String rol;
}
