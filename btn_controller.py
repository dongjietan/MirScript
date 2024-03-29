import os
import time
import re
import cv2
import random

import adb_controller
import image_processor
import settings
import globals
import utils
import game_controller
import path_controller
import move_controller
import match_controller

# def click_menu_batch_use():
#     adb_controller.screenshot(settings.screenshot_path)
#
#     lower_color = [0,0,212]
#     upper_color = [179,255,255]
#
#     match_scope = (876,924,754,910)
#     match_scope = utils.convert_scope(match_scope, (1664, 936))
#
#     resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
#     for idx in range(len(resultss)):
#         results = resultss[idx]
#         for result in results:
#             name_rate = result[1] #('43', 0.99934321641922)
#             name = name_rate[0] #'43'
#             if "批量使用" in name:
#                 print("result: {}".format(str(result)))
#                 corners = result[0]
#                 center = utils.get_center_of_corners(corners)
#                 adb_controller.click(center)
#                 return True
#     return False


# def click_confirm_batch_use():
#     adb_controller.screenshot(settings.screenshot_path)
#
#     lower_color = [0,0,212]
#     upper_color = [179,255,255]
#
#     match_scope = (584,646,915,1167)
#     match_scope = utils.convert_scope(match_scope, (1664, 936))
#
#     resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
#     for idx in range(len(resultss)):
#         results = resultss[idx]
#         for result in results:
#             name_rate = result[1] #('43', 0.99934321641922)
#             name = name_rate[0] #'43'
#             if "批量使用" in name:
#                 print("result: {}".format(str(result)))
#                 corners = result[0]
#                 center = utils.get_center_of_corners(corners)
#                 adb_controller.click(center)
#                 return True
#     return False


#点击屏幕，消除省电模式（不管有没有）
def click_center_of_screen():
    point = utils.convert_point((832, 468), (1664, 936))
    adb_controller.click(point, 0.1)


