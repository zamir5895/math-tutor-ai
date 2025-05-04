package com.backend.users.Kafka;


import jakarta.persistence.Access;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class KafkaProducer {

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    public void timeStartUsingTheApp(UserRegisteredEvent userRegisteredEvent) {
        kafkaTemplate.send("start-time", userRegisteredEvent);
    }

    public void timeEndUsingTheApp(UserFinishedEvent userFinishedEvent) {
        kafkaTemplate.send("end-time", userFinishedEvent);
    }
}
