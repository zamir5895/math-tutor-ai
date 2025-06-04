package org.example.usuarios.Admin.Domain;

import org.example.usuarios.Admin.Infraestructure.AdminRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class AdminService {

    @Autowired
    private AdminRepository adminRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public List<Admin> getAllAdmins() {
        return adminRepository.findAll();
    }

    public Optional<Admin> getAdminById(UUID id) {
        return adminRepository.findById(id);
    }

    public Admin saveAdmin(Admin admin) {
        admin.setPasswordHash(passwordEncoder.encode(admin.getPasswordHash()));
        return adminRepository.save(admin);
    }

    public void deleteAdmin(UUID id) {
        adminRepository.deleteById(id);
    }

    public Admin updateAdmin(UUID id, Admin adminDetails) {
        Optional<Admin> optionalAdmin = adminRepository.findById(id);
        if (optionalAdmin.isPresent()) {
            Admin admin = optionalAdmin.get();
            admin.setUsername(adminDetails.getUsername());
            if (adminDetails.getPasswordHash() != null && !adminDetails.getPasswordHash().isEmpty()) {
                admin.setPasswordHash(passwordEncoder.encode(adminDetails.getPasswordHash()));
            }
            return adminRepository.save(admin);
        }
        return null;
    }
}

