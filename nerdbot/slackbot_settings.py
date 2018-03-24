# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from common import read_setting as rs

# TODO ENVを実行環境に応じて動的に変更できるようにしたい。
ENV = "devel"
API_TOKEN = rs.load_config(ENV)["bot_api_key"]
DEFAULT_REPLY = "は？"
PLUGINS = ['plugins']