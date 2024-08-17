# Proyecto Parser de Ventas

Este proyecto es una aplicación de Spring Boot que permite subir archivos CSV con datos de ventas y almacenarlos en una base de datos MySQL. El proyecto incluye la capacidad de cargar datos desde un archivo CSV, convertir estos datos en un formato adecuado y almacenarlos en una base de datos, así como consultar estos datos a través de una API REST.

## Estructura del Proyecto

- **`ParserApplication.java`**: Clase principal de la aplicación.
- **`InformeVentasModel.java`**: Entidad JPA que mapea la tabla `informe_ventas` en la base de datos.
- **`InformeVentasModelRecord.java`**: Record de datos que representa el formato del archivo CSV.
- **`InformeVentasServices.java`**: Servicio para manejar la lógica de negocio relacionada con los datos de ventas.
- **`InformeVentasController.java`**: Controlador REST que expone endpoints para subir archivos y consultar datos.

## Configuración del Proyecto

### Archivo `application.properties`

```properties
# Nombre de la aplicación
spring.application.name=msvc-ventas

# Configuración de la base de datos
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/ventas
spring.datasource.username=tu_username
spring.datasource.password=tu_password

# Configuración de JPA e Hibernate
spring.jpa.hibernate.ddl-auto=update

# Configuración de Flyway
spring.flyway.enabled=true
spring.flyway.baseline-on-migrate=true

# Activar el modo de depuración
spring.debug=true

# Habilitar colores ANSI en la salida de la consola
spring.output.ansi.enabled=always

### Archivo `application.properties`
```
## Configuración de Variables de Entorno

Para poder compilar y ejecutar este proyecto Java Spring Boot, es necesario configurar las variables de entorno que proporcionan las credenciales de acceso a la base de datos. Estas variables son utilizadas por la configuración de `spring.datasource.username` y `spring.datasource.password` en el archivo de propiedades de la aplicación.

### Variables de Entorno Requeridas

1. **MYSQL_USERNAME**: Define el nombre de usuario para conectarse a la base de datos MySQL.
2. **MYSQL_PASSWORD**: Define la contraseña del usuario para conectarse a la base de datos MySQL.

### Configuración de las Variables de Entorno

#### En Linux/MacOS

Para establecer las variables de entorno, abre una terminal y ejecuta los siguientes comandos:

```bash
export MYSQL_USERNAME=tu_usuario
export MYSQL_PASSWORD=tu_contraseña
```

## Endpoints
### Subir archivo CSV
`http://localhost:8080/api/v1/infome-ventas/upload`
- HOST: `localhost`
- PORT: `8080`
- URL: `/api/v1/informe_ventas/upload` 
- Método: `POST`
- Parámetros: `file` tipo `MultipartFile`: Archivo CSV con los datos de ventas.
- Respuesta `200 OK`: Archivo procesado.

### Consultar Datos
`http://localhost:8080/api/v1/infome-ventas/data`
- HOST: `localhost`
- PORT: `8080`
- URL: `/api/v1/informe_ventas/data`
- Método: `GET`
- Respuesta `200 OK`: Archivo procesado.
  
```
  [
    {
        "sede": "SQL SIMENS",
        "puntoDeAtencion": "ADMINISTRACION",
        "informacionProducto": "SOPORTE",
        "valorFacturado": 165648,
        "mes": 2,
        "ano": 2023,
        "nombreDeEmpresa": "IPS OIMOS",
        "tipoDeEmpresa": "Centros Rehabilitación",
        "base": 139200,
        "valorDelIva": 26448
    }
]
```
### Requisitos
- `Java 22`
- `Spring Boot 3.x`
- `MySQL 8x`
- `Flyway`: Migracion Base de Datos.
