delete BoundingBox from Objects inner join BoundingBox on BoundingBox.object_id = Objects.object_id where recording_id = 1;
delete Tracjectory from Objects inner join Tracjectory on Tracjectory.object_id = Objects.object_id where recording_id = 1;
delete Location from Objects inner join Location on Location.object_id = Objects.object_id where recording_id = 1;
delete Class from Objects inner join Class on Class.object_id = Objects.object_id where recording_id = 1;
delete Objects from Objects where Objects.recording_id = 1;
delete Frame from Frame where Frame.recording_id = 1;
delete Recording from Recording where Recording.recording_id = 1;




delimiter |

Create Event testevent 
ON SCHEDULE EVERY 7 DAY
DO
BEGIN
    select GROUP_CONCAT(recording_id) into @recording_id from Recording where date_recorded < now() - INTERVAL 1 day; 
    delete BoundingBox from Objects inner join BoundingBox on BoundingBox.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Tracjectory from Objects inner join Tracjectory on Tracjectory.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Location from Objects inner join Location on Location.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Class from Objects inner join Class on Class.object_id = Objects.object_id where FIND_IN_SET(recording_id,@recording_id);
    delete Objects from Objects where FIND_IN_SET(recording_id,@recording_id);
    delete Frame from Frame where FIND_IN_SET(recording_id,@recording_id);
    delete Recording from Recording where FIND_IN_SET(recording_id,@recording_id);

END |

delimiter ;
