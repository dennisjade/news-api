import json
import re
import logging
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import json_util, ObjectId


app = Flask(__name__)
api = Api(app)

# we can put this is a config file and can autoswitch to different environment like dev, uat, prod
# but for 
uri = 'mongodb://isentia:scrapy@aws-ap-southeast-1-portal.2.dblayer.com:15424/isentia'
client = MongoClient(uri)                       #Configure the connection to the database
db = client.isentia                             #Select the database
newsdb = db.news                                #Select the collection

def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json.dumps(data, default=json_util.default)

class news(Resource):
    def get(self, keyword):
        #create a regular expression of the keyword
        regxKeyword = re.compile(keyword, re.IGNORECASE)

        #search to all fields in the document
        query = {
            '$or': [
                {'title': regxKeyword},
                {'body': regxKeyword},
                {'summary': regxKeyword}
            ]
        }
        results = newsdb.find(query)
        
        logging.info('Searching for:', keyword)
        
        json_results = []
        for result in results:
          json_results.append(result)

        response = app.response_class(
            response=toJson(json_results),
            status=200,
            mimetype='text/html'
        )
        return response

class home(Resource):
    def get(self):
        return 'Hello Isentia'

api.add_resource(news, '/news/search/<string:keyword>')
api.add_resource(home, '/')

if __name__ == '__main__':
     app.run()
