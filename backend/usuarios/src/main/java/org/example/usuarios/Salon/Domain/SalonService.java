package org.example.usuarios.Salon.Domain;

import org.example.usuarios.Salon.Infraestructure.SalonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class SalonService {

    @Autowired
    private SalonRepository salonRepository;

    public List<Salon> getAllSalones() {
        return salonRepository.findAll();
    }

    public Optional<Salon> getSalonById(UUID id) {
        return salonRepository.findById(id);
    }

    public List<Salon> getSalonesByProfesorId(UUID profesorId) {
        return salonRepository.findByProfesorId(profesorId);
    }

    public List<Salon> getSalonesByGrado(String grado) {
        return salonRepository.findByGrado(grado);
    }

    public List<Salon> getSalonesByTurno(String turno) {
        return salonRepository.findByTurno(turno);
    }

    public List<Salon> getSalonesByGradoAndSeccion(String grado, String seccion) {
        return salonRepository.findByGradoAndSeccion(grado, seccion);
    }

    public Salon saveSalon(Salon salon) {
        return salonRepository.save(salon);
    }

    public void deleteSalon(UUID id) {
        salonRepository.deleteById(id);
    }

    public Salon updateSalon(UUID id, Salon salonDetails) {
        Optional<Salon> optionalSalon = salonRepository.findById(id);
        if (optionalSalon.isPresent()) {
            Salon salon = optionalSalon.get();

            // Actualizamos los detalles básicos del salón
            salon.setSeccion(salonDetails.getSeccion());
            salon.setGrado(salonDetails.getGrado());
            salon.setTurno(salonDetails.getTurno());
            salon.setProfesorId(salonDetails.getProfesorId());

            // Actualizamos solo los IDs de los alumnos
            if (salonDetails.getAlumnoIds() != null && !salonDetails.getAlumnoIds().isEmpty()) {
                salon.setAlumnoIds(salonDetails.getAlumnoIds()); // Asignamos los IDs de los alumnos
            }

            // Guardamos el salón actualizado
            return salonRepository.save(salon);
        }
        return null; // Si no se encuentra el salón, devolvemos null
    }


}