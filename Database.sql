use manga;

CREATE TABLE mangas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    paginas INT NOT NULL,
    editorial VARCHAR(255)
);