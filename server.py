#!flask/bin/python
from flask import Flask , jsonify, render_template, request, Response,json,current_app
from flask.ext.restful import Api, MethodView, fields, marshal, reqparse
from flask.ext.httpauth import HTTPBasicAuth
from cros import *
import sqlscript, urllib

''' Youtube Video Listings main module. It constructs and handles requests.
	GET requests are returned as json files
'''
auth = HTTPBasicAuth()

app = Flask(__name__ , static_url_path = "")
api = Api(app)


class VideoListAPI(MethodView):

    def get(self ):
    	data=sqlscript.getItems()
    	return Response(json.dumps(data),  mimetype='application/json')
    	

    def post(self):
    	id=request.json['url']
    	video_url=id
    	
    	id=id.split("v=",1)
    	id=id[1].split("&",1)
    	id=id[0]
    	
    	url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id
    	data = json.load(urllib.urlopen(url))
    	title = data['entry']['title']['$t']
    	description = data['entry']['media$group']['media$description']['$t']							
    	
    	sqlscript.pushItems(title,description,video_url)
    	return Response(status=200, mimetype='application/json')

    def delete(self,video_id):
    	data=sqlscript.deleteItems(str(video_id))
    	return Response(json.dumps(data),  mimetype='application/json')
    	


VideoList_view = VideoListAPI.as_view('VideoList_api')
app.add_url_rule('/video/',view_func=VideoList_view, methods=['GET','POST','OPTIONS'])
app.add_url_rule('/video/<video_id>',view_func=VideoList_view, methods=['DELETE'])




if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
