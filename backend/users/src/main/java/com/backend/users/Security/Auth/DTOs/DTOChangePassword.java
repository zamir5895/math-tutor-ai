package com.backend.users.Security.Auth.DTOs;

import lombok.Data;

@Data
public class DTOChangePassword {
    private String username;
    private String newPassword;

}
