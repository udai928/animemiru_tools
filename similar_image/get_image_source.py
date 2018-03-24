#-*- coding:utf-8 -*-
import re
import os
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

import sys
sys.path.append('..')
from similar_image import HostingImage
from common import read_setting as rs
from common import mysql_connector as my_con

def get_image_urls_from_google(searchword,environment_str):
    print("# Google画像検索URLを生成")
    url_keyword = urllib.parse.quote(searchword)
    search_url = 'https://www.google.com/search?hl=jp&q=' + url_keyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'

    print("# BeatifulSoupオブジェクトを生成")
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(search_url, None, headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    print("# BeatifulSoupオブジェクトから画像URL文字列郡を取得")
    how_many_images = int(rs.load_config(environment_str)["how_many_images"])
    a_tags_filtered_jsname = soup.find_all("div",attrs={"class": "rg_meta notranslate"}, limit=how_many_images)
    image_urls = []
    for a_tag_filtered_jsname in a_tags_filtered_jsname:
        json_str = str(a_tag_filtered_jsname).replace("<div class=\"rg_meta notranslate\" jsname=\"ik8THc\">","").replace("</div>","")
        json_obj = json.loads(json_str)
        image_urls.append(json_obj["ou"])

    print(image_urls)
    return image_urls

def generate_hosting_images(searchword_str,environment_str):
    print("# サーチワードからAnimemiruDBにあるタイトルディレクトリ郡（[title_id]_[title_name]）を取得")
    title_dirs = get_title_dirs_from(searchword_str,environment_str)

    print("# title_dirが取得できなかった場合、そのtitle_dirの画像のみを比較対象とする")
    hosting_image_dirs = []
    if len(title_dirs) == 0:
        print(f"### title_dir ###サーチワードからアニメを特定できませんでした。比較対象画像は全てになるため処理に時間がかかります。")
        hosting_image_dirs.append(str(rs.load_config(environment_str)["images_dir"]))
    else:
        print(f"### title_dir ### サーチワードからアニメを特定できました。比較対象画像を{title_dirs}に絞ります。")
        for title_dir in title_dirs:
            if title_dir != None:
                hosting_image_dirs.append(str(rs.load_config(environment_str)["images_dir"]) + title_dir + "/")

    print("# Animeiruが保有する画像オブジェクトを取得")
    hosting_images = []
    for hosting_image_dir in hosting_image_dirs:
        for dir_path, dir_names, file_names in os.walk(hosting_image_dir):
            for file_name in file_names:
                pattern = ".*\.(jpg|png|bmp)"
                if re.search(pattern, file_name, re.IGNORECASE):
                    hosting_images.append(HostingImage.HostingImage(file_name,dir_path + file_name))
    return hosting_images

def get_title_dirs_from(searchword_str,environment_str):
    searchwords_splited = searchword_str.split(" ")
    title_dirs = []
    for searchword_splited in searchwords_splited:
        sql = f"""
        select concat(title_id,"_",title_name) from title
        where title_name like '%{searchword_splited}%';
        """
        title_dirs_from = my_con.execute_select_all(sql,environment_str)
        for i,title_dir in enumerate(title_dirs_from):
            title_dirs.append(title_dirs_from[i][0])
    return title_dirs


def delete_files(environment_str):
    search_image_dir = rs.load_config(environment_str)["search_image_dir"]
    for root, dirs, files in os.walk(search_image_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))