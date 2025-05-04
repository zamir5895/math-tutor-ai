package com.backend.users.Kafka;


import lombok.Data;

import java.time.ZonedDateTime;

@Data
public class UserFinishedEvent {
    private Long id;
    private String nombre;
    private String apellido;
    private String grado;
    private String seccion;
    private Integer edad;
    private ZonedDateTime fechaSalida;

}
