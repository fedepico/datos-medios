package com.parser.convertirdatos;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;

import java.io.IOException;
import java.util.List;

public class ConvertirDatos implements InterfaceConvertirDatos {

    private CsvMapper csvMapper = new CsvMapper();
    private ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public <T> List<T> obtenerDatos(String csv, Class<T> clase) {
        try {
            CsvSchema schema = csvMapper.schemaFor(clase).withHeader().withColumnSeparator(';');
            return csvMapper.readerFor(clase).with(schema).<T>readValues(csv).readAll();
        } catch (IOException ex) {
            throw new RuntimeException("Error al deserializar: " + ex.getMessage(), ex);
        }
    }

    public <T> T obtenerDatosJson(String json, Class<T> clase){
        try{
            return objectMapper.readValue(json, clase);
        }catch(JsonProcessingException ex){
            throw new RuntimeException(ex.getMessage());
        }
    }


}
