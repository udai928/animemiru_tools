# -*- coding: utf-8 -*-
from slackbot.bot import respond_to
from slackbot.bot import default_reply

import sys
sys.path.append("../")
from similar_image import similar_image_bot

# TODO ENVを実行環境に応じて動的に変更できるようにしたい。
ENV = "devel"

@respond_to("^search\s+\S.*")
def mention_func(message):
    text = message.body["text"]
    temp, keyword = text.split(None, 1)
    message.send(f"> {keyword} \nこのサーチワードからAnimemiru画像を検索します。")

    similar_image_bot.post_slack_similar_image(ENV,keyword)

    message.reply("...検索終了です。")
