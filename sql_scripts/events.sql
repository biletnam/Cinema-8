use cinema;

drop event delete_clients;
drop event delete_movies;
drop event delete_projections;
drop event delete_reservations;

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
