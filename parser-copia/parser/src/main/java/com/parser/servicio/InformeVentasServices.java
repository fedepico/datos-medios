package com.parser.servicio;

import com.parser.modelo.InformeVentasModelRecord;
import com.parser.modelo.InformeVentasRepository;
import com.parser.modelo.InformeVentasModel;
import com.parser.utilidad.Parser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.stereotype.Service;

import java.util.stream.Collectors;
import java.io.IOException;
import java.util.List;

@Service
public class InformeVentasServices {

    @Autowired
    private InformeVentasRepository repository;

    @Autowired
    private Parser parser;

    public void saveFromFile(MultipartFile file) throws IOException{
        List<InformeVentasModelRecord> registros = parser.parserFileFormat(file.getInputStream());

        List<InformeVentasModel> model = registros.stream()
                .map(this::convertToModel)
                .collect(Collectors.toList());
        repository.saveAll(model);
    }

    public List<InformeVentasModelRecord> allModel(){
        List<InformeVentasModel> data = repository.findAll();
        return data.stream()
                .map(this::convertToRecord)
                .collect(Collectors.toList());
    }

    private InformeVentasModelRecord convertToRecord(InformeVentasModel model) {
        return new InformeVentasModelRecord(
                model.getSede(),
                model.getPuntoDeAtencion(),
                model.getInformacionProducto(),
                model.getValorFacturado(),
                model.getMes(),
                model.getAno(),
                model.getNombreDeEmpresa(),
                model.getTipoDeEmpresa(),
                model.getBase(),
                model.getValorDelIva()
        );
    }

    private InformeVentasModel convertToModel(InformeVentasModelRecord record) {
        return new InformeVentasModel(
                record.sede(),
                record.puntoDeAtencion(),
                record.informacionProducto(),
                record.valorFacturado(),
                record.mes(),
                record.ano(),
                record.nombreDeEmpresa(),
                record.tipoDeEmpresa(),
                record.base(),
                record.valorDelIva()
        );
    }

}
