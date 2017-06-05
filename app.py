import json
import re
import logging
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import json_util, ObjectId


app = Flask(__name__)
api = Api(app)

uri = 'mongodb://isentia:scrapy@aws-ap-southeast-1-portal.2.dblayer.com:15424/isentia'
client = MongoClient(uri)                   #Configure the connection to the database
db = client.isentia                         #Select the database
newsdb = db.news                              #Select the collection

def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json.dumps(data, default=json_util.default)

class news(Resource):
    def get(self, keyword):
        regxKeyword = re.compile(keyword, re.IGNORECASE)
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
            mimetype='application/json'
        )
        return response
 
api.add_resource(news, '/news/search/<string:keyword>')

if __name__ == '__main__':
     app.run()
