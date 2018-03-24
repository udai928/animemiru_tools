# coding:utf-8
import sys
sys.path.append('..')

from common import mag
from common import mysql_connector as my_con
from common import read_setting as rs
import os
import os.path
from datetime import datetime as dt

ENV = sys.argv[1]
IMAGES_DIR = rs.load_config(ENV)["images_dir"]
TITLE_KEYWORD_FILE = "title_keyword.csv"
MEDIA_KEYWORD_FILE = "media_keyword.csv"
STORY_KEYWORD_FILE = "story_keyword.csv"
IMAGE_KEYWORD_FILE = "image_keyword.csv"


def main():
    for dir_path, dir_names, file_names in os.walk(IMAGES_DIR):
        print(f"{dir_path}を検索しています...")
        for dir_name in dir_names:
            print(f"ディレクトリ:{dir_name}が存在します。")

        for file_name in file_names:
            print(f"ファイル:{file_name}が存在します。")
            #file_name_no_ext:拡張子無しファイル名｜ext:拡張子
            file_name_no_ext, ext = os.path.splitext(file_name)
            if ".csv" == ext:
                print(f"csvファイルを検出しました。キーワード取り込み処理を実行します。")
                mag_obj = mag.Mag()
                mag_obj.get_mag_info_from_(dir_path,ENV)
                if file_name == IMAGE_KEYWORD_FILE:
                    mag_obj.insert_image_keyword(dir_path,file_name)
                elif file_name == STORY_KEYWORD_FILE:
                    mag_obj.insert_mediastory_keyword(dir_path,file_name)
                else:
                    mag_obj.insert_keyword(dir_path,file_name)

                #rename(dir_path,file_name)


def rename(dir_path,file_name):
    now_obj = dt.now()
    now_str = now_obj.strftime('%Y%m%d%H%M%S')
    print(f"rename from --> {dir_path}/{file_name}")
    print(f"rename to   --> {dir_path}/{file_name}.{now_str}")
    os.rename(f"{dir_path}/{file_name}", f"{dir_path}/{file_name}.{now_str}")


if __name__ == '__main__':
    main()