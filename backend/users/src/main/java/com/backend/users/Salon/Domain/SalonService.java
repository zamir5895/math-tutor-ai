package com.backend.users.Salon.Domain;

import com.backend.users.Salon.Infrastructure.SalonRepository;
import com.backend.users.Security.Auth.DTOs.StudentDTO;
import com.backend.users.Student.DTOs.DTOStudentProfile;
import com.backend.users.Student.Domain.Student;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SalonService {

    @Autowired
    private SalonRepository salonRepository;


    public List<DTOStudentProfile> getStudentsBySalonId(Long salonId) {
        return salonRepository.findById(salonId)
                .map(salon -> salon.getStudents().stream()
                        .map(student -> convertToStudentDTO(student))
                        .toList())
                .orElseThrow(() -> new RuntimeException("Salon not found"));
    }

    private DTOStudentProfile convertToStudentDTO(Student student) {
        DTOStudentProfile studentDTO = new DTOStudentProfile();
        studentDTO.setId(student.getId());
        studentDTO.setName(student.getFirstName());
        studentDTO.setApellido(student.getLastName());
        studentDTO.setUsername(student.getEmail());
        studentDTO.setSeccion(student.getSalon().getSeccion());
        studentDTO.setSalon(student.getSalon().getGrado());
        return studentDTO;
    }

    public Integer getCantidadEstudiantes(Long salonId) {
        return salonRepository.findById(salonId)
                .map(salon -> salon.getStudents().size())
                .orElseThrow(() -> new RuntimeException("Salon not found"));
    }


}
