drop user 'klient'@'localhost';
drop user 'pracownik'@'localhost';
drop user 'db_admin'@'localhost';

create user 'klient'@'localhost';
create user 'pracownik'@'localhost' identified by 'pracownik';
create user 'db_admin'@'localhost' identified by 'admin';


#Granty

grant ALL on kino.* to db_admin
	with grant option;

grant insert on kino.klienci to 'klient'@'localhost';
grant select, insert, delete, update on kino.klienci to 'pracownik'@'localhost';

grant insert, select, update, delete on kino.filmy to 'pracownik'@'localhost';
grant select on kino.filmy to 'klient'@'localhost';

grant insert, select, delete, update, trigger on kino.projekcje to 'pracownik'@'localhost';
grant select on kino.projekcje to 'klient'@'localhost';

grant insert, select, update, delete on kino.rezerwacje to 'pracownik'@'localhost', 'klient'@'localhost';

grant insert, select, delete, update on kino.sale to 'pracownik'@'localhost';
grant select on kino.sale to 'klient'@'localhost';
