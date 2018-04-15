# -*- coding:utf-8 -*-
import sys
import re

sys.path.append('..')
from common import mysql_connector as my_con

class Title:

    def __init__(self):
        self._title_id = None
        self._title_name = None
        self._title_source = None
        self._title_source_url = None

    @property
    def title_id(self):
        return self._title_id

    @title_id.setter
    def title_id(self, title_id):
        self._title_id = title_id

    @property
    def title_name(self):
        return self._title_name

    @title_name.setter
    def title_name(self, title_name):
        self._title_name = title_name

    @property
    def title_source(self):
        return self._title_source

    @title_source.setter
    def title_source(self, title_source):
        self._title_source = title_source

    @property
    def title_source_url(self):
        return self._title_source_url

    @title_source_url.setter
    def title_source_url(self, title_source_url):
        self._title_source_url = title_source_url

    def title_generator(self, image_path, env):
        if "images" in image_path:
            # "/Users/hoge/titlemiru/static/images/1_この素晴らしい世界に祝福を/01" -> "images/1_この素晴らしい世界に祝福を/"
            # "images/1_この素晴らしい世界に祝福を/" -> "1_この素晴らしい世界に祝福を/"
            # "1_この素晴らしい世界に祝福を" -> "1", "この素晴らしい世界に祝福を"
            title_dir_under_static = re.search(r"images/(.+)/", image_path)
            title_dir_name = title_dir_under_static[1].replace("images/", "")
            title_id = title_dir_name.split("_")[0]
            self._title_id = int(title_id)
            sql = f""" select title_name,title_source,title_source_url from title where title_id = {self._title_id};"""
            title_info_one = my_con.execute_select_one(sql, env)
            self._title_name = title_info_one[0]
            self._title_source = title_info_one[1]
            self._title_source_url = title_info_one[2]
            if title_info_one == None:
                self._title_id = 0
                self._title_name = "animemiru"
                self._title_source = ""
                self._title_source_url = "http://animemiru.jp/"
        else:
            self._title_id = 0
            self._title_name = "animemiru"
            self._title_source = ""
            self._title_source = "http://animemiru.jp/"


