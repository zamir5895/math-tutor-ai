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
        System.out.println(token);

        if (token != null) {
            String jwt = token.startsWith("Bearer ") ? token.substring(7) : token;
            System.out.println("jwt " + jwt);

            try {
                if (jwt.chars().filter(ch -> ch == '.').count() == 2) {
                    String username = jwtTokenProvider.extractUsername(jwt);

                    if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                        if (jwtTokenProvider.validateToken(jwt, username)) {
                            String role = jwtTokenProvider.extractRole(jwt);

                            SimpleGrantedAuthority authority = new SimpleGrantedAuthority("ROLE_" + role);

                            UsernamePasswordAuthenticationToken authenticationToken =
                                    new UsernamePasswordAuthenticationToken(username, null, Collections.singletonList(authority));

                            SecurityContextHolder.getContext().setAuthentication(authenticationToken);
                        }
                    }
                } else {
                    System.err.println("Invalid JWT format: " + jwt);
                }
            } catch (Exception e) {
                System.err.println("Error processing JWT: " + e.getMessage());
            }
        }

        chain.doFilter(request, response);
    }
}
