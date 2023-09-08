import streamlit as st
from pymongo import MongoClient 
import pandas as pd
import sqlalchemy as sa
import mysql.connector    


myHost ="localhost"
myUser="root"
myPassword = "password"
myDatabaseName = "myYoutubeChannel"

try:
  engine =sa.create_engine("mysql+mysqlconnector://{}:{}@{}/{}".format(myUser,myPassword,myHost,myDatabaseName),echo=False)
  alchemyconnection = engine.connect()
except:
  st.write("")
  
mydb = mysql.connector.connect(
host=myHost,
user=myUser,
password=myPassword
)

def dataBaseCreation(data,id): 
  mydb._execute_query('''Create Database If Not Exists {}'''.format(myDatabaseName))
  mydb._execute_query('''USE {}'''.format(myDatabaseName))
  tableCreation(data,id)
  
  
def tableCreation(data,id):  
  query ='''CREATE TABLE if not exists ChannelDetails (
	Channel_Id	varchar (255) Not null,
	Channel_Name	varchar(255) Not null,
	Channel_Description	longtext,
	Channel_Views	int Not null,
	Subscription_Count	int Not null,
	Channel_VideoCount	int Not null,
  PlayList_Id varchar(255) Not null,
	PRIMARY KEY(Channel_Id))'''
  mydb._execute_query(query)
  mydb.commit()
  
  query ='''CREATE TABLE if not exists PlayListDetails (
	Channel_Id	varchar (255) Not null,
	PlayList_Name	varchar(255) Not null,	
  PlayList_Id varchar(255) Not null,
  FOREIGN KEY (Channel_Id) REFERENCES ChannelDetails(Channel_Id),
	PRIMARY KEY(PlayList_Id))'''
  mydb._execute_query(query)
  mydb.commit()
  
  Videoquery ='''CREATE TABLE if not exists VideoDetails (
	Video_Id	varchar(255) Not null,
	Video_Name	longtext Not null,
	Video_Description	longtext,
	Tags	longtext ,
  PublishedAt	datetime Not null,
	View_Count	int Not null,
	Like_Count	int Not null,
	Comment_Count	int Not null,
  Favorite_Count	int Not null,
	Duration	int Not null,
	Caption_Status	varchar(255),
	Thumbnail	longtext not null,
  Channel_Id varchar(255) Not null,
  FOREIGN KEY (Channel_Id) REFERENCES ChannelDetails(Channel_Id),
  PRIMARY KEY(Video_Id))'''	
  mydb._execute_query(Videoquery)
  mydb.commit()
 
  commentquery ='''CREATE TABLE if not exists CommentDetails (
	Comment_Text	longtext Not null,
	Comment_Id	varchar(255) Not null,
	Comment_Author	varchar(255),
	Comment_PublishedAt	datetime Not null,
  Video_Id	varchar(255) Not null,
  FOREIGN KEY (Video_Id) REFERENCES VideoDetails(Video_Id),
  PRIMARY KEY(Comment_Id))'''	
  mydb._execute_query(commentquery)
  mydb.commit()
  
  countTbl = checkTable(id)  
  if len(countTbl) == 1:
        st.write(":red[This Channel Already exist]")    
  else:
        channelTbl(data)
        

def channelTbl(data): 
  ChannelDetails= data['ChannelDetails']    
  ChannelList =pd.DataFrame([ChannelDetails])
  ChannelList = ChannelList.astype({'Channel_Views':int,'Subscription_Count':int,'Channel_VideoCount':int})
  ChannelList.to_sql('channelDetails',engine, if_exists='append', index= False)
  playListTbl(data)
  videoTbl(data)

def playListTbl(data): 
  PlayListDetails= data['PlayListDetails']   
  PlayListDetails =pd.DataFrame(PlayListDetails)
  PlayListDetails = PlayListDetails.astype(str)  
  PlayListDetails.to_sql('PlayListDetails',engine, if_exists='append', index= False)
  
  
  
