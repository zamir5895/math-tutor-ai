package org.example.usuarios.Auth;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.example.usuarios.User.Domain.User;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.List;
import java.util.UUID;

@Component
public class JwtTokenProvider {

    @Value("${app.JWT_SECRET_KEY}")
    private String jwtSecret;

    @Value("${app.JWT_EXPIRATION:86400000}")
    private long jwtExpiration; // 1 día por defecto

    public String generateToken(Authentication authentication) {
        User user = (User) authentication.getPrincipal();
        return Jwts.builder()
                .setSubject(user.getUsername())
                .claim("role", user.getRole())
                .claim("userId", user.getId().toString()) // Agregar UUID
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + jwtExpiration))
                .signWith(SignatureAlgorithm.HS512, jwtSecret)
                .compact();
    }

    public String extractRole(String token) {
        return Jwts.parser()
                .setSigningKey(jwtSecret)
                .parseClaimsJws(token)
                .getBody()
                .get("role", String.class);
    }

    public String extractUsername(String token) {
        return Jwts.parser()
                .setSigningKey(jwtSecret)
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    public UUID extractUserId(String token) {
        String userIdStr = Jwts.parser()
                .setSigningKey(jwtSecret)
                .parseClaimsJws(token)
                .getBody()
                .get("userId", String.class);
        return UUID.fromString(userIdStr);
    }

    public boolean validateToken(String token, String username) {
        return (username.equals(extractUsername(token)) && !isTokenExpired(token));
    }

    public boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }


    private Date extractExpiration(String token) {
        return Jwts.parser()
                .setSigningKey(jwtSecret)
                .parseClaimsJws(token)
                .getBody()
                .getExpiration();
    }




}