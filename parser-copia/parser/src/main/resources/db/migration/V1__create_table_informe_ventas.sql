-- Crear una tabla de informe ventas

CREATE TABLE informe_ventas (
    id_ventas BIGINT AUTO_INCREMENT PRIMARY KEY,
    sede VARCHAR(50),
    punto_de_atencion VARCHAR(50),
    in_producto VARCHAR(100),
    valor_facturado BIGINT,
    mes INT,
    año INT,
    nombre_empresa VARCHAR(100),
    tipo_de_empresa VARCHAR(100),
    base BIGINT,
    valor_del_iva BIGINT
);
