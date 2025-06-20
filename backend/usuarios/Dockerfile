FROM openjdk:17-jdk-slim
ARG JAR_FILE=target/usuarios-0.0.1-SNAPSHOT.jar
COPY ${JAR_FILE} usuarios_app.jar
EXPOSE 8090
ENTRYPOINT ["java", "-jar", "usuarios_app.jar"]