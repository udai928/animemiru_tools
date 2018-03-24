#-*- coding:utf-8 -*-
import os
import urllib.request
import urllib.error

import sys
sys.path.append('..')
from common import read_setting as rs

class SearchImage:
    def __init__(self,image_url,environment_str):
        self.image_url = image_url
        self.image_dir = rs.load_config(environment_str)["search_image_dir"]
        self.image_filename = os.path.basename(image_url)
        self.image_path = self.image_dir + self.image_filename

    def download_image(self):
        try:
            data = urllib.request.urlopen(self.image_url).read()
            with open(self.image_path, mode="wb") as f:
                f.write(data)

            # ダウンロードできたかチェック（ダウンロードの失敗をexceptionでキャッチしきれないケースがあったため）
            if os.path.exists(self.image_path):
                return True
            else:
                print(f"### ErrorDownload ### 画像（{self.image_url}）ダウンロードに失敗しました。比較対象から除外します。")
                return False
        except urllib.error.URLError as e:
            print(f"### ErrorDownload ### 画像（{self.image_url}）ダウンロードに失敗しました。比較対象から除外します。：{e}")
            return False