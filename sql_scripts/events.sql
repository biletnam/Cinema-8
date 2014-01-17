use cinema;

drop event delete_clients;
drop event delete_movies;
drop event delete_projections;
drop event delete_reservations;
drop function check_projection_date;
drop trigger projection_date_insert;
drop trigger projection_date_update;

create event if not exists delete_clients on SCHEDULE EVERY 1 DAY STARTS TIMESTAMP('2014-01-15 05:00:00', '05:00:00') do
    delete from cinema.employee_app_client
        where id not in (
            select client_id 
            from employee_app_reservation
            where projection_id in (
                select projection_id
                from employee_app_projection
                where date_time >= NOW() 
                )
            );


create event if not exists delete_movies on SCHEDULE EVERY 1 DAY STARTS TIMESTAMP('2014-01-15 05:00:00', '05:02:00') do
    delete from cinema.employee_app_movie
        where id not in (
            select movie_id 
            from employee_app_projection
            where date_time >= NOW()
                
            );


create event if not exists delete_projections on SCHEDULE EVERY 5 MINUTE  do
    delete from cinema.employee_app_projection
    where date_time < NOW();
                

create event if not exists delete_reservations on SCHEDULE EVERY 5 MINUTE do
    delete from cinema.employee_app_reservation
        where received=false and projection_id in (
            select projection_id
            from employee_app_projection
            where date_time < TIMESTAMPADD(MINUTE, 30, NOW())
            );


DELIMITER //
create function check_projection_date(d DATETIME, movie_length INT, room_num INT)
RETURNS INT
    BEGIN
        DECLARE fetched_movie_id INT;
        DECLARE fetched_movie_length INT DEFAULT 0;
        DECLARE done INT DEFAULT FALSE;
        DECLARE fetched_date_time DATETIME;
        DECLARE time_dif DATETIME;

        DECLARE proj_cur CURSOR FOR select date_time, movie_id from employee_app_projection where room_id = room_num;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

        IF d <= NOW() THEN
            RETURN -1;
        END IF;
        
        OPEN proj_cur;

        proj_cur_loop: LOOP
            FETCH proj_cur INTO fetched_date_time, fetched_movie_id;
            
            IF done THEN
                LEAVE proj_cur_loop;
            END IF;

            IF fetched_date_time < d THEN
                SET fetched_movie_length = (select length from employee_app_movie where id = fetched_movie_id);
                SET time_dif = TIMESTAMPADD(MINUTE, fetched_movie_length, fetched_date_time);
                
                IF d <= time_dif THEN
                    CLOSE proj_cur;
                    RETURN fetched_movie_id;
                END IF;
            
            ELSE
                SET time_dif = TIMESTAMPADD(MINUTE, movie_length, d);
                
                IF time_dif >= fetched_date_time THEN
                    CLOSE proj_cur;
                    RETURN fetched_movie_id;
                END IF;
            
            END IF;
        END LOOP;
        
        CLOSE proj_cur;
        RETURN 0;
    END //
DELIMITER ;

 

DELIMITER //
create trigger projection_date_insert before insert on employee_app_projection
    FOR EACH ROW
    BEGIN
        DECLARE status INT DEFAULT 0;
        DECLARE movie_length INT DEFAULT 0;

        SET movie_length = (SELECT length from employee_app_movie where id = NEW.movie_id);

        SET status = check_projection_date(NEW.date_time, movie_length, NEW.room_id);

        IF status < 0 THEN
            signal sqlstate '45000' set message_text = "You've insertet date that was in the past";
        END IF;

        IF status > 0 THEN
            signal sqlstate '45000' set message_text = "Your projection is in conflict with other movie, change the date of this projection";

        END IF;

    END //

DELIMITER ;


DELIMITER //
create trigger projection_date_update before update on employee_app_projection
    FOR EACH ROW
    BEGIN
        DECLARE status INT DEFAULT 0;
        DECLARE movie_length INT DEFAULT 0;

        SET movie_length = (SELECT length from employee_app_movie where id = NEW.movie_id);

        SET status = check_projection_date(NEW.date_time, movie_length, NEW.room_id);

        IF status < 0 THEN
            signal sqlstate '45000' set message_text = "You've insertet date that was in the past";
        END IF;

        IF status > 0 THEN
            signal sqlstate '45000' set message_text = "Your projection is in conflict with other movie, change the date of this projection";

        END IF;

    END //

DELIMITER ;


