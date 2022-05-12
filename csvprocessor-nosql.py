from pandas import read_csv
import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime
import pymongo
import uuid

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]
objects = mydb['objects']
frames = mydb['frames']
recording = mydb['recording']
recording_id = str(uuid.uuid1())

df = read_csv('2021-12-8-17-0-0_cl.csv')

recording_row = recording.insert_one({'recording_id':recording_id})

currentFrameIndex = None
objectRows = []
df = df.sort_values(by='FrameIndex')
# this may not insert the last row
for index, row in df.iterrows():
    # check if frame exists 
    '''if currentFrameIndex != row["FrameIndex"]:
        #print(row['FrameIndex'])
        if len(objectRows) > 0:
            print (len(objectRows))
            objects.insert_many(objectRows)
            
            print('insert many')
        objectRows = []
        frame = frames.find_one({"frame_id":row["FrameIndex"],'recording_id':recording_id})
        
        if frame == None:
            frame = frames.insert_one({"frame_id":row["FrameIndex"],'recording_id':recording_id})
            frame_id = frame.inserted_id
        else:
            frame_id = frame['_id']
        currentFrameIndex = row["FrameIndex"]'''

    objectsRow = {}

    objectsRow['ObjectID'] = int(row['ObjectID'])
    #objectsRow['frame_uuid'] = frame_id
    objectsRow["Frame_id"] = row['FrameIndex']
    objectsRow["recording_id"] = recording_id
    objectsRow['class'] = row['Class']
    objectsRow['bbox'] = {'point_cnt' : row['Point_Cnt'], 'dir_y_bbox' : row['Dir_Y_Bbox'], 'dir_x_bbox' : row['Dir_X_Bbox'], 'height' : row['Height'], 'width' : row['Width'], 'length' : row['Length']}
    objectsRow['location'] = {'coord_x' : row['Coord_X'], 'coord_y' : row['Coord_Y'], 'coord_z' :row['Coord_Z'], 'distance' : row['Distance'], 'longitude' : row['Longitude'], 'latitude' : row['Latitude'], 'elevation' : row['Elevation']}
    objectsRow['trajectory'] = {'speed_x' : row['Speed_X'], 'speed_y' : row['Speed_Y'], 'speed' : row['Speed(m/s)']}
    #test = objects.insert_one(objectsRow)
    #print(test.inserted_id)
    #print('row inserted')
    objectRows.append(objectsRow)

    '''print(index,row)
    #print(row['FrameIndex'])
    print(row['ObjectID'])
    print(row['Coord_X'])
    print(row['Coord_Y'])
    print(row['Coord_Z'])
    print(row['Distance'])
    print(row['Speed_X'])
    print(row['Speed_Y'])
    print(row['Speed(m/s)'])
    print(row['Longitude'])
    print(row['Latitude'])        
    print(row['Elevation'])     
    print(row['Point_Cnt'])       
    print(row['Dir_X_Bbox'])       
    print(row['Dir_Y_Bbox'])      
    print(row['Height'])           
    print(row['Length'])         
    print(row['Width'])           
    print(row['Area'])             
    print(row['Class'])            
    #print(row[])'''


# sql metadata
# no sql contains the data
# :D:D:D

if len(objectRows) > 0:
    objects.insert_many(objectRows)
    print("inserted")
