import sqlite3 
from flask import Response

db = sqlite3.connect(':memory:', check_same_thread=False)

cursor = db.cursor()
try:
	cursor.execute('''
		CREATE TABLE videos(id INTEGER PRIMARY KEY, title VARCHAR,description VARCHAR, url VARCHAR) ''')
	db.commit()
except Exception as e:
	pass
	


def getItems(video_id ='all'):
	if video_id=='all':
		cursor.execute('''SELECT * FROM videos''')
		data=cursor.fetchall()
		return(data)
	else:
		cursor.execute('''SELECT * FROM videos WHERE id=?''', (video_id))
		data=cursor.fetchall()
		return(data)

def pushItems(video_title, video_description, video_url):
	cursor.execute('''INSERT INTO videos (title, description, url) 
		VALUEs(?,?,?)''', (video_title, video_description, video_url))
	db.commit()
	return 

def deleteItems(video_id):
	cursor.execute('''DELETE FROM videos WHERE id =? ''', (video_id))
	db.commit()
	return

pushItems("Game of Thrones","what everybody should whatch","http://got.com")

