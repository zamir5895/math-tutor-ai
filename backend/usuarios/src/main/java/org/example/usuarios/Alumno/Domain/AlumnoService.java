package org.example.usuarios.Alumno.Domain;

import org.example.usuarios.Alumno.Infraestructure.AlumnoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class AlumnoService {

    @Autowired
    private AlumnoRepository alumnoRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public List<Alumno> getAllAlumnos() {
        return alumnoRepository.findAll();
    }

    public Optional<Alumno> getAlumnoById(UUID id) {
        return alumnoRepository.findById(id);
    }

    public Optional<Alumno> getAlumnoByDni(String dni) {
        return alumnoRepository.findByDni(dni);
    }

    public List<Alumno> getAlumnosBySalonId(UUID salonId) {
        return alumnoRepository.findBySalonId(salonId);
    }

    public List<Alumno> getAlumnosBySeccion(String seccion) {
        return alumnoRepository.findBySeccion(seccion);
    }

    public Alumno saveAlumno(Alumno alumno) {
        // Solo encriptar la contraseña si no está ya encriptada
        if (alumno.getPasswordHash() != null && !alumno.getPasswordHash().startsWith("$2a$")) {
            alumno.setPasswordHash(passwordEncoder.encode(alumno.getPasswordHash()));
        }
        return alumnoRepository.save(alumno);
    }

    public boolean existsByDni(String dni) {
        return alumnoRepository.existsByDni(dni);
    }

    public void deleteAlumno(UUID id) {
        alumnoRepository.deleteById(id);
    }

    public Alumno updateAlumno(UUID id, Alumno alumnoDetails) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(id);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            alumno.setUsername(alumnoDetails.getUsername());
            alumno.setDni(alumnoDetails.getDni());
            if (alumnoDetails.getPasswordHash() != null && !alumnoDetails.getPasswordHash().isEmpty()) {
                alumno.setPasswordHash(passwordEncoder.encode(alumnoDetails.getPasswordHash()));
            }
            return alumnoRepository.save(alumno);
        }
        return null;
    }

    // Métodos para manejo de minutos totales
    public Alumno incrementarMinutos(UUID alumnoId) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            Integer minutosActuales = alumno.getMinutosTotales() != null ? alumno.getMinutosTotales() : 0;
            alumno.setMinutosTotales(minutosActuales + 1);
            return alumnoRepository.save(alumno);
        }
        return null;
    }

    public Integer getMinutosTotales(UUID alumnoId) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            return alumno.getMinutosTotales() != null ? alumno.getMinutosTotales() : 0;
        }
        return 0;
    }

    public Alumno setMinutosTotales(UUID alumnoId, Integer minutos) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            alumno.setMinutosTotales(minutos);
            return alumnoRepository.save(alumno);
        }
        return null;
    }

    // Métodos para manejo de última conexión
    public Alumno actualizarUltimaConexion(UUID alumnoId) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            alumno.setUltimaConexion(LocalDateTime.now());
            return alumnoRepository.save(alumno);
        }
        return null;
    }

    public LocalDateTime getUltimaConexion(UUID alumnoId) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            return optionalAlumno.get().getUltimaConexion();
        }
        return null;
    }

    // Métodos para manejo de fechas de ejercicios
    public Alumno agregarFechaEjercicio(UUID alumnoId, LocalDate fecha) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            alumno.agregarFechaEjercicioResuelto(fecha);
            return alumnoRepository.save(alumno);
        }
        return null;
    }

    public Alumno agregarFechaEjercicioHoy(UUID alumnoId) {
        return agregarFechaEjercicio(alumnoId, LocalDate.now());
    }

    public List<LocalDate> getFechasEjercicios(UUID alumnoId) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            return optionalAlumno.get().getFechasEjerciciosResueltos();
        }
        return null;
    }

    public boolean tieneEjercicioEnFecha(UUID alumnoId, LocalDate fecha) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            List<LocalDate> fechas = optionalAlumno.get().getFechasEjerciciosResueltos();
            return fechas != null && fechas.contains(fecha);
        }
        return false;
    }

    public boolean tieneEjercicioHoy(UUID alumnoId) {
        return tieneEjercicioEnFecha(alumnoId, LocalDate.now());
    }

    // Método para obtener estadísticas del alumno
    public AlumnoStats getEstadisticasAlumno(UUID alumnoId) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            return new AlumnoStats(
                    alumno.getMinutosTotales() != null ? alumno.getMinutosTotales() : 0,
                    alumno.getUltimaConexion(),
                    alumno.getFechasEjerciciosResueltos() != null ? alumno.getFechasEjerciciosResueltos().size() : 0
            );
        }
        return null;
    }

    // Método para limpiar fechas duplicadas (mantenimiento)
    public Alumno limpiarFechasDuplicadas(UUID alumnoId) {
        Optional<Alumno> optionalAlumno = alumnoRepository.findById(alumnoId);
        if (optionalAlumno.isPresent()) {
            Alumno alumno = optionalAlumno.get();
            List<LocalDate> fechas = alumno.getFechasEjerciciosResueltos();
            if (fechas != null) {
                List<LocalDate> fechasUnicas = fechas.stream().distinct().sorted().toList();
                alumno.setFechasEjerciciosResueltos(fechasUnicas);
                return alumnoRepository.save(alumno);
            }
        }
        return null;
    }

    // Clase interna para estadísticas
    public static class AlumnoStats {
        private Integer minutosTotales;
        private LocalDateTime ultimaConexion;
        private Integer totalEjercicios;

        public AlumnoStats(Integer minutosTotales, LocalDateTime ultimaConexion, Integer totalEjercicios) {
            this.minutosTotales = minutosTotales;
            this.ultimaConexion = ultimaConexion;
            this.totalEjercicios = totalEjercicios;
        }

        // Getters
        public Integer getMinutosTotales() { return minutosTotales; }
        public LocalDateTime getUltimaConexion() { return ultimaConexion; }
        public Integer getTotalEjercicios() { return totalEjercicios; }

        // Setters
        public void setMinutosTotales(Integer minutosTotales) { this.minutosTotales = minutosTotales; }
        public void setUltimaConexion(LocalDateTime ultimaConexion) { this.ultimaConexion = ultimaConexion; }
        public void setTotalEjercicios(Integer totalEjercicios) { this.totalEjercicios = totalEjercicios; }
    }
}