import time
import os
import numpy as np
import cv2 as cv
import random
from math import *

def xuanzhuan(img):
  height,width=img.shape[:2]
  degree=-90
  #旋转后的尺寸
  heightNew=int(width*fabs(sin(radians(degree)))+height*fabs(cos(radians(degree))))
  widthNew=int(height*fabs(sin(radians(degree)))+width*fabs(cos(radians(degree))))
  matRotation=cv.getRotationMatrix2D((width/2,height/2),degree,1)
  matRotation[0,2] +=(widthNew-width)/2  #重点在这步，目前不懂为什么加这步
  matRotation[1,2] +=(heightNew-height)/2  #重点在这步
  imgRotation=cv.warpAffine(img,matRotation,(widthNew,heightNew),borderValue=(255,255,255))
  return imgRotation
def distance_n(id):
    img = cv.imread('autojump.png')
    img = xuanzhuan(img)
    player_template = cv.imread('player2.png')
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)
    player_spot = (max_loc[0] + 25, max_loc[1] + 150)
    # 绘制player位置标记
    img_blur = cv.GaussianBlur(img, (5, 5), 0)  # 高斯模糊
    canny_img = cv.Canny(img_blur, 1, 10)  # 边缘检测
    height, width = canny_img.shape
    # 消除多余的头部
    for y in range(max_loc[1]-5, max_loc[1] + 150):
        for x in range(max_loc[0]-5, max_loc[0] + 50):
            canny_img[y][x] = 0
    if max_loc[0] + 25 > int(width / 2):
        crop_img = canny_img[300:max_loc[1]+42 , 20: max_loc[0]+25 ]  # 裁切
        crop_img1 = img[300:max_loc[1] +42, 20: max_loc[0]+25 , :]  # 裁切
    else:
        crop_img = canny_img[300:max_loc[1] +42, max_loc[0] +25: width]  # 裁切
        crop_img1 = img[300:max_loc[1]+42 , max_loc[0]+25 :width, :]  # 裁切
    crop_h, crop_w = crop_img.shape
    point_mid = np.zeros((crop_h, crop_w, 1), dtype=np.uint8)
    center_x, center_y = 0, 0  # 临时变量
    max_x = 0
    num_point = 0
    w_point=0
    for y in range(crop_h):
        for x in range(crop_w):
            if crop_img1[y, x, 0] == 245 and crop_img1[y, x, 1] == 245 and crop_img1[y, x, 2] == 245:
                point_mid[y, x] = 255
                num_point = num_point + 1
    if num_point>260 and num_point<320:
       crop_img=point_mid
       w_point=1
    # 计算中央点
    for y in range(crop_h):
        for x in range(crop_w):
            if crop_img[y, x] == 255:
                if center_x == 0:
                    center_x = x
                if x > max_x:
                    center_y = y
                    max_x = x
    if center_y + 20 > crop_h and w_point == 0:
        max_x = 0
        center_y = 0
        center_x = 0
        if max_loc[0] + 25 > int(width / 2):
            crop_img = canny_img[300:max_loc[1] + 70, 20: max_loc[0] + 25]  # 裁切
            crop_img1 = img[300:max_loc[1] + 70, 20: max_loc[0] + 25, :]  # 裁切
        else:
            crop_img = canny_img[300:max_loc[1] + 70, max_loc[0]: width]  # 裁切
            crop_img1 = img[300:max_loc[1] + 70, max_loc[0]:, :]  # 裁切
        crop_h, crop_w = crop_img.shape
        for y in range(crop_h):
            for x in range(crop_w):
                if crop_img[y, x] == 255:
                    if center_x == 0:
                        center_x = x
                    if x > max_x:
                        center_y = y
                        max_x = x
    if max_loc[0] + 25 > int(width / 2):
        block_center = (center_x + 20, center_y + 300)  # 中央点
    else:
        block_center = (center_x + max_loc[0]+25 , center_y + 300)  # 中央点
    #print("玩家位置", player_spot)
    #print("落点位置", block_center)
    distance1 = (block_center[0] - player_spot[0]) * (block_center[0] - player_spot[0]) + (block_center[1] - player_spot[1]) * (block_center[1] - player_spot[1])
    distance1 = sqrt(distance1)
    #cv.line(img, player_spot, block_center, (0, 255, 0), 5)  # 绘制直线
    filename=str(id)+'.png'
    cv.imwrite(filename,img)
    return distance1




def screenshot(id):
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png .')


def jump(distance):
    press_time = int(distance * 2)
    print(str(press_time))
    rand = random.randint(0, 9) * 10
    cmd = ('adb shell input swipe %i %i %i %i ' + str(press_time)) \
          % (320 + rand, 410 + rand, 320 + rand, 410 + rand)
    os.system(cmd)
    #print(cmd)


#��ʼ��
id=0

while int(id)>=0 :


    if(int(id)==0):
        # jump the first time
        jump(350)
        time.sleep(1.8)
        screenshot(1)
        id=1
    elif(id>0):
        disj=distance_n(id)
        jump(disj)
        time.sleep(1.8)
        screenshot(id)
        id=id+1
else:
    # exit
    screenshot('res')





