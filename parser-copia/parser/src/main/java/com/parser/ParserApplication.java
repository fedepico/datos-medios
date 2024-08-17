package com.parser;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.SpringApplication;

@SpringBootApplication
public class ParserApplication /*implements CommandLineRunner*/ {

	public static void main(String[] args) {
		SpringApplication.run(ParserApplication.class, args);
	}

//	// clase asgegada paa iprimir por consola
//	@Override
//	public void run(String... args) throws IOException {
//
//		Parser parser = new Parser();
//		InputStream inputStream = new ClassPathResource("file.csv").getInputStream();
//		parser.parserFileFormat(inputStream);
//	}
}
