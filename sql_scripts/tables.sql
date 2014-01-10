drop database kino;

create database kino;

USE kino;

create table klienci (
    id_klienta INT UNSIGNED NOT NULL AUTO_INCREMENT,
    imie VARCHAR(20) NOT NULL,
    nazwisko VARCHAR(30) NOT NULL,
    telefon INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY(id_klienta)
);


create table filmy (
    id_filmu SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    tytul VARCHAR(100) NOT NULL,
    czas_trwania SMALLINT UNSIGNED NOT NULL,
    min_wiek TINYINT UNSIGNED DEFAULT NULL,
    gatunek VARCHAR(30),
    audio VARCHAR(15) DEFAULT 'Angielski',
    napisy VARCHAR(15) DEFAULT '',
    PRIMARY KEY(id_filmu)
);


create table sale (
    nr_sali TINYINT UNSIGNED NOT NULL,
    ilosc_miejsc TINYINT UNSIGNED NOT NULL,
    status VARCHAR(10) CHECK(status in ('Aktywna', 'Nieczynna')),
    PRIMARY KEY(nr_sali)
);

create table projekcje (
    id_projekcji INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_filmu SMALLINT UNSIGNED NOT NULL,
    nr_sali TINYINT UNSIGNED NOT NULL,
    data_godz TIMESTAMP NOT NULL,
    cena_biletu SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY(id_projekcji),
    CONSTRAINT projekcje_fk_sala FOREIGN KEY(nr_sali) REFERENCES sale(nr_sali) on DELETE CASCADE, 
    CONSTRAINT projekcje_fk_film FOREIGN KEY(id_filmu) REFERENCES filmy(id_filmu) on DELETE CASCADE,
    CONSTRAINT unq_film_sala_data UNIQUE(id_filmu, nr_sali, data_godz)
);


create table rezerwacje (
    nr_rezerwacji INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nr_miejsca SMALLINT UNSIGNED NOT NULL,
    id_klienta INT UNSIGNED NOT NULL,
    id_projekcji INT UNSIGNED NOT NULL,
    PRIMARY KEY(nr_rezerwacji),
    CONSTRAINT rezerwacje_fk_klient FOREIGN KEY(id_klienta) REFERENCES klienci(id_klienta) on DELETE CASCADE,
    CONSTRAINT rezerwacje_fk_projekcja FOREIGN KEY(id_projekcji) REFERENCES projekcje(id_projekcji) on DELETE CASCADE,
    CONSTRAINT rezerwacje_unique UNIQUE(nr_miejsca, id_projekcji)
);

#pomyśleć nad tym co powinno być z rezerwacjami gdy usunie się projekcję lub film!!!!!!!!!!

#event usuwający dane klientów którzy nie mają rezerwacji w przyszłości
#event usuwający filmy, które nie mają projekcji w przyszłości
#triger przy insercie do sprawdzania czy w danym dniu o danej godzinie w danej sali może być projekcja (cjodzi o to żeby kolejna projekcja nie była rozpoczynana w trakcie trwania filmu)
#event usuwający zakończone projekcje
#event usuwajacy rezerwacje nieodebrane na 30 min przed rozpoczeciem seansu

