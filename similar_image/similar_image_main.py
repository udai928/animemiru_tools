#-*- coding:utf-8 -*-
import sys
sys.path.append('..')

from similar_image import SearchImage
from similar_image import get_image_source as source
from similar_image import Comparerator

def similar_image(env_str,searchword_str):
    print("# Google画像検索でヒットした画像のURLを取得")
    google_search_image_urls = source.get_image_urls_from_google(searchword_str, env_str)

    print("# Google画像検索画像のダウンロード先tmpフォルダ内の画像を削除")
    source.delete_files(env_str)

    print("# Google画像検索でヒットした画像をダウンロード")
    search_images = []
    for google_search_image_url in google_search_image_urls:
        search_image_obj = SearchImage.SearchImage(google_search_image_url, env_str)
        if search_image_obj.download_image():
            search_images.append(search_image_obj)

    print("# 比較対象のAnimeiruが保有する画像オブジェクトを生成")
    hosting_images = source.generate_hosting_images(searchword_str, env_str)

    # TODO:hosting_imagesの件数を取得し、件数とcompare処理の進捗からプログレッシブバー的なのを表示したい。

    print("# Googleの画像とAnimemiru保有の画像を比較して似ている画像を抽出")
    similar_images = []
    for search_image in search_images:
        for hosting_image in hosting_images:
            compare_result = Comparerator.Comparerator(search_image, hosting_image)
            compare_result.compare_histgram()
            compare_result.compare_histgram_rgb()
            compare_result.compare_description()
            if compare_result.is_similar():
                print(f"### Similar ### {compare_result.search_img_obj.image_filename}と{compare_result.hosting_img_obj.image_filename}が類似画像と判定されました。")
                similar_images.append(compare_result)

    return similar_images

