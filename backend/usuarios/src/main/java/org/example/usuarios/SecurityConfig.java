package org.example.usuarios;

import org.example.usuarios.Auth.JwtRequestFilter;
import org.example.usuarios.User.Domain.UserService;
import org.springframework.context.annotation.Bean;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private final JwtRequestFilter jwtRequestFilter;

    public SecurityConfig(JwtRequestFilter jwtRequestFilter) {
        this.jwtRequestFilter = jwtRequestFilter;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(HttpSecurity http, UserService userService) throws Exception {
        AuthenticationManagerBuilder authBuilder =
                http.getSharedObject(AuthenticationManagerBuilder.class);
        authBuilder
                .userDetailsService(userService)
                .passwordEncoder(passwordEncoder());
        return authBuilder.build();
    }


    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.csrf(csrf -> csrf.disable())
                .cors(cors -> cors.configurationSource(corsConfigurationSource()))  // Configuración CORS
                .authorizeHttpRequests(auth ->
                        // Rutas públicas

                        auth.requestMatchers("/auth/login").permitAll()
                                .requestMatchers("/profesor/register").permitAll()
                                .requestMatchers("/alumno/register").permitAll()
                                .requestMatchers("/health").permitAll()

                                // Rutas solo para ADMIN
                                .requestMatchers("/salon/admin_only/**").hasAuthority("ROLE_ADMIN")
                                .requestMatchers("/profesor/admin_only/**").hasAuthority("ROLE_ADMIN")
                                .requestMatchers("/alumno/admin_only/**").hasAnyAuthority("ROLE_ADMIN")
                                .requestMatchers("/admin/**").hasAuthority("ROLE_ADMIN")

                                .requestMatchers("/salon/profesor/**").hasAuthority("ROLE_TEACHER")
                                .requestMatchers("/profesor/**").hasAnyAuthority("ROLE_ADMIN", "ROLE_TEACHER")

                                .requestMatchers("/salon/**").hasAnyAuthority("ROLE_ADMIN", "ROLE_TEACHER")
                                .requestMatchers("/seccion/**").hasAnyAuthority("ROLE_ADMIN", "ROLE_TEACHER")
                                .requestMatchers("/alumno/studentbyId/**").hasAnyAuthority("ROLE_ADMIN", "ROLE_TEACHER")
                                .requestMatchers("/alumno/student/**").hasAnyAuthority("ROLE_STUDENT")
                                .requestMatchers("/alumno/salon/**").hasAnyAuthority("ROLE_ADMIN", "ROLE_STUDENT", "ROLE_TEACHER")
                                .requestMatchers("/alumno/**").hasAnyAuthority("ROLE_ADMIN", "ROLE_STUDENT", "ROLE_TEACHER")


                                // Cualquier otra solicitud debe estar autenticada
                                .anyRequest().authenticated()
                )
                .sessionManagement(session -> session
                        .sessionCreationPolicy(SessionCreationPolicy.STATELESS)  // Configuración sin estado (sin sesión)
                );

        // Añadir el filtro JWT antes de otros filtros
        http.addFilterBefore(jwtRequestFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

    @Bean
    public UrlBasedCorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of(
                "http://localhost:5173",
                "http://frontend-matemix.s3-website-us-east-1.amazonaws.com",
                "https://frontend-matemix-dn8rvqqt7-zamir5895s-projects.vercel.app/",
                "https://frontend-matemix-pink.vercel.app/",
                "http://52.206.13.161:5173",
                "http://learning-with-matemix.s3-website-us-east-1.amazonaws.com/"
        ));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L); // Caché de preflight

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }


}
