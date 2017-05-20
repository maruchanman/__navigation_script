# -*- coding: utf-8 -*-
# Author: Yuta Yamashita

import pandas as pd
from .utils import *


class Selector(object):

    def __init__(self, cID, records):
        self.cID = cID
        self.records = records
        self.json_data = self.get_json()
        self.logic = self.get_logic()
        self.questions = self.get_questions()
        self.responses = self.get_responses()

    def get_json(self):
        '''
        Load json data.
        Output:
            - json data
        '''
        json_path = "./dist/" + self.cID + ".json"
        json_data = load_json(json_path)
        return json_data

    def get_logic(self):
        '''
        Load logic csv data.
        Output:
            - logic data (pandas).
        '''
        csv_path = "./logic/" + self.cID + ".csv"
        logic_data = pd.read_csv(csv_path)
        return logic_data

    def get_questions(self):
        '''
        Get questions by json data.
        Input:
            - json data
        Output:
            - questions
        '''
        questions = sorted_by_dictkey(self.json_data["questions"],
                                      "question_id")
        return questions

    def get_responses(self):
        '''
        Get responses by json data.
        Input:
            - json data
        Output:
            - responses
        '''
        responses = sorted_by_dictkey(self.json_data["response"], "response_id")
        return responses

    def select_question(self):
        '''
        Select return quesion.
        Input:
            - questions
            - available nums
        Output:
            - use question
        '''
        use_num = self.message_info[1]
        question = self.questions[use_num-1]
        return question

    def select_response(self):
        '''
        Select response by algorithm.
        Now, selected by random.
        Input:
            - responses
            - records
        Output:
            - use response
        '''
        use_num = self.message_info[1]
        response = self.responses[use_num-1]
        return response

    def make_response_message(self):
        '''
        Make json message of response.
        '''
        self.response = self.select_response()
        message = {
            "is_question": False,
            "content": {
                "question": {},
                "response": self.response
            },
            "records": self.records
        }
        message_json = json.dumps(message, ensure_ascii=False)
        return message_json

    def make_question_message(self):
        '''
        Make json message of question.
        '''
        self.question = self.select_question()
        message = {
            "is_question": True,
            "content": {
                "question": self.question,
                "response": {}
            },
            "records": self.records
        }
        message_json = json.dumps(message, ensure_ascii=False)
        return message_json

    def make_message_json(self):
        '''
        Make json data for return message.
        If message type == Q, return question message.
        Input:
            - records
            - use question
        Output:
            - message json data
        '''

        assert self.message_info[0] == "Q" or self.message_info[0] == "I",\
            "Error! Please set logic type = Q or I"

        if self.message_info[0] == "Q":
            return self.make_question_message()
        else:
            return self.make_response_message()

    def check_logic(self):
        '''
        Check logic and select next message.
        Input:
            - records
            - logic
        Output:
            - next answer type and ID
        '''
        if len(self.records) == 0:
            return ["Q", 1]
        else:
            last_q = self.records[-1][0]
            last_a = self.records[-1][1]
            set_df = self.logic[(self.logic.question == last_q) & (self.logic.answer == last_a)]
            message_info = set_df[["next_type", "next_id"]].values[0]
            return message_info

    def get_message(self):
        '''
        Main module of getting return message.
        '''
        self.message_info = self.check_logic()
        message_json = self.make_message_json()
        return message_json
