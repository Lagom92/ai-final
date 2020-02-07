from flask import Flask, render_template, request
from flask_restful import Resource, abort, Api, reqparse
from flask_cors import CORS
import tensorflow as tf
import sqlite3
import os
import numpy as np

from flask import g
from flask import Flask, render_template, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter

import data
import model as ml
from configs import DEFINES

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

# slack 연동 정보 입력 부분
SLACK_TOKEN = "xoxb-728026288049-734244769025-K6y6Amjuqiga0LVVfJDKgiVP"
SLACK_SIGNING_SECRET = "5fc4b1c88e0683e61a748a4a0280cc48"

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def predict(query):
    char2idx,  idx2char, _ = data.load_voc()
    predic_input_enc, _ = data.enc_processing([query], char2idx)
    predic_output_dec, _ = data.dec_output_processing([""], char2idx)
    predic_target_dec = data.dec_target_processing([""], char2idx)

    predictor_fn = tf.contrib.predictor.from_saved_model(
            export_dir="./data_out/model/1569981326"
        )
        
    predictions = predictor_fn({'input':predic_input_enc, 'output':predic_output_dec, 'target':predic_target_dec})
    answer = data.model_pred(predictions, idx2char)
    return answer


def insertDB(q, a):
    conn = sqlite3.connect('./db/app.db')
    cur = conn.cursor()
    cur.execute("insert into thinkB (question, answer) values (:question, :answer)", {'question': q, 'answer': a})
    conn.commit()
    conn.close()


def getDB():
    conn = sqlite3.connect('./db/app.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM thinkB ORDER BY created_datetime DESC LIMIT 10")
    datas = cur.fetchall()

    conn.commit()
    conn.close()

    return datas


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    text = " ".join(text.split()[1:])
    
    answer = predict(text)

    slack_web_client.chat_postMessage(
            channel=channel,
            text=answer,
        )

    return True

class Declaration(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question', type=str)
            parser.add_argument('answer', type=str)
            args = parser.parse_args()
            _question = args['question']
            _answer = args['answer']

            insertDB(_question, _answer)

            datas = {
                'flag': True,
                'message': "Save Success"
            }

            return datas

        except Exception as e:

            datas = {
                'flag': False,
                'answer': str(e)
            }
            
            return datas
            
    def get(self):
        try:
            data_list = getDB()

            datas = {
                'flag': True,
                'datas': data_list
            }

            return datas
        
        except Exception as e:

            datas = {
                'flag': False,
                'answer': str(e)
            }
            
            return datas

class Chat(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question', type=str)

            args = parser.parse_args()

            _question = args['question']
            _answer = predict(_question)

            datas = {
                'flag': True,
                'answer': _answer
            }
            
            return datas

        except Exception as e:
            datas = {
                'flag': False,
                'answer': str(e)
            }
            return datas


api.add_resource(Declaration, '/Declaration')
api.add_resource(Chat, '/chat')


@app.route("/", methods=["GET"])
def index():
    return render_template('readme.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
