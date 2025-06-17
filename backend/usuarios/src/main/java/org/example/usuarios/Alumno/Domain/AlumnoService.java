package org.example.usuarios.Alumno.Domain;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.example.usuarios.Alumno.DTOs.AlumnoCSVRecord;
import org.example.usuarios.Alumno.DTOs.AlumnoRegisterRequestDTO;
import org.example.usuarios.Alumno.DTOs.AlumnoRegisterResponse;
import org.example.usuarios.Alumno.DTOs.AlumnoResponseDTO;
import org.example.usuarios.Alumno.Infraestructure.AlumnoRepository;
import org.example.usuarios.Auth.ApiResponseDTO;
import org.example.usuarios.Salon.DTOs.AlumnoRegistroDTO;
import org.example.usuarios.Salon.DTOs.RegistroMasivoResponse;
import org.example.usuarios.Salon.DTOs.SalonInfo;
import org.example.usuarios.Salon.DTOs.SalonResponse;
import org.example.usuarios.Salon.Domain.Salon;
import org.example.usuarios.Salon.Infraestructure.SalonRepository;
import org.example.usuarios.User.Domain.Rol;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class AlumnoService {

    @Autowired
    private AlumnoRepository alumnoRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;
    @Autowired
    private SalonRepository salonRepository;

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

    public static class AlumnoStats {
        private Integer minutosTotales;
        private LocalDateTime ultimaConexion;
        private Integer totalEjercicios;

        public AlumnoStats(Integer minutosTotales, LocalDateTime ultimaConexion, Integer totalEjercicios) {
            this.minutosTotales = minutosTotales;
            this.ultimaConexion = ultimaConexion;
            this.totalEjercicios = totalEjercicios;
        }

        public Integer getMinutosTotales() { return minutosTotales; }
        public LocalDateTime getUltimaConexion() { return ultimaConexion; }
        public Integer getTotalEjercicios() { return totalEjercicios; }

        public void setMinutosTotales(Integer minutosTotales) { this.minutosTotales = minutosTotales; }
        public void setUltimaConexion(LocalDateTime ultimaConexion) { this.ultimaConexion = ultimaConexion; }
        public void setTotalEjercicios(Integer totalEjercicios) { this.totalEjercicios = totalEjercicios; }
    }

    public AlumnoRegisterResponse guardarAlumno(AlumnoRegisterRequestDTO dto, UUID salonId){
        Salon s = salonRepository.findById(salonId)
                .orElseThrow(() -> new IllegalArgumentException("El salón con ID " + salonId + " no existe"));
        if (existsByDni(dto.getDni())) {
            throw new IllegalArgumentException("Ya existe un alumno con el DNI proporcionado");
        }
        String username = generarUsername(dto.getNombre(), dto.getApellido());
        if (alumnoRepository.existsByDni(dto.getDni())) {
            throw new IllegalArgumentException("Ya existe un alumno con el DNI proporcionado");
        }
        if (alumnoRepository.existsByUsername(username)) {
            throw new IllegalArgumentException("El username ya está registrado");
        }
        Alumno alumno = new Alumno();
        alumno.setNombre(dto.getNombre());
        alumno.setApellido(dto.getApellido());
        alumno.setUsername(username.toLowerCase());
        alumno.setDni(dto.getDni());
        String password = generarPasswordSimple(dto.getNombre(), dto.getApellido(), dto.getDni());
        alumno.setPasswordHash(passwordEncoder.encode(password));
        alumno.setSalon(s);
        alumno.setRole(Rol.STUDENT);
        alumno.setCreatedAt(ZonedDateTime.now());
        Alumno alumnoGuardado = saveAlumno(alumno);
        return new AlumnoRegisterResponse(
                alumnoGuardado.getNombre(),
                alumnoGuardado.getApellido(),
                alumnoGuardado.getDni(),
                alumnoGuardado.getUsername(),
                password,
                alumnoGuardado.getId()
        );


    }

    private String generarUsername(String nombre, String apellido) {
        return (nombre.substring(0, 4) + apellido).toLowerCase();
    }

    private String generarPasswordSimple(String nombre, String apellido, String dni) {
        String parteNombre = nombre.length() >= 4 ?
                nombre.substring(0, 4).toLowerCase() :
                nombre.toLowerCase();

        String parteApellido = apellido.length() >= 4 ?
                apellido.substring(0, 4).toLowerCase() :
                apellido.toLowerCase();

        String parteDni = dni.length() >= 4 ?
                dni.substring(dni.length() - 4) :
                dni;


        return (parteNombre + parteApellido + parteDni).toLowerCase();
    }


    private List<AlumnoCSVRecord> leerCSV(MultipartFile file) throws Exception {
        try (InputStream is = file.getInputStream();
             BufferedReader br = new BufferedReader(new InputStreamReader(is))) {

            return br.lines()
                    .skip(1) // Saltar encabezados
                    .map(line -> {
                        String[] values = line.split(",");
                        return new AlumnoCSVRecord(
                                values[0].trim(),
                                values[1].trim(),
                                values[2].trim()
                        );
                    })
                    .collect(Collectors.toList());
        }
    }
    private String getCellValue(Cell cell) {
        if (cell == null) return "";

        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue().trim();
            case NUMERIC:
                return String.valueOf((int) cell.getNumericCellValue());
            default:
                return "";
        }
    }
    private List<AlumnoCSVRecord> leerExcel(MultipartFile file) throws Exception {
        List<AlumnoCSVRecord> records = new ArrayList<>();

        try (Workbook workbook = new XSSFWorkbook(file.getInputStream())) {
            Sheet sheet = workbook.getSheetAt(0);

            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row != null) {
                    records.add(new AlumnoCSVRecord(
                            getCellValue(row.getCell(0)),
                            getCellValue(row.getCell(1)),
                            getCellValue(row.getCell(2))
                    ));
                }
            }
        }

        return records;
    }

    public RegistroMasivoResponse registrarAlumnosDesdeArchivo(MultipartFile file, UUID salonId) {
        try {
            if (file.isEmpty()) {
                throw new IllegalArgumentException("El archivo está vacío");
            }

            List<AlumnoCSVRecord> records;
            String fileName = file.getOriginalFilename();

            if (fileName != null && fileName.endsWith(".xlsx")) {
                records = leerExcel(file);
            } else {
                records = leerCSV(file);
            }
            int cont = 0;

            List<AlumnoRegistroDTO> alumnosRegistrados = new ArrayList<>();
            Salon s = salonRepository.findById(salonId)
                    .orElseThrow(() -> new IllegalArgumentException("El salón con ID " + salonId + " no existe"));
            for (AlumnoCSVRecord record : records) {
                String username = generarUsername(record.getNombre(), record.getApellido());

                String password = generarPasswordSimple(record.getNombre(), record.getApellido(), record.getDni());

                Alumno alumno = new Alumno();
                alumno.setNombre(record.getNombre());
                alumno.setApellido(record.getApellido());
                alumno.setUsername(username.toLowerCase());
                alumno.setDni(record.getDni());
                alumno.setPasswordHash(passwordEncoder.encode(password));
                alumno.setRole(Rol.STUDENT);
                alumno.setCreatedAt(ZonedDateTime.now());
                alumno.setSalon(s);
                Alumno alumnoGuardado = saveAlumno(alumno);


                alumnosRegistrados.add(new AlumnoRegistroDTO(
                        alumnoGuardado.getUsername(),
                        password
                ));
                cont+=1;
            }

            String csvRespuesta = generarCSVRespuesta(alumnosRegistrados);

            return new RegistroMasivoResponse(cont, csvRespuesta);

        } catch (Exception e) {
            throw new IllegalArgumentException("Error al registrar el archivo", e);
        }
    }
    private String generarCSVRespuesta(List<AlumnoRegistroDTO> alumnos) {
        StringBuilder csv = new StringBuilder("username,password\n");

        for (AlumnoRegistroDTO alumno : alumnos) {
            csv.append(alumno.getUsername())
                    .append(",")
                    .append(alumno.getContraseña())
                    .append("\n");
        }

        return csv.toString();
    }

    public SalonResponse getSalonByAlumnoId(UUID alumnoId) {
        Alumno alumno = alumnoRepository.findById(alumnoId)
                .orElseThrow(() -> new IllegalArgumentException("El alumno con ID " + alumnoId + " no existe"));

        Salon salon = salonRepository.findStudentSalon(alumnoId)
                .orElseThrow(() -> new IllegalArgumentException("El alumno no está asignado a ningún salón"));

        SalonResponse salonResponse = new SalonResponse();
        salonResponse.setId(salon.getId());
        salonResponse.setCantidadAlumnos(salon.getAlumnos().size());
        salonResponse.setNombre(salon.getNombre());
        salonResponse.setSeccion(salon.getSeccion());
        salonResponse.setGrado(salon.getGrado());
        salonResponse.setTurno(salon.getTurno());
        salonResponse.setDescripcion(salon.getDescripcion());
        return salonResponse;
    }
}