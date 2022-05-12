'''
    Name: csvprocessorsql.py
    Author: Chase Carthen
    Description: The following file takes trajectory and inputs it into a mysql database. 
    Dependencies: pandas, sqlalchemy
'''
from pandas import read_csv
import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime
import re
from io import StringIO

def parseFileName(filename):
    datestart = datetime.datetime.now()
    match = re.search('([0-9][0-9][0-9][0-9])-([0-9]+)-([0-9]+)-([0-9]+)-([0-9]+)-([0-9]+)', filename)
    print(match)
    if match != None:
        datestart = datetime.datetime.strptime(match[0], '%Y-%m-%d-%H-%M-%S')
    return datestart

def importCSVToMySQL(csvfilename='', csvstring='', datestart=datetime.datetime.now(), location='Virginia and 15th', userName='', password='', server='localhost:5000', databaseName='testdb', framesPerSecond=10):
    databaseString = 'mysql+pymysql://%s:%s@%s/%s' % (userName,password,server,databaseName)
    if csvfilename == '' and csvstring =='':
        return False
    
    # parse date from file name if it can be done
    if csvfilename != '':
        datestart = parseFileName(csvfilename)
        df = read_csv(csvfilename)
    else:
        df = read_csv(StringIO(csvstring))
    framesPerSecond = framesPerSecond if framesPerSecond > 0 else 10
    # connect to database and load metaclasses 
    engine = db.create_engine(databaseString)
    session = Session(engine)
    metadata = db.MetaData()
    objects = db.Table('Objects', metadata, autoload=True, autoload_with=engine)
    recording = db.Table('Recording', metadata, autoload=True, autoload_with=engine)
    Base = automap_base(metadata=metadata)
    Base.prepare(engine, reflect=True)
    Recording = Base.classes.Recording
    Class = Base.classes.Class
    Frame = Base.classes.Frame
    Objects = Base.classes.Objects
    BoundingBox = Base.classes.BoundingBox
    Location = Base.classes.Location
    Trajectory = Base.classes.Trajectory

    


    recording = Recording()
    recording.date_recorded = datestart
    recording.recording_location = location

    session.add(recording)
    session.commit()

    # enumerate all frames and objects
    
    objects = df['ObjectID'].unique()
    objects.sort()
    frames = df['FrameIndex'].unique()
    frames.sort()

    framesdb = []
    for frameIndex in frames:
        frame = Frame(recording_id = recording.recording_id, frame_index = frameIndex, frametime = datestart + datetime.timedelta(seconds= frameIndex * 1.0/framesPerSecond))
        session.add(frame)
        framesdb.append(frame)
    session.commit()

    frameMap = {}

    for framedb in framesdb:
        frameMap[framedb.frame_index] = framedb.frame_id

    objectMap = {}

    Classes = []
    BBoxes = []
    Locations = []
    Trajectories = []
    for objectID in objects:
        objectinstance = Objects(object_instance_id=objectID, recording_id = recording.recording_id)
        session.add(objectinstance)
        objectMap[objectID] = objectinstance
    session.commit()

    for objectID in objects:
        objectid = objectMap[objectID].object_id
        
        # class
        frames = df[df['ObjectID'] == objectID]['FrameIndex'].values
        classes = df[df['ObjectID'] == objectID]['Class'].values
        
        # bbox
        pointcnt = df[df['ObjectID'] == objectID]['Point_Cnt'].values
        dirxbox = df[df['ObjectID'] == objectID]['Dir_X_Bbox'].values
        dirybox = df[df['ObjectID'] == objectID]['Dir_Y_Bbox'].values
        height = df[df['ObjectID'] == objectID]['Height'].values
        width = df[df['ObjectID'] == objectID]['Width'].values
        length = df[df['ObjectID'] == objectID]['Length'].values

        # trajectory
        speedx = df[df['ObjectID'] == objectID]['Speed_X'].values
        speedy = df[df['ObjectID'] == objectID]['Speed_Y'].values
        speed = df[df['ObjectID'] == objectID]['Speed(m/s)'].values

        # location
        coordx = df[df['ObjectID'] == objectID]['Coord_X'].values
        coordy = df[df['ObjectID'] == objectID]['Coord_Y'].values
        coordz = df[df['ObjectID'] == objectID]['Coord_Z'].values
        distance = df[df['ObjectID'] == objectID]['Distance'].values
        longitude = df[df['ObjectID'] == objectID]['Longitude'].values
        latitude = df[df['ObjectID'] == objectID]['Latitude'].values
        elevation = df[df['ObjectID'] == objectID]['Elevation'].values


        for index in range(len(classes)):
            frameid = frameMap[frames[index]]
            Classes.append(Class(id=classes[index], frame_id=frameid, object_id=objectid))
            BBoxes.append(BoundingBox(frame_id = frameid, object_id = objectid, point_cnt = pointcnt[index], dir_x_bbox=dirxbox[index], dir_y_bbox=dirybox[index], height=height[index], width=width[index], length=length[index]))
            Locations.append(Location(frame_id=frameid, object_id = objectid, coord_x = coordx[index], coord_y = coordy[index], coord_z=coordz[index], distance=distance[index], longitude=longitude[index], latitude=latitude[index],elevation=elevation[index]))
            Trajectories.append(Trajectory(frame_id=frameid, object_id = objectid, speed_x = speedx[index], speed_y = speedy[index], speed = speed[index]))

    for index in range(len(Classes)):
        session.add(Classes[index])
        session.add(BBoxes[index])
        session.add(Locations[index])
        session.add(Trajectories[index])

    session.commit()
    return True

#importCSVToMySQL('./2021-12-8-17-0-0_cl.csv')

