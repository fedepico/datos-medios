package com.parser.modelo;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "informe_ventas")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class InformeVentasModel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_ventas;

    @Column(name = "sede")
    private String sede;

    @Column(name = "punto_de_atencion")
    private String puntoDeAtencion;

    @Column(name = "in_producto")
    private String informacionProducto;

    @Column(name = "valor_facturado")
    private Long valorFacturado;

    @Column(name = "mes")
    private Integer mes;

    @Column(name = "año")
    private Integer ano;

    @Column(name = "nombre_empresa")
    private String nombreDeEmpresa;

    @Column(name = "tipo_de_empresa")
    private String tipoDeEmpresa;

    @Column(name = "base")
    private Long base;

    @Column(name = "valor_del_iva")
    private Long valorDelIva;

    public InformeVentasModel(String sede, String puntoDeAtencion, String informacionProducto,
                              Long valorFacturado, Integer mes, Integer ano, String nombreDeEmpresa,
                              String tipoDeEmpresa, Long base, Long valorDelIva) {
        this.sede = sede;
        this.puntoDeAtencion = puntoDeAtencion;
        this.informacionProducto = informacionProducto;
        this.valorFacturado = valorFacturado;
        this.mes = mes;
        this.ano = ano;
        this.nombreDeEmpresa = nombreDeEmpresa;
        this.tipoDeEmpresa = tipoDeEmpresa;
        this.base = base;
        this.valorDelIva = valorDelIva;
    }

}
