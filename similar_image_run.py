#-*- coding:utf-8 -*-
import sys
from similar_image import similar_image_main

def main():
    # python similar_image.py "devel" "アニメ ソードアート・オンライン 1話"
    ENV = sys.argv[1]
    SEARCHWORD_STR = sys.argv[2]
    similar_images = similar_image_main.similar_image(ENV,SEARCHWORD_STR)
    similar_images_len = len(similar_images)
    for_count = 0
    if similar_images_len == 0:
        print("該当する類似画像がありません。")
    elif similar_images_len < 10:
        print("該当する類似画像が0~10個でした。")
        for_count = similar_images_len
    else:
        print("該当する画像が10個以上でした。")
        for_count = 10
    sorted_similar_images = sorted(similar_images,key=lambda x:x.des_result,reverse=False)
    for i in range(for_count):
        sorted_similar_images[i].image_show()



if __name__ == '__main__':
    main()