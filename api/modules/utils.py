# -*- coding:utf-8 -*-
# Author: Yuta Yamashita

import json


def load_json(path):
    '''
    Loading json file.
    '''
    with open(path, "r") as f:
        return json.load(f)

def sorted_by_dictkey(target, sort_key):
    '''
    sort list by dictionary key
    -- example, key=id --
    [{id:2, content:"bbb"}, {id:1, content:"aaa"}]
    -> [{id:1, content:"aaa"}, {id:2, content:"bbb"}]
    '''
    sorted_list = sorted(target, key=lambda x:x[sort_key])
    return sorted_list