def videoTbl(data):
  VideoDetails= data['VideosDetailsList']
  videosList=pd.DataFrame(VideoDetails)  
  videosList = videosList.astype({'View_Count':int,'Like_Count':int,'Comment_Count':int,'Favorite_Count':int,'Duration':int})
  videosList['PublishedAt'] = pd.to_datetime(videosList['PublishedAt'])  
  videosList.to_sql("videoDetails",engine, if_exists='append', index= False) 
  commentTbl(data)
  
  
  
def commentTbl(data):     
  commentDetails= data['CommentsDetailsList']
  commentsList = pd.DataFrame(commentDetails)
  commentsList['Comment_PublishedAt'] = pd.to_datetime(commentsList['Comment_PublishedAt'])
  commentsList.to_sql("commentDetails",engine, if_exists='append', index= False)
  st.write("Table Created Succcessfully")

def checkTable(Id):
      query ='''select * from channeldetails where channel_Id ='{}'  limit 1 '''.format(Id)
      df = pd.read_sql_query(query,engine)
      return df


def question(quesNum):
      if quesNum == 1:
        myQuery='''SELECT channelDetails.Channel_Name, videoDetails.Video_Name
        FROM videoDetails
        INNER JOIN channelDetails ON videoDetails.Channel_Id=channelDetails.Channel_Id;'''
        df = pd.read_sql_query(myQuery, engine)
        return df
      if quesNum == 2:
          myQuery='''SELECT Channel_name,Channel_VideoCount FROM channelDetails   
          WHERE channel_VideoCount = (SELECT MAX(channel_VideoCount) FROM channelDetails)'''
          df = pd.read_sql_query(myQuery, engine)
          return df
      if quesNum == 3:
          myQuery='''SELECT channelDetails.Channel_Name, Video_Name,View_Count from VideoDetails 
          INNER JOIN channelDetails ON videoDetails.Channel_Id=channelDetails.Channel_Id
          order by View_Count desc LIMIT 10'''
          df = pd.read_sql_query(myQuery, engine)
          return df
      if quesNum == 4:
          myQuery='''SELECT Comment_Count, Video_Name from VideoDetails order by Comment_Count desc'''
          df = pd.read_sql_query(myQuery, engine)
          return df
      if quesNum == 5:
            myQuery='''SELECT channelDetails.Channel_Name,Video_Name, like_count from VideoDetails 
            INNER JOIN channelDetails ON videoDetails.Channel_Id=channelDetails.Channel_Id
            order by like_count desc limit 1'''
            df = pd.read_sql_query(myQuery, engine)
            return df
      if quesNum == 6:
            myQuery='''SELECT Video_Name, like_count from VideoDetails order by like_count desc'''
            df = pd.read_sql_query(myQuery, engine)
            return df
      if quesNum == 7:
            myQuery='''SELECT Channel_Views, Channel_Name  from channelDetails order by Channel_Views desc'''
            df = pd.read_sql_query(myQuery, engine)
            return df
      if quesNum == 8:
            myQuery='''SELECT 
                    ChannelDetails.Channel_Name  
                    FROM ChannelDetails
                    WHERE ChannelDetails.Channel_Id IN (SELECT Channel_Id from VideoDetails
                    Where Year(PublishedAt) ='2022' 
                    group by Channel_Id)'''
            df = pd.read_sql_query(myQuery, engine)
            return df
      if quesNum == 9:
            myQuery='''SELECT channelDetails.Channel_Name ,avg(Duration) as AverageDuration
                        FROM videoDetails
                        INNER JOIN channelDetails ON videoDetails.Channel_Id=channelDetails.Channel_Id
                        group by videoDetails.Channel_Id'''
            df = pd.read_sql_query(myQuery, engine)
            return df
      if quesNum == 10:
            myQuery='''SELECT channelDetails.Channel_Name, Comment_Count, Video_Name from VideoDetails
            INNER JOIN channelDetails ON videoDetails.Channel_Id=channelDetails.Channel_Id
            order by Comment_Count desc LIMIT 1'''
            df = pd.read_sql_query(myQuery, engine)
            return df

          
            




