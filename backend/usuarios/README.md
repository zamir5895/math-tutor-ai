# Getting Started

Java 17 
variables de entorno que use de ejemplo:
JWT_EXPIRATION=86400000;JWT_SECRET_KEY=myVeryLongSecretKeyThatIsAtLeast64CharactersLongForHS512AlgorithmToEnsureSecurityAndPreventErrors;KAFKA_BOOTSTRAP_SERVERS=localhost:9092;SPRING_DATASOURCE_PASSWORD=a;SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/mibasedatos;SPRING_DATASOURCE_USERNAME=miusuario

tienes que crear la base de datos mibasedatos en postgre y un usuario: miusuario con contraseña: a depende de ti en realidad tendrías que editer las variables de entorno en caso quieras usar otrso nombres el JWT secret key recomiendo buscar en linea un generador largo  sino no funciona

tambien hay para probar las apis en postman

Lo de abajo es relleno



### Reference Documentation

For further reference, please consider the following sections:

* [Official Apache Maven documentation](https://maven.apache.org/guides/index.html)
* [Spring Boot Maven Plugin Reference Guide](https://docs.spring.io/spring-boot/3.5.0/maven-plugin)
* [Create an OCI image](https://docs.spring.io/spring-boot/3.5.0/maven-plugin/build-image.html)
* [Spring Data JPA](https://docs.spring.io/spring-boot/3.5.0/reference/data/sql.html#data.sql.jpa-and-spring-data)
* [Spring Web](https://docs.spring.io/spring-boot/3.5.0/reference/web/servlet.html)

### Guides

The following guides illustrate how to use some features concretely:

* [Accessing Data with JPA](https://spring.io/guides/gs/accessing-data-jpa/)
* [Building a RESTful Web Service](https://spring.io/guides/gs/rest-service/)
* [Serving Web Content with Spring MVC](https://spring.io/guides/gs/serving-web-content/)
* [Building REST services with Spring](https://spring.io/guides/tutorials/rest/)

### Maven Parent overrides

Due to Maven's design, elements are inherited from the parent POM to the project POM.
While most of the inheritance is fine, it also inherits unwanted elements like `<license>` and `<developers>` from the
parent.
To prevent this, the project POM contains empty overrides for these elements.
If you manually switch to a different parent and actually want the inheritance, you need to remove those overrides.

