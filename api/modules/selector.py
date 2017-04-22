# -*- coding: utf-8 -*-
# Author: Yuta Yamashita

from utils import *


class Selector(object):

    def __init__(self, cID, records):
        self.cID = cID
        self.records = records
        self.json_data = self.get_json()
        self.threshold = self.get_threshold()
        self.questions = self.get_questions()
        self.items = self.get_items()

    def get_json(self):
        '''
        Load json data.
        Output:
            - json data
        '''
        json_path = "../dist/" + self.cID + ".json"
        json_data = load_json(json_path)
        return json_data

    def get_threshold(self):
        '''
        Get threshold by json data.
        Input:
            - json data
        Output:
            - threshold
        '''
        threshold = self.json_data["question_threshold"]
        return threshold

    def get_questions(self):
        '''
        Get questions by json data.
        Input:
            - json data
        Output:
            - questions
        '''
        questions = sorted_by_dictkey(self.json_data["questions"], "question_id")
        return questions

    def get_items(self):
        '''
        Get items by json data.
        Input:
            - json data
        Output:
            - items
        '''
        items = sorted_by_dictkey(self.json_data["items"], "item_id")
        return items

    def select_question(self):
        '''
        Select return quesion.
        Now, selected by random.
        Input:
            - questions
            - available nums
        Output:
            - use question
        '''
        import random
        use_num = random.choice(self.available_nums)
        question = self.questions[use_num-1]
        return question

    def select_item(self):
        '''
        Select item by algorithm.
        Now, selected by random.
        Input:
            - items
            - records
        Output:
            - use item
        '''
        import random
        item_nums = [x for x in range(1, len(self.items)+1)]
        use_num = random.choice(item_nums)
        item = self.items[use_num-1]
        return item

    def make_item_message(self):
        '''
        Make json message of item.
        '''
        self.item = self.select_item()
        message = {
            "is_question": False,
            "content": {
                "question": {},
                "item": self.item
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
                "item": {}
            },
            "records": self.records
        }
        message_json = json.dumps(message, ensure_ascii=False)
        return message_json

    def make_message_json(self):
        '''
        Make json data for return message.
        If available_nums == -1, return item message.
        Input:
            - records
            - use question
        Output:
            - message json data
        '''
        if self.available_nums == -1:
            return self.make_item_message()
        else:
            return self.make_question_message()

    def get_available_questions(self):
        '''
        Get available question numbers.
        If number of answers > threshold, return -1.
        Input:
            - records
            - questions
        Output:
            - available question numbers
        '''
        used_nums = [x[0] for x in self.records]
        question_nums = [x for x in range(1, len(self.questions)+1)]
        available_nums = list(filter(lambda x: x not in used_nums, question_nums))
        if len(used_nums) >= self.threshold or len(available_nums) == 0:
            return -1
        else:
            return available_nums

    def get_message(self):
        '''
        Main module of getting return message.
        '''
        self.available_nums = self.get_available_questions()
        message_json = self.make_message_json()
        return message_json
