CREATE DATABASE testdb;
USE testdb;

CREATE TABLE Recording (
    recording_id int NOT NULL AUTO_INCREMENT,
    date_recorded datetime,
    recording_location varchar(120),
    primary key(recording_id)
);

CREATE TABLE Frame (
    frame_id int NOT NULL AUTO_INCREMENT,
    frametime timestamp(3),
    recording_id int,
    frame_index int,
    foreign key (recording_id) references Recording(recording_id),
    primary key (frame_id)
);

CREATE TABLE Objects (
    object_id int NOT NULL AUTO_INCREMENT,
    object_instance_id int,
    recording_id int,
    foreign key(recording_id) references Recording(recording_id),
    primary key(object_id)
);

CREATE TABLE Class(
    class_id int NOT NULL AUTO_INCREMENT,
    object_id int,
    frame_id int, 
    id int, 
    foreign key (object_id) references Objects(object_id),
    foreign key (frame_id) references Frame(frame_id),
    primary key (class_id)
);

CREATE TABLE BoundingBox (
    bbox_id int NOT NULL AUTO_INCREMENT,
    object_id int,
    frame_id int,
    point_cnt int,
    dir_x_bbox float,
    dir_y_bbox float,
    height float,
    width float,
    length float,
    foreign key (object_id) references Objects(object_id),
    foreign key (frame_id) references Frame(frame_id),
    primary key (bbox_id)
);

CREATE TABLE Location (
    location_id int NOT NULL AUTO_INCREMENT,
    object_id int,
    frame_id int,
    coord_x float,
    coord_y float,
    coord_z float,
    distance float,
    longitude double,
    latitude double,
    elevation float,
    foreign key (object_id) references Objects(object_id),
    foreign key (frame_id) references Frame(frame_id),
    primary key (location_id)
);

CREATE TABLE Trajectory (
    trajectory_id int NOT NULL AUTO_INCREMENT,
    object_id int,
    frame_id int,
    speed_x float,
    speed_y float,
    speed float,
    foreign key (object_id) references Objects(object_id),
    foreign key (frame_id) references Frame(frame_id),
    primary key (trajectory_id)
);


delimiter |

Create Event testevent 
ON SCHEDULE EVERY 7 DAY
DO
BEGIN
    select GROUP_CONCAT(recording_id) into @recording_id from Recording where date_recorded < now() - INTERVAL 1 day; 
    delete BoundingBox from Objects inner join BoundingBox on BoundingBox.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Trajectory from Objects inner join Trajectory on Trajectory.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Location from Objects inner join Location on Location.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Class from Objects inner join Class on Class.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Objects from Objects where FIND_IN_SET(recording_id,@recording_id);
    delete Frame from Frame where FIND_IN_SET(recording_id,@recording_id);
    delete Recording from Recording where FIND_IN_SET(recording_id,@recording_id);

END |

delimiter ;