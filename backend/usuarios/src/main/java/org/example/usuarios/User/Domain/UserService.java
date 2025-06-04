package org.example.usuarios.User.Domain;

import org.example.usuarios.User.Infraestructure.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class UserService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    // Método requerido por UserDetailsService - ESTE ES CRÍTICO PARA EL LOGIN
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("Usuario no encontrado: " + username));

        // Debug: verificar que el usuario se encuentra correctamente
        System.out.println("Usuario encontrado: " + user.getUsername());
        System.out.println("Rol del usuario: " + user.getRole());

        return user; // User implementa UserDetails
    }

    // Métodos de gestión de usuarios
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public Optional<User> getUserById(UUID id) {
        return userRepository.findById(id);
    }

    public Optional<User> getUserByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    // Este método encripta la contraseña - usar solo cuando ya tienes el hash
    public User saveUser(User user) {
        if (!isPasswordEncrypted(user.getPasswordHash())) {
            user.setPasswordHash(passwordEncoder.encode(user.getPasswordHash()));
        }
        return userRepository.save(user);
    }

    // Método para registro - NO encripta porque ya viene encriptado
    public User registerUser(User user) {
        return userRepository.save(user);
    }

    // Método para crear usuario con contraseña en texto plano
    public User createUserWithPlainPassword(User user, String plainPassword) {
        user.setPasswordHash(passwordEncoder.encode(plainPassword));
        return userRepository.save(user);
    }

    public boolean existsByUsername(String username) {
        return userRepository.existsByUsername(username);
    }

    public void deleteUser(UUID id) {
        userRepository.deleteById(id);
    }

    // Método auxiliar para verificar si la contraseña ya está encriptada
    private boolean isPasswordEncrypted(String password) {
        // BCrypt hashes typically start with $2a$, $2b$, or $2y$ and are 60 characters long
        return password != null && password.startsWith("$2") && password.length() == 60;
    }

    // Método para verificar contraseña (útil para debugging)
    public boolean checkPassword(String rawPassword, String encodedPassword) {
        return passwordEncoder.matches(rawPassword, encodedPassword);
    }
}