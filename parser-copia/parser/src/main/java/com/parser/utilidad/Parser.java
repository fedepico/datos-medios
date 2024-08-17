package com.parser.utilidad;

import com.parser.modelo.InformeVentasModelRecord;
import com.parser.modelo.InformeVentasRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Service
public class Parser {

    @Autowired
    private InformeVentasRepository informeVentasRepository;

    private Boolean isFirstLine = true;

    public List<InformeVentasModelRecord> parserFileFormat(InputStream inputStream) throws IOException {

        List<InformeVentasModelRecord> registros = new ArrayList<>();

        BufferedReader bufferedReader = new BufferedReader(
                new InputStreamReader(inputStream, StandardCharsets.UTF_8)
        );

        String line;

        while((line = bufferedReader.readLine()) != null){
            // Ignora los encabezados
            if(isFirstLine){
                isFirstLine = false;
                continue;
            }

            if (line.trim().isEmpty()) continue; // Ignora líneas vacías

            var campos = line.split(";");

            try {
                // Validar y convertir campos
                String sede = campos[0];
                String puntoDeAtencion = campos[1];
                String informacionProducto = campos[2];
                Long valorFacturado = parseLongOrZero(campos[3]);
                Integer mes = parseIntegerOrZero(campos[4]);
                Integer ano = parseIntegerOrZero(campos[5]);
                String nombreDeEmpresa = campos[6];
                String tipoDeEmpresa = campos[7];
                Long base = parseLongOrZero(campos[8]);
                Long valorDelIva = parseLongOrZero(campos[9]);

                // Crear un nuevo record si todo es válido
                InformeVentasModelRecord registro = new InformeVentasModelRecord(
                     sede,
                     puntoDeAtencion,
                     informacionProducto,
                     valorFacturado,// es Long
                     mes, //es Integer
                     ano, // es Integer
                     nombreDeEmpresa,
                     tipoDeEmpresa,
                     base, // es Long
                     valorDelIva // es Long se cambio a string
                );
                registros.add(registro);
            } catch (Exception e) {
                // Manejar cualquier error de conversión o validación
                System.err.println("Error al procesar la línea: " + line);
                e.printStackTrace();
            }
        }
        return registros;
    }

    private Long parseLongOrZero(String value) {
        try {
            return Long.parseLong(value);
        } catch (NumberFormatException e) {
            return 0L; // o cualquier valor por defecto que prefieras
        }
    }

    private Integer parseIntegerOrZero(String value) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            return 0; // o cualquier valor por defecto que prefieras
        }
    }
}

