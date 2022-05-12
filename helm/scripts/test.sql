CREATE TABLE objects (
    object_id int,
    class_id int,
    foreign key(class_id) references class(class_id)
);