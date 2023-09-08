
**Title:**
	**YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit****

**Description:**
	This is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
		-Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, 		 likes, comments of each video) using Google API.
		-Option to store the data in a MongoDB database as a data lake.
		-Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
		-Option to select a channel name and migrate its data from the data lake to a SQL database as tables.
		-Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.
		
**Built With:**
	Streamlit
	Python
	MongoDB
	MYSql
	
**Prerequist:**
	VsCode - Need to Install (or any other source code editor which Supports Python)
	MongoDBCompass - Need to Install
	MySql - Need to install
	Youtube API Key
	
**Objective:**
	To develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, 
	stores it in a MongoDB database, migrates it to a SQL data warehouse, 
	and enables users to search for channel details and join tables to view data in the Streamlit app.
	
**RoadMap:**
	**stage1**:Based on channel ID get all the Details(Channel Details, Videos Details, Comment Details) in JSON format
	**stage2**:Based on Selected Channel ID need to insert as a Document in MongoDB 
	**stage3**:Based on Selected Channel Name need to Migrate the Document from MongoDB to MySql
	**stage4**:Retrieve data from the SQL database using different search options Questions Listed below

**Required NPM packages:**
	install Python
	import build from googleapiclient.discovery - "For API Call with YOUTUBE"
	import MongoClient from pymongo "To Connect with MongoDB"
	import streamlit "For User Interface"

**Changes need to be Done in SourceCode File:**
	**Sql.py:**
		myHost ="localhost" => mySql server name
		myUser="root" => mySql Username
		myPassword = "password" => mySql Password
		myDatabaseName = "xxxx" => mySql Databasename		
	**MongoDB.py:**
		provide _apiKey = "AIzaSxxxxxxxxxxxxxxxxxxxxxxxxxt8"
		mongoDBConnectionString = "mongodb://localhost:27017" => MongoDB connection string
		either we can Use standalone MongoDBCompass or Online MongoDB Atlas Database

**How to Run Application:**
	1) cd "file_path/MongoDB.py" 

**Questions:**

		1)What are the names of all the videos and their corresponding channels?
		2)Which channels have the most number of videos, and how many videos do
			they have?
		3)What are the top 10 most viewed videos and their respective channels?
		4)How many comments were made on each video, and what are their
			corresponding video names?
		5)Which videos have the highest number of likes, and what are their 
			corresponding channel names?
		6)What is the total number of likes and dislikes for each video, and what are 
			their corresponding video names?
		7)What is the total number of views for each channel, and what are their 
			corresponding channel names?
		8)What are the names of all the channels that have published videos in the year
			2022?
		9)What is the average duration of all videos in each channel, and what are their 
			corresponding channel names?
		10)Which videos have the highest number of comments, and what are their 
			corresponding channel names?
