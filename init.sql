-- 1) Creación de base de datos
CREATE DATABASE my_collections;

-- 2) Creación de tablas
CREATE TABLE my_movies (
    ID SERIAL PRIMARY KEY,         -- Campo ID, autoincrementable
    Autor VARCHAR(100),            -- Campo Autor, cadena de texto
    Descripcion TEXT,              -- Campo Descripción, texto largo
    Fecha_Estreno DATE             -- Campo Fecha de Estreno, tipo fecha
);

-- 3) Inserción de registros de prueba a la tabla creada
INSERT INTO my_movies (Autor, Descripcion, Fecha_Estreno)
VALUES 
    ('Steven Spielberg', 'Raiders of the Lost Ark', '1981-06-12'),
    ('Christopher Nolan', 'Inception', '2010-07-16'),
    ('Quentin Tarantino', 'Django Unchained', '2012-08-17'),
    ('James Cameron', 'Titanic', '1997-12-19'),
    ('Ridley Scott', 'Blade Runner', '1982-06-25');