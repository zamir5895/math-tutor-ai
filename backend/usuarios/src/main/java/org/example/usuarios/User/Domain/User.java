package org.example.usuarios.User.Domain;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import java.util.Collection;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.UUID;

@Entity
@Table(name = "users")
@Inheritance(strategy = InheritanceType.JOINED)
public class User implements UserDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Rol rol;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    // Constructors
    public User() {}

    public User(String username, String passwordHash, Rol rol) {
        this.username = username;
        this.passwordHash = passwordHash;
        this.rol = rol;
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public void setUsername(String username) { this.username = username; }

    public String getPasswordHash() { return passwordHash; }
    public void setPasswordHash(String passwordHash) { this.passwordHash = passwordHash; }

    public Rol getRole() { return rol; }
    public void setRole(Rol rol) { this.rol = rol; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    // Métodos de UserDetails - ESTOS SON CRÍTICOS PARA LA AUTENTICACIÓN
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        // Convertir el único rol a una autoridad
        if (rol == null) {
            return Collections.singletonList(new SimpleGrantedAuthority("ROLE_STUDENT"));
        }
        return Collections.singletonList(new SimpleGrantedAuthority("ROLE_" + rol.name()));  // Usar el rol único
    }


    @Override
    public String getPassword() {
        return passwordHash; // Spring Security usa este método para obtener la contraseña
    }

    @Override
    public String getUsername() {
        return username; // Spring Security usa este método para obtener el username
    }

    @Override
    public boolean isAccountNonExpired() {
        return true; // La cuenta nunca expira
    }

    @Override
    public boolean isAccountNonLocked() {
        return true; // La cuenta nunca se bloquea
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true; // Las credenciales nunca expiran
    }

    @Override
    public boolean isEnabled() {
        return true; // La cuenta siempre está habilitada
    }

    // Método toString para debugging
    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", rol=" + rol +
                ", createdAt=" + createdAt +
                '}';
    }
}