#点击盟重老兵
def click_npc_meng_zhong_lao_bing():
    print("click_npc_meng_zhong_lao_bing")
    adb_controller.screenshot(settings.screenshot_path)
    # 坐标颜色绿色参数
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (0,936,0,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    masks = []
    masks.append((0,34,440,1234)) #顶部滚动通知
    masks.append((42,198,1354,1664)) #右上角地图
    masks.append((796,936,625,1196)) #底部聊天窗口
    masks = utils.convert_masks(masks, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color, masks = masks)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            print("name: {}".format(str(name)))
            if "老兵" in name:
                print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


def click_yellow_menu(text):
    print("click_yellow_menu: {}".format(str(text)))
    # 坐标颜色黄色参数
    lower_color = [0,102,185]
    upper_color = [29,253,255]

    match_scope = (62,788,72,718)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            print("name: {}".format(str(name)))
            if text in name:
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


# 点击洞穴传送
def click_transfer_cave(cave_name):
    print("click_transfer_cave: {}".format(str(cave_name)))
    cave_name_dict = {
        "骷髅洞": "ku_lou_dong",
        "废矿入口": "fei_kuang_ru_kou",
        "死亡山谷": "si_wang_shan_gu",
        "沃玛寺庙": "wo_ma_si_miao",
        "猪洞": "zhu_dong",
        "祖玛寺庙": "zu_ma_si_miao",
        "封魔": "feng_mo",
        "赤月": "chi_yue",
        "骨魔洞窟": "gu_mo_dong_ku",
        "牛魔寺庙": "niu_mo_si_miao",
        "未知暗殿": "wei_zhi_an_dian",
        "同心小径": "tong_xin_xiao_jing",
    }
    cave_name = "{}{}".format("cave_btns/", cave_name_dict[cave_name])
    print("click_transfer_cave2: {}".format(str(cave_name)))
    return click_btn(cave_name)
    # # 米色参数
    # lower_color = [0,0,212]
    # upper_color = [179,255,255]
    #
    # match_scope = (284,608,966,1618)
    # match_scope = utils.convert_scope(match_scope, (1664, 936))
    #
    # resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    # for idx in range(len(resultss)):
    #     results = resultss[idx]
    #     for result in results:
    #         name_rate = result[1] #('43', 0.99934321641922)
    #         name = name_rate[0] #'43'
    #         print("cave name: {}".format(str(name)))
    #         # 骷髅两个字识别不出来
    #         if cave_name == "骷髅洞":
    #             cave_name = "洞"
    #         if cave_name == name:
    #             # print("result: {}".format(str(result)))
    #             corners = result[0]
    #             center = utils.get_center_of_corners(corners)
    #             adb_controller.click(center)
    #             return True
    # return False


# 消除如何移动提示
def click_msg_box(text):
    btn_name_dict = {
        "如何移动": "ru_he_yi_dong_g",
        "开始": "kai_shi_g",
        "知道了": "zhi_dao_le",
        "确定(右)": "que_ding_r",
        "否(左)": "fou_l",
        "是(右)": "shi_r",
        "依然传送": "yi_ran_chuan_song",
    }
    btn_name = "{}{}".format("msg_btn/", btn_name_dict[text])
    return click_btn(btn_name)
    # # 米色
    # lower_color = [0,0,212]
    # upper_color = [179,255,255]
    # # 绿色
    # if is_green:
    #     lower_color = [35,43,46]
    #     upper_color = [75,255,255]
    #
    # match_scope = (583,651,673,985)
    # match_scope = utils.convert_scope(match_scope, (1664, 936))
    #
    # resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    # for idx in range(len(resultss)):
    #     results = resultss[idx]
    #     for result in results:
    #         name_rate = result[1] #('43', 0.99934321641922)
    #         name = name_rate[0] #'43'
    #         if text == name:
    #             # print("result: {}".format(str(result)))
    #             corners = result[0]
    #             center = utils.get_center_of_corners(corners)
    #             adb_controller.click(center)
    #             return True
    # return False


# 点击菜单
def click_menu(text, match_scope):
    adb_controller.screenshot(settings.screenshot_path)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            print("name: {}".format(str(name)))
            if text in name:
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


def click_btn(btn_name, match_scope = (0,936,0,1664), need_screenshot = False):
    if need_screenshot:
        adb_controller.screenshot(settings.screenshot_path)
        
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = match_controller.match_template(btn_name, match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)
        return True
    return False

# 点击商品菜单
# def click_item_menu(text):
#     match_scope = (36,688,180,428)
#     return click_menu(text, match_scope)

def click_setting_menu(text):
    btn_name_dict = {
        "技能": "ji_neng",
    }
    btn_name = "{}{}".format("setting_menu/", btn_name_dict[text])
    return click_btn(btn_name)

def click_setting():
    match_scope = (888,936,80,174)
    return click_menu("设置", match_scope)

# def click_skill_setting():
    # match_scope = (404,474,1522,1638)
    # return click_menu("技能", match_scope)

# 点击商品菜单
def click_item_menu_at_index(index):
    match_scope = (36,688,180,428)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    x = match_scope[2] + (match_scope[3] - match_scope[2]) * 0.5
    each_height = (match_scope[1] - match_scope[0]) / 10
    y = 36 + each_height * 0.5 + each_height * index
    item_center = (x, y)
    adb_controller.click(item_center)

# 点击购买
def click_btn_buy():
    # match_scope = (798,864,426,546)
    # return click_menu("购买", match_scope)
    point = utils.convert_point((492, 832), (1664, 936))
    adb_controller.click(point)


def click_sell_all():
    match_scope = (456,516,1380,1540)
    return click_menu("出售", match_scope)

def click_repair_all():
    match_scope = (518,578,1380,1540)
    return click_menu("特修", match_scope)

def click_repair_wearing():
    match_scope = (582,650,490,754)
    return click_menu("装备", match_scope)

def click_confirm():
    return click_msg_box("确定(右)")
    # match_scope = (582,650,908,1166)
    # return click_menu("确定", match_scope)

def click_no():
    return click_msg_box("否(左)")
    # match_scope = (582,650,490,754)
    # return click_menu("否", match_scope)

def click_yes():
    return click_msg_box("是(右)")
    # match_scope = (582,650,908,1166)
    # return click_menu("是", match_scope)


# 点击“依然传送”
def click_btn_confirm_transform():
    return click_msg_box("依然传送")
    # match_scope = (582,650,908,1166)
    # return click_menu("依然传送", match_scope)


# 点击“登录”
# def click_btn_login():
#     match_scope = (694,788,724,940)
#     return click_menu("登录", match_scope)


# 如有弹出公告，则点击确定
def click_sure_btn():
    adb_controller.screenshot(settings.screenshot_path)

    match_loc = image_processor.match_template(
        settings.screenshot_path, r"template_images/msg_btn/que_ding_s.png", 0.15)
    if(match_loc != None):
        print("检测到弹框确定按钮，自动关闭...." + str(match_loc))
        adb_controller.click(match_loc)
        adb_controller.screenshot(settings.screenshot_path)
        return True
    return False


def click_scope(scope):
    point = ((scope[3] - scope[2]) / 2 + scope[2], (scope[1] - scope[0]) / 2 + scope[0])
    adb_controller.click(point)

def click_map():
    point = utils.convert_point((1645, 100), (1664, 936))
    adb_controller.click(point)

def click_map_aim():
    match_scope = utils.convert_scope((712,781,1556,1619), (1664, 936))
    click_scope(match_scope)

def click_map_input():
    match_scope = utils.convert_scope((420,501,562,1084), (1664, 936))
    click_scope(match_scope)

def click_map_clear():
    match_scope = utils.convert_scope((37,101,1398,1528), (1664, 936))
    click_scope(match_scope)
    time.sleep(settings.act_time)

# def click_map_edit_confirm():
#     match_scope = utils.convert_scope((229,289,1405,1520), (1664, 936))
#     click_scope(match_scope)

# def click_map_input_confirm():
#     match_scope = utils.convert_scope((586,647,912,1166), (1664, 936))
#     click_scope(match_scope)

def click_npc_wen_biao_tou():
    # 坐标颜色绿色参数
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (0,936,0,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if "温镖头" in name:
                print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False

def click_accept_ya_biao():
    point = utils.convert_point((145, 450), (1664, 936))
    adb_controller.click(point)

def click_npc_lu_lao_ban():
    # 坐标颜色绿色参数
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (0,936,0,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    masks = []
    masks.append((0,34,440,1234)) #顶部滚动通知
    masks.append((42,198,1354,1664)) #右上角地图
    masks.append((796,936,625,1196)) #底部聊天窗口
    masks = utils.convert_masks(masks, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color, masks = masks)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if "陆老板" in name:
                # print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False

def click_finish_ya_biao():
    point = utils.convert_point((185, 175), (1664, 936))
    adb_controller.click(point)


# def wait_to_match_and_click(btn_name,threshold,max_time,step_time):
#     print("Start to wait till match text by "+str(btn_name)+" for up to "+str(max_time)+" seconds  ....")
#     time_start = time.time()
#     click_success = False
#     while(True):
#         if click_btn(btn_name, need_screenshot = True):
#             click_success = True
#             break
#         if(time.time() - time_start > max_time):
#             print("Reach max_time but failed to match")
#             break
#         time.sleep(step_time)
#     return click_success

#丢弃
def click_drop():
    point = utils.convert_point((1310, 840), (1664, 936))
    adb_controller.click(point)

#存仓
def click_in_warehouse():
    print('存仓')
    point = utils.convert_point((1444, 840), (1664, 936))
    adb_controller.click(point)

def click_cancel_drop():
    point = utils.convert_point((622, 616), (1664, 936))
    adb_controller.click(point)

def click_confirm_drop():
    point = utils.convert_point((938, 616), (1664, 936))
    adb_controller.click(point)


def click_cancel_select():
    point = utils.convert_point((1080, 840), (1664, 936))
    adb_controller.click(point)

def click_left_return():
    print("click_left_return")
    # point = utils.convert_point((59, 872), (1664, 936))
    # adb_controller.click(point)
    click_btn("btn_left_return")

def click_right_return():
    print("click_right_return")
    # point = utils.convert_point((1604, 872), (1664, 936))
    # adb_controller.click(point)
    click_btn("btn_right_return")
