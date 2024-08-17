package com.parser.convertirdatos;

import java.io.InputStream;
import java.util.List;

public interface InterfaceConvertirDatos {
    <T> List<T> obtenerDatos(String csv, Class<T> clase);
    <T> T obtenerDatosJson(String json, Class<T> clase);

}
