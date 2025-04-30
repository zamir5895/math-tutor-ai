package com.backend.users.User.Domain;


import com.backend.users.Profesor.Domain.Professor;
import com.backend.users.Profesor.Infrastructure.ProfessorRepository;
import com.backend.users.Student.Infrastructure.StudentRepository;
import com.backend.users.User.Infrastructure.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private UserRepository<User> userRepository;

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private ProfessorRepository professorRepository;

    public User findByEmail(String email,String role){
        User user;
        if(role.equals("ROLE_STUDENT")) {
            user = studentRepository.findByEmail(email).orElseThrow(() -> new UsernameNotFoundException("User not found"));
        }
        else if(role.equals("ROLE_PROFESSOR")) {
            user = professorRepository.findByEmail(email).orElseThrow(() -> new UsernameNotFoundException("User not found"));
        }
        else{
            user = userRepository.findByEmail(email).orElseThrow(() -> new UsernameNotFoundException("User not found"));
        }
        return user;
    }


    @Bean(name="UserDetailsService")
    public UserDetailsService userDetailsService() {
        return username -> {
            User user = userRepository
                    .findByEmail(username)
                    .orElseThrow(() -> new UsernameNotFoundException("User not found"));
            return (UserDetails) user;
        };
    }
}
