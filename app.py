# cofing:utf-8
from flask import Flask, render_template, request, jsonify, json

from common import read_setting as rs
from common import mysql_connector as my_con
from common import mag as mag

# from similar_image.Comparerator import *
# from similar_image.HostingImage import *
# from similar_image.SearchImage import *
# from similar_image.get_image_source import *
from similar_image import similar_image_main

ENV = "devel"

app = Flask(__name__)

@app.route('/')
def index():
    images = []
    return render_template("index.html",images = images ,keyword = '')


@app.route('/similar_image', methods=['POST'])
def post():
    print(request.form["keyword"])
    keyword = request.form["keyword"]
    select_images = similar_image_main.similar_image(ENV,keyword)

    if select_images == []:
        return render_template("index.html",images = [])

    images = []
    for index,select_image in enumerate(unique(select_images)):
        image_static_path = (select_image.hosting_img_path).split("static")
        print(image_static_path)
        image = {}
        image["image_index"] = index
        image["image_path"] = f"static{image_static_path[1]}"
        image["image_tag"] = f"<img src=\"static{image_static_path[1]}\" alt=\"\" width=\"480\" height=\"270\" class=\"alignnone size-medium wp-image-598\" />\n<a href=\"[anime_story.story_url]\" target=\"_blank\" rel=\"noopener\"><div class=\"source\">出典: [anime.anime_title] 第[anime_stroy.story_id]話</div></a>"
        images.append(image)

    print(images)
    return render_template("index.html",images = images, keyword = keyword)


# @app.route('/search', methods=['POST'])
# def post():
#     print(request.form["keyword"])
#     keyword = request.form["keyword"]
#
#     select_images = []
#     select_images.extend(get_image_name_from_keyword(keyword))
#     select_images.extend(get_image_name_from_media_story(keyword))
#
#     select_image_ids = []
#     select_image_ids.extend(get_image_ids_from_media(keyword))
#     select_image_ids.extend(get_image_ids_from_title(keyword))
#
#     select_images.extend(get_image_name_from_image_ids(select_image_ids))
#
#     if select_images == []:
#         return render_template("index.html",images = [])
#
#     images = []
#     for index,select_image in enumerate(unique(select_images)):
#         print(select_image[0])
#         image = {}
#         image["image_index"] = index
#         image["image_path"] = f"static/{select_image[0]}"
#         image["image_tag"] = f"<img src=\"static/{select_image[0]}\" alt=\"\" width=\"480\" height=\"270\" class=\"alignnone size-medium wp-image-598\" />\n<a href=\"[anime_story.story_url]\" target=\"_blank\" rel=\"noopener\"><div class=\"source\">出典: [anime.anime_title] 第[anime_stroy.story_id]話</div></a>"
#         images.append(image)
#
#     print(images)
#     return render_template("index.html",images = images, keyword = keyword)

# TODO list_handler.pyから呼び出すようにリファクタする。
def unique(list_x):
    list_uniq = []
    for x in list_x:
        if x not in list_uniq:
            list_uniq.append(x)
    return list_uniq

def get_image_name_from_keyword(keyword):
    sql = f"""
    select
        distinct image_name
    from image img
    left join relay_image_keyword relay_kw
        on img.image_id = relay_kw.image_id
    left join keyword kw
        on kw.keyword_id = relay_kw.keyword_id
    where
        kw.keyword_character like '%{keyword}%'
    ;
    """
    image_names = my_con.execute_select_all(sql,"devel")
    return image_names

def get_image_name_from_media_story(keyword):
    sql = f"""
    select
        distinct image_name
    from image img
    left join relay_media_story_image sty_img
        on img.image_id = sty_img.image_id
    left join relay_media_story_keyword sty_kw
        on sty_kw.media_id = sty_img.media_id and sty_kw.story_id = sty_img.story_id
    left join keyword kw
        on kw.keyword_id = sty_kw.keyword_id
    where
        kw.keyword_character like '%{keyword}%';
    """
    image_names = my_con.execute_select_all(sql,"devel")
    return image_names

def get_image_name_from_image_ids(image_ids):
    if image_ids == []:
        return []
    image_ids_csv = ''
    for index,image_id in enumerate(image_ids):
        if index == 0:
            image_ids_csv = image_ids_csv + image_id[0]
        else:
            image_ids_csv = image_ids_csv + "," + image_id[0]
    sql = f"""
    select distinct image_name from image where image_id in ({image_ids_csv});
    """
    image_names = my_con.execute_select_all(sql,"devel")
    return image_names

def get_image_ids_from_media(keyword):
    sql = f"""
    select distinct image_id from relay_media_story_image
    where media_id in (
        select media_id from relay_media_keyword sty_kw
        left join keyword kw
            on kw.keyword_id = sty_kw.keyword_id
        where
            kw.keyword_character like '%{keyword}%'
    )
    """
    image_ids = my_con.execute_select_all(sql,"devel")
    return image_ids

def get_image_ids_from_title(keyword):
    sql = f"""
    select distinct image_id from relay_media_story_image
    where media_id in (
        select m.media_id from relay_media_keyword m_kw
        left join media m
            on m.media_id = m_kw.media_id
        where
            title_id in (
                select title_id from relay_title_keyword title_kw
                left join keyword kw
                    on kw.keyword_id = title_kw.keyword_id
                where
                    kw.keyword_character like '%{keyword}%'
            )
    );
    """
    image_ids = my_con.execute_select_all(sql,"devel")
    return image_ids


if __name__ == "__main__":
    app.run("0.0.0.0")
    app.debug()
