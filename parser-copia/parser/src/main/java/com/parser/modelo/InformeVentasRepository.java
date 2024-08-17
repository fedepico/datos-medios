package com.parser.modelo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface InformeVentasRepository extends JpaRepository<InformeVentasModel, Long> {
}
