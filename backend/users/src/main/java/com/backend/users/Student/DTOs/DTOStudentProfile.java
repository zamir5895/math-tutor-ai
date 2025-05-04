package com.backend.users.Student.DTOs;

import lombok.Data;

@Data
public class DTOStudentProfile {
    private Long id;
    private String name;
    private String apellido;
    private Integer edad;
    private String username;
    private Integer salon;
    private String seccion;

}
