package org.example.usuarios.Auth;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.web.filter.OncePerRequestFilter;
import org.springframework.stereotype.Component;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class JwtRequestFilter extends OncePerRequestFilter {

    private final JwtTokenProvider jwtTokenProvider;

    public JwtRequestFilter(JwtTokenProvider jwtTokenProvider) {
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        final String token = request.getHeader("Authorization");

        if (token != null && token.startsWith("Bearer ")) {
            String jwt = token.substring(7);  // Extraer JWT del header
            String username = jwtTokenProvider.extractUsername(jwt);

            if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                if (jwtTokenProvider.validateToken(jwt, username)) {
                    // Extraer el único rol del JWT
                    String role = jwtTokenProvider.extractRole(jwt);  // Método para extraer el único rol del token

                    // Convertir el rol a SimpleGrantedAuthority
                    SimpleGrantedAuthority authority = new SimpleGrantedAuthority("ROLE_" + role);

                    // Crear el token de autenticación con el único rol
                    UsernamePasswordAuthenticationToken authenticationToken =
                            new UsernamePasswordAuthenticationToken(username, null, Collections.singletonList(authority));

                    // Establecer el contexto de seguridad
                    SecurityContextHolder.getContext().setAuthentication(authenticationToken);
                }
            }
        }

        // Continuar con la cadena de filtros
        chain.doFilter(request, response);
    }

}
