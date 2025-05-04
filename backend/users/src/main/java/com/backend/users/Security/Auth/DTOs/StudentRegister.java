package com.backend.users.Security.Auth.DTOs;

import lombok.Data;

@Data
public class StudentRegister {

    private String nombre;
    private String apellido;
    private Long salonId;
    private Integer edad;
    private String phoneNumber;
    private String dni;
}
