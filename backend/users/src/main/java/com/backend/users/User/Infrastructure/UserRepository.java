package com.backend.users.User.Infrastructure;

import com.backend.users.User.Domain.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository<T extends User> extends JpaRepository<T, Long> {

    Optional<T> findByEmail(String email);

    boolean existsById(Long id);

    void deleteById(Long id);

}
