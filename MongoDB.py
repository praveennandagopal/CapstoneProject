import streamlit as st
import json
from googleapiclient.discovery import build
from pymongo import MongoClient 
import json
import datetime
import pandas as pd
import re
import Sql as sqlFile

def apiConnection():    
    _apiKey = "AIzaSyCza79IynWTLQ-bxDLC8L4qYw1A0C6cFt8"
    _service = build('youtube','v3',developerKey=_apiKey)
    return _service

def mongoCollection():      
    mongoDBcon = MongoClient(mongoDBConnectionString)    
    database = mongoDBcon["ABCD"]
    collection = database["ABCD"]
    return collection
    
def MongodbCall(channelId):
    collection = mongoCollection()    
    if collection.find_one({'ChannelDetails.Channel_Id':channelId }):
        return False
    else:        
        return True  



service  = apiConnection()
st.header('YouTube API ', divider='rainbow')
_channelId= st.text_input("Please Enter Channel ID")
mongoDBConnectionString = "mongodb://localhost:27017"


# def searchResult() :
#     request= service.search().list(part="id,snippet",q =_channelName,maxResults= 1)
#     response = request.execute()
#     return response

def getChannelDetails(channelId):        
    request= service.channels().list(part="snippet,contentDetails,statistics",id = channelId)
    response = request.execute()
    data ={
        'Channel_Id':response['items'][0]['id'] ,
        'Channel_Name': response['items'][0]['snippet']['title'],
        'Channel_Description': response['items'][0]['snippet']['description'],
        'Channel_Views': response['items'][0]['statistics']['viewCount'],
        'Subscription_Count':response['items'][0]['statistics']['subscriberCount'] ,
        'Channel_VideoCount':response['items'][0]['statistics']['videoCount'],
        'PlayList_Id':response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    }
    return data
def getPlayListDetails(channelId): 
     request = service.playlists().list(
        part="snippet,contentDetails",
        channelId=channelId,
        maxResults=50
    )
     response = request.execute()
     for item in response['items']: 
        data ={
        'Channel_Id':item['snippet']['channelId'] ,
        'PlayList_Name': item['snippet']['title'],        
        'PlayList_Id':item['id']
        }
        playListDetailList.append(data)
    
def getVideoList(playListId) : 
    request= service.playlistItems().list(part="snippet,contentDetails",maxResults=50,playlistId = playListId)
    response = request.execute()
    for item in response['items']: 
        videoId= item['contentDetails']['videoId']
        videolst.append(videoId)
        video_ids = ",".join(videolst)
    return response 

def getVideoDetailsList(videosIDList) : 
    request= service.videos().list(part="snippet,contentDetails,statistics",id = videosIDList)
    response = request.execute()
    tags =response['items'][0]['snippet']['tags']
    data = {
            'Video_Id':response['items'][0]['id'],
            'Video_Name':response['items'][0]['snippet']['title'],
            'Video_Description':response['items'][0]['snippet']['description'],
            'Tags':",".join(tags),
            'PublishedAt':response['items'][0]['snippet']['publishedAt'],
            'View_Count':response['items'][0]['statistics']['viewCount'] ,
            'Like_Count':response['items'][0]['statistics']['likeCount'] ,
            'Comment_Count':response['items'][0]['statistics']['commentCount'],
            'Favorite_Count':response['items'][0]['statistics']['favoriteCount'],
            'Duration':convertDuration(response['items'][0]['contentDetails']['duration']),
            'Caption_Status':response['items'][0]['contentDetails']['caption'],
            'Thumbnail':response['items'][0]['snippet']['thumbnails'] ['standard']['url'],
            'Channel_Id':response['items'][0]['snippet']['channelId']                
        }  
    return data
   


def getVideoListNextPageToken(playListId,nextPageToken) : 
    request= service.playlistItems().list(part="snippet,contentDetails",maxResults=50,pageToken =nextPageToken, playlistId = playListId)
    response = request.execute()
    for item in response['items']: 
        videoId= item['contentDetails']['videoId']
        videolst.append(videoId)
        video_ids = ",".join(videolst)
    return response 
 
def convertDuration(duration):
    s = duration
    hrs = re.findall(r"(\d+)H", s)
    min = re.findall(r"(\d+)M", s)
    sec = re.findall(r"(\d+)S", s)
    PT = 0
    if hrs:
        PT = int(hrs[0]) *3600 +PT    
    if min:
        PT = PT + int(min[0])*60   
    if sec:
        PT = PT + int(sec[0]) 
    return PT
    
