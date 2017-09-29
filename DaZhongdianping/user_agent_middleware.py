#!/usr/bin/python
#coding=utf-8
#__author__='dahu'
#data=2017-
# 
from settings import USER_AGENT_LIST

import random

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)