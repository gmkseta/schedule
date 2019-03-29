# -*- coding: utf-8 -*-
# from time import sleep
# from re import findall
# import math
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
# import requests
# from util.settings import Settings
# from .util import web_adress_navigator
# from util.extractor_posts import extract_post_info
# import datetime
# from util.instalogger im port InstaLogger
# from util.exceptions import PageNotFound404,NoInstaProfilePageFound,NoInstaPostPageFound
from schedule import *
import pdb;
import re;
import pymysql;
import os;
from setting import *
import sys;
import json


class JsonPost:
    # browser = None
    # option = None
    def __init__(self,path):
        self.get_data_sql = "SELECT id, postfile FROM POSTS WHERE postfile IS NOT NULL AND json_post IS NULL";     

        self.save_process_sql ='''
        UPDATE posts SET json_post = %s where id = %s
        '''


        try:
            self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd=MYSQL_PASS,
            db='hisw_development',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()

            self.path = path

        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit()


    def get_post(self):
        self.cursor.execute(self.get_data_sql)
        post_list =self.cursor.fetchall()
        for i in post_list:
            try:
                sc = Schedule(self.path+'/'+i['postfile'])
                print(sc.json)
                self.cursor.execute(self.save_process_sql, (json.dumps(sc.json), i['id']))
                self.conn.commit();
                
            except ValidTokenException:
                print("ValidTokenException")
            
   

test = JsonPost(sys.argv[1])
test.get_post()