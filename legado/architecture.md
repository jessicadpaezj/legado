# Entendiendo la Arquitectura de la Aplicación

## Preguntas clave

1. ¿Cuáles son los componentes funcionales de la aplicación y cómo se relacionan entre sí?
2. ¿Cómo es el despliegue de los componentes en el entorno productivo?
3. ¿Cómo interactúan los componentes con las fuentes de datos?
4. ¿Qué patrones y tácticas de arquitectura se están utilizando?
5. ¿Qué tecnologías y frameworks forman parte de la arquitectura?
6. ¿Cuáles son los principales módulos o capas en la aplicación?
7. ¿Existen dependencias entre los servicios o microservicios?
8. ¿Cómo se gestionan la seguridad y la autenticación dentro de la aplicación?
9. ¿Existen mecanismos de escalabilidad y balanceo de carga?
10. ¿Cómo se manejan los errores y la resiliencia del sistema?
11. ¿Cómo se entienden las capas de la aplicación y cómo se manejan?
12. ¿Cómo me puedo comunicar con esta aplicación?:API? mecanismo de comunicación. Si es un api generar el código para entender cuales son los endpoints

## Respuestas

### 1. Componentes funcionales y relaciones
- **API REST y GraphQL**: Exponen endpoints para operaciones CRUD, autenticación, perfiles, artículos, comentarios y favoritos.
- **Capa de Aplicación**: Orquesta la lógica de negocio y consulta, separando comandos (escritura) y queries (lectura).
- **Capa de Dominio/Core**: Define entidades, servicios y repositorios del dominio.
- **Infraestructura**: Implementa detalles técnicos como persistencia (MyBatis), seguridad (JWT), y acceso a datos.
- **Seguridad**: Gestionada por Spring Security y JWT.

Las capas se comunican de forma jerárquica: API → Aplicación → Dominio → Infraestructura.

### 2. Despliegue en entorno productivo
- **Aplicación monolítica** empaquetada como JAR/WAR y desplegada en un contenedor Java (por ejemplo, Docker).
- **Base de datos**: SQLite por defecto, fácilmente configurable a otros motores.
- **Configuración externa**: application.properties para credenciales, claves y parámetros.

### 3. Interacción con fuentes de datos
- **MyBatis** implementa el patrón Data Mapper para desacoplar entidades de la lógica de persistencia.
- **Repositorios** en infraestructura delegan operaciones CRUD a MyBatis y exponen interfaces al dominio.

### 4. Patrones y tácticas de arquitectura
- **Domain Driven Design (DDD)**: Separación clara entre dominio, aplicación, infraestructura y API.
- **CQRS**: Separación de comandos (escritura) y queries (lectura).
- **Data Mapper**: MyBatis desacopla entidades de la base de datos.
- **Autenticación Stateless**: JWT y Spring Security.

### 5. Tecnologías y frameworks
- **Spring Boot** (Web, Security)
- **MyBatis** (persistencia)
- **Lombok** (boilerplate)
- **GraphQL** (dgs-framework de Netflix)
- **JWT** (seguridad)
- **SQLite** (por defecto)
- **Gradle** (build)

### 6. Principales módulos/capas
- **api/**: Controladores REST y GraphQL
- **application/**: Servicios de aplicación y queries
- **core/**: Entidades y lógica de dominio
- **infrastructure/**: Implementaciones técnicas (repositorios, servicios, seguridad)

### 7. Dependencias entre servicios/microservicios
- **No existen microservicios**: Es una arquitectura monolítica. Las dependencias son internas entre capas.

### 8. Seguridad y autenticación
- **Spring Security** configura endpoints públicos y protegidos.
- **JWT**: Filtro personalizado para validar tokens en cada request.
- **PasswordEncoder**: BCrypt para almacenamiento seguro de contraseñas.

### 9. Escalabilidad y balanceo de carga
- **Escalabilidad horizontal** posible desplegando múltiples instancias detrás de un balanceador externo.
- **Stateless**: Uso de JWT permite escalar sin sesión de servidor.
- **No hay balanceo de carga interno**: Se delega a la infraestructura de despliegue.

### 10. Manejo de errores y resiliencia
- **@RestControllerAdvice** y handlers para excepciones personalizadas.
- **Respuestas HTTP adecuadas** (401, 403, 404, etc.).
- **Errores de GraphQL** gestionados en los datafetchers.

### 11. Capas de la aplicación y su gestión
- **API**: Expone endpoints REST y GraphQL.
- **Aplicación**: Orquesta casos de uso y queries.
- **Dominio**: Entidades, lógica y servicios de negocio.
- **Infraestructura**: Implementaciones técnicas.
- **Gestión**: Cada capa depende solo de la inferior, siguiendo DDD.

### 12. Comunicación con la aplicación: API y endpoints
- **REST API**: Comunicación vía HTTP/JSON.
- **GraphQL API**: Comunicación vía HTTP/GraphQL en `/graphql`.

#### Ejemplo de endpoints REST principales:
```http
POST   /users            # Registro de usuario
POST   /users/login      # Login
GET    /user             # Usuario actual
PUT    /user             # Actualizar usuario
GET    /profiles/{username}         # Perfil de usuario
POST   /profiles/{username}/follow  # Seguir usuario
DELETE /profiles/{username}/follow  # Dejar de seguir
GET    /articles         # Listar artículos
POST   /articles         # Crear artículo
GET    /articles/feed    # Feed personalizado
GET    /articles/{slug}  # Detalle de artículo
PUT    /articles/{slug}  # Actualizar artículo
DELETE /articles/{slug}  # Eliminar artículo
POST   /articles/{slug}/favorite    # Marcar favorito
DELETE /articles/{slug}/favorite    # Quitar favorito
GET    /articles/{slug}/comments    # Listar comentarios
POST   /articles/{slug}/comments    # Agregar comentario
DELETE /articles/{slug}/comments/{id} # Eliminar comentario
GET    /tags            # Listar tags
```

#### Ejemplo de consulta GraphQL:
```graphql
query {
  articles(first: 10) {
    edges {
      node {
        title
        author { username }
      }
    }
  }
}
```

- **Autenticación**: Enviar JWT en el header `Authorization: Token <jwt>`.
- **Documentación**: Ver `/graphiql` para explorar el API GraphQL.
