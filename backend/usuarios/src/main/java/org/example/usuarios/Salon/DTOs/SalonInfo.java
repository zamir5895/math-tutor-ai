package org.example.usuarios.Salon.DTOs;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Data
public class SalonInfo {
    private List<UUID> salonIds = new ArrayList<>();
    private Integer cantidadAlumnos;
}