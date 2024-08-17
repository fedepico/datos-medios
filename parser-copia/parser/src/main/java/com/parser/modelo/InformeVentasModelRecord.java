package com.parser.modelo;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public record InformeVentasModelRecord(
        @JsonAlias("sede") String sede,
        @JsonAlias("pnto_atncn") String puntoDeAtencion,
        @JsonAlias("ln_prdct") String informacionProducto,
        @JsonAlias("vlr_factrdo") Long valorFacturado,// es Long
        @JsonAlias("mes") Integer mes, //es Integer
        @JsonAlias("año") Integer ano, // es Integer
        @JsonAlias("empresa") String nombreDeEmpresa,
        @JsonAlias("tp_empresa") String tipoDeEmpresa,
        @JsonAlias("base") Long base, // es Long
        @JsonAlias("vlr_iva") Long valorDelIva // es Long se cambio a string
) {}