def getComments(videoID):
    
    request= service.commentThreads().list(part="snippet,replies",maxResults=1, videoId= videoID)
    response = request.execute()
    comments = response
    for item in comments['items']:
        topleveldata = {
            'Comment_Text':item['snippet']['topLevelComment']['snippet']['textDisplay'],
            'Comment_Id':item['snippet']['topLevelComment']['id'],
            'Comment_Author':item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            'Comment_PublishedAt':item['snippet']['topLevelComment']['snippet']['publishedAt'],
            'Video_Id':item['snippet']['topLevelComment']['snippet']['videoId']
            }
        commentsDetailList.append(topleveldata)

  
# def getCommentsReplies(threadId):
#     request = service.comments().list(part="snippet,id", maxResults=1,parentId=threadId)
#     response = request.execute()
    
# def setComments(comments):
#     for item in comments['items']:
#         topleveldata = {
#             'Comment_Text':item['snippet']['topLevelComment']['snippet']['textDisplay'],
#             'Comment_Id':item['snippet']['topLevelComment']['id'],
#             'Comment_Author':item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
#             'Comment_PublishedAt':item['snippet']['topLevelComment']['snippet']['publishedAt'],
#             'Video_Id':item['snippet']['topLevelComment']['snippet']['videoId']
#             }
       
#         commentsDetailList.append(topleveldata)
#         # if item['snippet']['totalReplyCount'] > 0:
#         #     _threadIdJson = getCommentsReplies(item['snippet']['topLevelComment']['id'])
#         #     for replyComments in _threadIdJson['items']: 
#         #         replies = {
#         #         'Comment_Text':replyComments['snippet']['textDisplay'],
#         #         'Comment_Id':replyComments['id'],
#         #         'Comment_Author':replyComments['snippet']['authorDisplayName'],
#         #         'Comment_PublishedAt':replyComments['snippet']['publishedAt']
#         #         }
#         #         commentsDetailList.append(replies)


creating_DB = st.button("Send To MongoDB")


if(creating_DB):
    
    if _channelId !="":        
        
        checkChannel = MongodbCall(_channelId)
        if checkChannel:
           
            _channelDetailsList = getChannelDetails(_channelId)
            playListDetailList=[]
            getPlayListDetails(_channelId)
        
            videolst = []
            validVideoIds=[]
            _videoListJson = getVideoList(_channelDetailsList['PlayList_Id']) 
            while 'nextPageToken' in _videoListJson:
                _videoListJson = getVideoListNextPageToken(_channelDetailsList['PlayList_Id'],_videoListJson['nextPageToken'])
            _videoDetailsList =[]
            
            for ids in videolst:
                try:
                    _videoDetailsJson = getVideoDetailsList(ids)            
                    _videoDetailsList.append(_videoDetailsJson)
                    validVideoIds.append(ids)
                except:
                    continue         
            
            commentsDetailList=[]
            
            for item in validVideoIds:
                try:
                    setComments = getComments(item)
                    
                except:
                    continue
                
            dict={
                'ChannelDetails' : _channelDetailsList,
                'PlayListDetails' :playListDetailList,
                'VideosDetailsList':_videoDetailsList,
                'CommentsDetailsList':commentsDetailList
            }
           
            collection = mongoCollection()
            collection.insert_one(dict)
            st.write(":green[Channel Inserted Successfully]")
        else:
            st.write(":red[Channel Already existed]")
    
    else:
        st.write(":red[Please Enter Youtube Name]")
   

choices =[]

for i in mongoCollection().find():
    choices.append(i["ChannelDetails"]["Channel_Name"])      
      
option = st.selectbox(
'Which one like to be Migrate to MongoDB?',
(choices))
  

if st.button("Migrate MongoDB to SQL") : 
    if option != "":       
        data = mongoCollection().find_one({'ChannelDetails.Channel_Name':option })          
        id = data["ChannelDetails"]["Channel_Id"]
        tblCreation = sqlFile.dataBaseCreation(data,id)               
st.header('SQL Query ', divider='rainbow')
try:
        ques = {
        1:"What are the names of all the videos and their corresponding channels?",
        2:"Which channels have the most number of videos, and how many videos do they have?",
        3:"What are the top 10 most viewed videos and their respective channels?",
        4:"How many comments were made on each video, and what are their corresponding video names?",
        5:"Which videos have the highest number of likes, and what are their  corresponding channel names?",
        6:"What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
        7:"What is the total number of views for each channel, and what are their  corresponding channel names?",
        8:"What are the names of all the channels that have published videos in the year 2022?",
        9:"What is the average duration of all videos in each channel, and what are their corresponding channel names?",
        10:"Which videos have the highest number of comments, and what are their corresponding channel names?"
        }
        listQues = list(ques.values())
        option = st.selectbox(
        'Please Select A Question One at a time?',
        (listQues))
        
        for key, value in ques.items():
            if option == value:                
                Ques=sqlFile.question(key)  
                st.write(":green[Records Present in Below Table is ]",len(Ques))
                st.write(Ques)
                
except:  
        st.write(":red[There is No Tables in SQL]")  


