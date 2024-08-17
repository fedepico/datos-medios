package com.parser.controller;

import com.parser.modelo.InformeVentasModelRecord;
import com.parser.servicio.InformeVentasServices;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("api/v1/infome-ventas")
public class InformeVentasController {

    @Autowired
    private InformeVentasServices services;

    @PostMapping("/upload")
    public ResponseEntity uploadFile(@RequestParam("file")MultipartFile file) throws IOException {
        services.saveFromFile(file);
        return ResponseEntity.ok("Archivo procesado");
    }

    @GetMapping("/data")
    public ResponseEntity<List<InformeVentasModelRecord>> allData(){
        List<InformeVentasModelRecord> data = services.allModel();
        return ResponseEntity.ok(data);
    }

}
