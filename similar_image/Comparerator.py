# -*- coding:utf-8 -*-
import cv2
import os
import sys

IMG_SIZE = (800, 450)
COLOR = ('b','g','r')


class Comparerator:

    def __init__(self,search_img, hosting_img):
        self.search_img_obj = search_img
        self.hosting_img_obj = hosting_img
        self.search_img_path = search_img.image_path
        self.hosting_img_path = hosting_img.image_path
        self.hist_result = None
        self.hist_rgb_result = None
        self.des_result = None

    def is_similar(self):
        judgment = False
        if self.hist_result == None and self.hist_rgb_result != None and self.des_result != None:
            print(f"{self.hist_result}がNoneでした。")
            if self.des_result < 130 and self.hist_rgb_result >= 0.7:
                return True
        if self.hist_result != None and self.hist_rgb_result == None and self.des_result != None:
            print(f"{self.hist_rgb_result}がNoneでした。")
            if self.des_result < 130 and self.hist_result >= 0.7:
                return True
        if self.hist_result != None and self.hist_rgb_result != None and self.des_result == None:
            print(f"{self.des_result}がNoneでした。")
            if self.hist_rgb_result > 0.6 and self.hist_rgb_result > 0.6:
                return True
        if self.des_result < 150 and self.hist_rgb_result >= 0.6 and self.hist_result >= 0.6:
            return True
        return judgment

    def compare_histgram_rgb(self):
        search_hist_rgb = self.cal_histgram_rgb(self.search_img_obj.image_path)
        hosting_hist_rgb = self.cal_histgram_rgb(self.hosting_img_obj.image_path)
        result_rgb = []
        for i,col in enumerate(COLOR):
            result = cv2.compareHist(search_hist_rgb[col], hosting_hist_rgb[col], 0)
            result_rgb.append(result)
        self.hist_rgb_result = sum(result_rgb)/len(result_rgb)

    def cal_histgram_rgb(self,image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, IMG_SIZE)
        img_hist_rgb = {}
        for i, col in enumerate(COLOR):
            img_hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            img_hist_rgb[col] = img_hist
        # img_hist.show()
        return img_hist_rgb

    def compare_histgram(self):
        search_hist = self.cal_histgram(self.search_img_obj.image_path)
        hosting_hist = self.cal_histgram(self.hosting_img_obj.image_path)
        self.hist_result = cv2.compareHist(search_hist, hosting_hist, 0)

    def cal_histgram(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, IMG_SIZE)
        img_hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        return img_hist

    def compare_description(self):
        detector = cv2.BRISK_create()
        # detector = cv2.ORB_create()
        # detector = cv2.AKAZE_create()
        #    detector = cv2.AgastFeatureDetector_create()
        #    detector = cv2.FastFeatureDetector_create()
        #    detector = cv2.MSER_create()
        #    detector = cv2.SimpleBlobDetector_create()
        #    detector = cv2.xfeatures2d.SIFT_create()
        search_des = self.cal_description(self.search_img_obj.image_path, detector)
        hosting_des = self.cal_description(self.hosting_img_obj.image_path, detector)
        try:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
            matches = bf.match(search_des, hosting_des)
            dist = [m.distance for m in matches]
            ret = sum(dist) / len(dist)
        except cv2.error:
            print(f"### exception ### BFMatcherでエラーが発生したため、マッチ度を10000にしました。" \
                  f"search:{self.search_img_obj.image_filename} / hosting:{self.hosting_img_obj.image_filename} ")
            ret = 100000
        self.des_result = ret

    def cal_description(self, image_path, detector):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, IMG_SIZE)
        kp, description = detector.detectAndCompute(img, None)
        return description

    def image_show(self):
        search_img_path_obj = cv2.imread(self.search_img_obj.image_path)
        cv2.imshow(self.search_img_obj.image_path, search_img_path_obj)

        hosting_img_path_obj = cv2.imread(self.hosting_img_obj.image_path)
        cv2.imshow(self.hosting_img_obj.image_path, hosting_img_path_obj)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

