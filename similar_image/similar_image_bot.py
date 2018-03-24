#-*- coding:utf-8 -*-
import requests
import json

import sys
sys.path.append('..')
from common import read_setting as rs
from common import list_handler as lh
from similar_image import similar_image_main as sim

def main():
    ENV = sys.argv[1]
    SEARCHWORD_STR = sys.argv[2]
    post_slack_similar_image(ENV, SEARCHWORD_STR)

def post_slack_similar_image(environment_str, searchword):
    source_url = rs.load_config(environment_str)["source_url"]
    webhook_url = rs.load_config(environment_str)["webhook_url"]
    bot_name = rs.load_config(environment_str)["bot_name"]
    image_www_path = rs.load_config(environment_str)["image_www_path"]

    select_images = sim.similar_image(environment_str,searchword)

    for select_image in lh.unique(select_images):
        image_static_path = (select_image.hosting_img_path).split("static/")
        print(image_static_path)

        message_text = f"""{image_www_path}/{image_static_path[1]}\n""" \
            f"""```<img src=\"static{image_static_path[1]}\" alt=\"\" width=\"480\" height=\"270\" """ \
            f"""class=\"alignnone size-medium wp-image-598\" />\n""" \
            f"""<a href=\"{source_url}\" target=\"_blank\" rel=\"noopener\"><div class=\"source\">""" \
            f"""出典: [anime.anime_title] 第[anime_stroy.story_id]話</div></a>```"""

        post_slack_webhook(bot_name,message_text, webhook_url)
        print(message_text)


def post_slack_webhook(botname, text, webhook_url):
    requests.post(webhook_url,data=json.dumps(
            {
                "text": text,
                "username": botname,
                "icon_emoji": ":python:"
            }))

if __name__ == '__main__':
    main()