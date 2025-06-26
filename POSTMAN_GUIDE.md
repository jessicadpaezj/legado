# 🚀 Guía para Probar la API RealWorld con Postman

## 📋 **Archivos Incluidos**

1. **`RealWorld_API_Collection.json`** - Colección completa de Postman
2. **`RealWorld_Environment.json`** - Variables de entorno
3. **`POSTMAN_GUIDE.md`** - Esta guía

## 🛠️ **Configuración Inicial**

### **Paso 1: Importar la Colección**
1. Abre Postman
2. Haz clic en **"Import"**
3. Selecciona el archivo `RealWorld_API_Collection.json`
4. La colección aparecerá en tu workspace

### **Paso 2: Configurar el Entorno**
1. Haz clic en **"Import"** nuevamente
2. Selecciona el archivo `RealWorld_Environment.json`
3. En la esquina superior derecha, selecciona **"RealWorld Environment"**

### **Paso 3: Verificar Variables**
Las variables se configuran automáticamente:
- `base_url`: http://localhost:8080
- `auth_token`: (se llenará automáticamente después del login)
- `comment_id`: (se llenará cuando crees comentarios)
- `article_slug`: (se llenará cuando crees artículos)

## 🔐 **Flujo de Prueba Recomendado**

### **1. Autenticación**
```bash
# Primero ejecuta la aplicación
./gradlew bootRun
```

1. **Register User** - Crea un usuario de prueba
2. **Login User** - Inicia sesión y copia el token
3. En la variable `auth_token`, pega el token (sin "Token ")

### **2. Gestión de Usuario**
1. **Get Current User** - Verifica que el token funciona
2. **Update Current User** - Actualiza tu perfil

### **3. Artículos**
1. **Create Article** - Crea un artículo de prueba
2. **Get All Articles** - Lista todos los artículos
3. **Get Article by Slug** - Obtiene un artículo específico
4. **Update Article** - Actualiza el artículo
5. **Delete Article** - Elimina el artículo

### **4. Favoritos**
1. **Favorite Article** - Marca un artículo como favorito
2. **Unfavorite Article** - Quita de favoritos

### **5. Comentarios**
1. **Create Comment** - Crea un comentario
2. **Get Comments** - Lista comentarios
3. **Delete Comment** - Elimina un comentario

### **6. Perfiles**
1. **Get Profile** - Obtiene perfil de usuario
2. **Follow User** - Sigue a un usuario
3. **Unfollow User** - Deja de seguir

### **7. Tags**
1. **Get All Tags** - Lista todas las etiquetas

### **8. GraphQL**
1. **GraphQL Playground** - Abre el playground
2. **GraphQL Query - Get Articles** - Prueba consultas GraphQL
3. **GraphQL Query - Get Users** - Prueba más consultas

## 📝 **Ejemplos de Respuestas Esperadas**

### **Registro Exitoso (201)**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "bio": null,
    "image": null,
    "token": "eyJhbGciOiJIUzI1NiJ9..."
  }
}
```

### **Login Exitoso (200)**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "bio": null,
    "image": null,
    "token": "eyJhbGciOiJIUzI1NiJ9..."
  }
}
```

### **Artículo Creado (200)**
```json
{
  "article": {
    "id": 1,
    "slug": "test-article",
    "title": "Test Article",
    "description": "This is a test article",
    "body": "This is the body of the test article...",
    "tagList": ["java", "spring", "test"],
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T00:00:00.000Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "testuser",
      "bio": null,
      "image": null,
      "following": false
    }
  }
}
```

## 🔧 **Configuración Automática de Variables**

### **Script para Extraer Token Automáticamente**
En el request **"Login User"**, agrega este script en la pestaña **"Tests"**:

```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    const token = response.user.token;
    pm.environment.set("auth_token", token);
    console.log("Token guardado:", token);
}
```

### **Script para Extraer Article Slug**
En el request **"Create Article"**, agrega este script:

```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    const slug = response.article.slug;
    pm.environment.set("article_slug", slug);
    console.log("Article slug guardado:", slug);
}
```

### **Script para Extraer Comment ID**
En el request **"Create Comment"**, agrega este script:

```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    const commentId = response.comment.id;
    pm.environment.set("comment_id", commentId);
    console.log("Comment ID guardado:", commentId);
}
```

## 🚨 **Códigos de Estado HTTP**

- **200** - OK (Operación exitosa)
- **201** - Created (Recurso creado)
- **204** - No Content (Eliminación exitosa)
- **400** - Bad Request (Datos inválidos)
- **401** - Unauthorized (Token inválido)
- **403** - Forbidden (Sin permisos)
- **404** - Not Found (Recurso no encontrado)
- **422** - Unprocessable Entity (Validación fallida)

## 🐛 **Solución de Problemas**

### **Error 401 - Unauthorized**
- Verifica que el token esté en la variable `auth_token`
- Asegúrate de que el token no haya expirado
- Revisa que el header `Authorization` tenga el formato: `Token {{auth_token}}`

### **Error 404 - Not Found**
- Verifica que la aplicación esté corriendo en `http://localhost:8080`
- Asegúrate de que el slug del artículo sea correcto
- Revisa que el usuario exista

### **Error 422 - Validation Failed**
- Revisa el formato del JSON en el body
- Verifica que todos los campos requeridos estén presentes
- Asegúrate de que el email tenga formato válido

### **Error de Conexión**
- Verifica que la aplicación esté corriendo: `./gradlew bootRun`
- Revisa que el puerto 8080 esté disponible
- Si usas otro puerto, actualiza la variable `base_url`

## 📊 **Pruebas de Rendimiento**

### **Prueba de Carga Básica**
1. **Get All Articles** - Mide tiempo de respuesta
2. **Get Articles by Tag** - Prueba filtros
3. **Get User Feed** - Prueba con autenticación

### **Prueba de Concurrencia**
Usa la función **"Runner"** de Postman para:
- Ejecutar múltiples requests simultáneamente
- Medir tiempos de respuesta
- Identificar cuellos de botella

## 🔍 **GraphQL Testing**

### **Query Básica**
```graphql
query {
  articles(limit: 10, offset: 0) {
    id
    title
    slug
    description
    body
    author {
      id
      username
      email
    }
    tags {
      id
      name
    }
    createdAt
    updatedAt
  }
}
```

### **Query con Variables**
```graphql
query GetArticles($limit: Int, $offset: Int) {
  articles(limit: $limit, offset: $offset) {
    id
    title
    slug
  }
}
```

Variables:
```json
{
  "limit": 5,
  "offset": 0
}
```

## 🎯 **Tips y Trucos**

1. **Usa la función "Save Response"** para guardar respuestas importantes
2. **Configura "Pre-request Scripts"** para datos dinámicos
3. **Usa "Tests" scripts** para validaciones automáticas
4. **Organiza requests en folders** por funcionalidad
5. **Usa variables de entorno** para diferentes ambientes (dev, staging, prod)

## 📚 **Recursos Adicionales**

- [Documentación de Postman](https://learning.postman.com/)
- [RealWorld API Spec](https://github.com/gothinkster/realworld)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)

---

¡Con esta colección podrás probar completamente la API RealWorld! 🚀 