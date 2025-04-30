package com.backend.users;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
public class HealthController {


    @RequestMapping("/health")
    public String health() {
        return "OK";
    }

    @RequestMapping("/status")
    public String status() {
        return "it's working";
    }
}
