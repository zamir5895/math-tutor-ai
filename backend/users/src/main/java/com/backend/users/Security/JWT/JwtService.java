package com.backend.users.Security.JWT;


import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.exceptions.JWTDecodeException;
import com.backend.users.User.Domain.UserService;
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import jakarta.annotation.PostConstruct;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.util.Date;

@Service
public class JwtService {

    @Value("${JWT_SECRET_KEY}")
    private String secretKey;

    private Algorithm algorithm;

    private final UserService userService;


    public JwtService(UserService userService){
        this.userService = userService;
    }

    @PostConstruct
    public void init(){
        this.algorithm = Algorithm.HMAC256(secretKey);
    }


    public String extractUsername(String token) {
        try {
            return JWT.decode(token).getSubject();
        } catch (JWTDecodeException e) {
            return null;
        }
    }

    public String extractRole(String token) {
        try {
            return JWT.decode(token).getClaim("role").asString();
        } catch (JWTDecodeException e) {
            return null;
        }
    }


    public String generatetoken(UserDetails data){
        Date now = new Date();
        Date expiration = new Date(now.getTime()+1000*60*60*24);

        Algorithm algorithm = Algorithm.HMAC256(secretKey);
        return JWT.create()
                .withSubject(data.getUsername())
                .withClaim("role", data.getAuthorities().toArray()[0].toString())
                .withIssuedAt(now)
                .withExpiresAt(expiration)
                .sign(algorithm);
    }
    public void validateToken(String token, String userEmail) throws AuthenticationException {
        Algorithm algorithm = Algorithm.HMAC256(secretKey);
        JWT.require(algorithm).build().verify(token);
        UserDetails userDetails = userService.userDetailsService().loadUserByUsername(userEmail);

        SecurityContext context = SecurityContextHolder.createEmptyContext();

        UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                userDetails,
                token,
                userDetails.getAuthorities()
        );

        context.setAuthentication(authToken);
        SecurityContextHolder.setContext(context);
    }


    public void invalidateToken() {
        SecurityContextHolder.clearContext();
    }
    public Date getExpirationTime(String token) {
        try {
            return JWT.decode(token).getExpiresAt();
        } catch (JWTDecodeException e) {
            throw new EntityNotFoundException("Invalid or malformed token");
        }
    }


}
