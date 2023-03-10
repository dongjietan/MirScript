import os
import time
import re
import cv2
import random
import numpy
import datetime

import globals
import settings
import utils
import image_processor
import adb_controller
import game_controller
import path_controller
import move_controller
import trash_controller
import skill_controller
import btn_controller

def summon_pet():
    print('道士重新召唤宝宝')
    if globals.current_lvl >= 35:
        if not skill_controller.cast_dog():
            skill_controller.cast_skeleton()
            skill_controller.cast_skeleton()
    else:
        if not skill_controller.cast_skeleton():
            print("学习召唤骷髅")
            game_controller.open_bag_and_drink("ji_neng_shu", batch=True)
            skill_controller.cast_skeleton()

def wait_till_max_lvl_max():
    print("wait_till_max_lvl_max")
    game_controller.reactive_pet()
    # 当前等级最大血量
    current_pet_max_HP = game_controller.get_pet_current_max_HP()
    # 可以达到的最大血量
    pet_max_HP = game_controller.get_pet_max_HP()
    print("current_pet_max_HP: {}".format(str(current_pet_max_HP)))
    print("pet_max_HP: {}".format(str(pet_max_HP)))
    if current_pet_max_HP == 0:
        print("current_pet_max_HP == 0")
        if globals.occupation == globals.Occupation.Taoist:
            summon_pet()
    while current_pet_max_HP != pet_max_HP:
        time.sleep(10)
        # 消除确认框，比如游戏断开，活动提醒
        while btn_controller.click_sure_btn():
            adb_controller.screenshot(settings.screenshot_path)
        current_pet_max_HP = game_controller.get_pet_current_max_HP()
        pet_max_HP = game_controller.get_pet_max_HP()

    print("pet HP reach Max")
    #消除省电模式
    if game_controller.is_save_power_mode():
        btn_controller.click_center_of_screen()
        adb_controller.screenshot(settings.screenshot_path)

    go_back_town_and_fly()


def go_back_town_and_fly():
    print("go_back_town_and_fly")
    # 回城
    move_controller.navigate_to_point((338,338), fly_to_exp_map)

def fly_to_exp_map():
    print("fly_to_exp_map")
    adb_controller.screenshot(settings.screenshot_path)
    while btn_controller.click_sure_btn():
        adb_controller.screenshot(settings.screenshot_path)

    #补给
    buy_supplies()
    adb_controller.screenshot(settings.screenshot_path)

    #道士检查是否学习隐身术，否者买一本
    if globals.occupation == globals.Occupation.Taoist and globals.current_lvl >= 20 and globals.current_lvl <= 25:
        if not skill_controller.cast_invisible():
            item_list = {
              "隐身术": 1,
            }
            trash_controller.buy_books(item_list)
            adb_controller.screenshot(settings.screenshot_path)
            game_controller.open_bag_and_drink("ji_neng_shu", batch=True)

    btn_controller.click_npc_meng_zhong_lao_bing()
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_yellow_menu("传送")
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)
    if globals.current_lvl < 17:
        btn_controller.click_transfer_cave("骷髅洞")
    elif globals.current_lvl <= 35:
        btn_controller.click_transfer_cave("废矿入口")
    else:
        btn_controller.click_transfer_cave("废矿入口")

    btn_controller.click_btn_confirm_transform()
    time.sleep(3.0)
    adb_controller.screenshot(settings.screenshot_path)
    map_name = game_controller.read_map_name()
    if globals.current_lvl < 17:
        if map_name == "洞1层":
            get_exp_by_random_fly()
        else:
            start()
    elif globals.current_lvl < 35:
        if map_name == "比奇矿区":
            go_to_east_waste_ore()
        else:
            start()
    else:
        if map_name == "比奇矿区":
            go_to_east_waste_ore()
        else:
            start()


def get_exp_by_random_fly():
    print("get_exp_by_random_fly")

    #吃栗子
    game_controller.open_bag_and_drink("zhong_se_li_zi")

    no_more_random_fly = 0
    while True:
        adb_controller.screenshot(settings.screenshot_path)
        if not game_controller.template_exist("btn_close_target"):
            skill_controller.cast_poison()
            skill_controller.cast_talisman()
            adb_controller.screenshot(settings.screenshot_path)
            if not game_controller.template_exist("btn_close_target"):
                pos_before_fly = move_controller.get_current_coordinate()
                skill_controller.cast_random_fly()
                skill_controller.cast_poison()
                skill_controller.cast_talisman()
                pos_after_fly = move_controller.get_current_coordinate()
                if pos_before_fly == pos_after_fly:
                    no_more_random_fly = no_more_random_fly + 1
                if no_more_random_fly >= 2:
                    while btn_controller.click_sure_btn():
                        adb_controller.screenshot(settings.screenshot_path)
                    print("学习召唤骷髅")
                    adb_controller.screenshot(settings.screenshot_path)
                    game_controller.open_bag_and_drink("ji_neng_shu", batch=True)
                    adb_controller.screenshot(settings.screenshot_path)
                    skill_controller.cast_back_town()
                    time.sleep(2.0)
                    start()
                    break


# 去废矿东部
def go_to_east_waste_ore():
    print("go_to_east_waste_ore")
    move_controller.navigate_to_point((179,110), start, skill_controller.cast_invisible)


def routine_lvl_one():
    print("routine_lvl_one")
    if btn_controller.click_msg_box("如何移动", True):
        time.sleep(15)
        adb_controller.screenshot(settings.screenshot_path)
        btn_controller.click_msg_box("开始", True)
    game_controller.open_bag()
    game_controller.wipe_up_bag()
    time.sleep(0.5)
    trash_controller.drink_item("bu_yi_nan")
    trash_controller.drink_item("bu_yi_nv")
    trash_controller.drink_item("wu_mu_jian")
    btn_controller.click_left_return()
    btn_controller.click_right_return()
    while game_controller.read_lv_text() < 7:
        skill_controller.cast_attack()
        adb_controller.screenshot(settings.screenshot_path)
    print("等级7")
    time.sleep(3.0)
    while btn_controller.click_sure_btn():
        adb_controller.screenshot(settings.screenshot_path)

    routine_lvl_seven()


def routine_lvl_seven():
    print("routine_lvl_seven")
    if globals.current_lvl == 7:
        game_controller.open_bag()
        btn_controller.click_right_menu("整理")
        game_controller.wipe_up_bag()
        time.sleep(0.5)
        trash_controller.drink_item("jun_xiang")
        time.sleep(4.0)
        trash_controller.batch_drink_item("ji_neng_shu")
        trash_controller.drink_item("tie_jian")
        trash_controller.batch_drink_item("bo_li_jie_zhi")

        btn_controller.click_left_return()
        btn_controller.click_right_return()

    adb_controller.screenshot(settings.screenshot_path)
    game_controller.set_occupation()

    while game_controller.read_lv_text() < 15:
        if globals.occupation == globals.Occupation.Taoist:
            skill_controller.cast_attack()
        elif globals.occupation == globals.Occupation.Magician:
            skill_controller.cast_fire_ball()
        adb_controller.screenshot(settings.screenshot_path)
    print("等级15")
    time.sleep(30)
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_msg_box("知道了")
    routine_lvl_fifteen()


def routine_lvl_fifteen():
    print("routine_lvl_fifteen")
    while btn_controller.click_sure_btn():
        adb_controller.screenshot(settings.screenshot_path)

    if globals.current_lvl == 15 and game_controller.get_bag_remain_capacity() > 32:
        # 穿装备，学技能
        game_controller.open_bag()
        btn_controller.click_right_menu("整理")
        game_controller.wipe_up_bag()
        time.sleep(0.5)
        trash_controller.drink_item("jun_xiang")
        time.sleep(4.0)
        trash_controller.batch_drink_item("ji_neng_shu")
        if globals.occupation == globals.Occupation.Taoist:
            trash_controller.drink_item("ban_yue_wan_dao")
            trash_controller.drink_item("da_shou_zhuo")
            trash_controller.drink_item("zhen_zhu_jie_zhi")
        #穿衣服
        trash_controller.drink_item("qing_xing_kui_jia_nv")
        trash_controller.drink_item("qing_xing_kui_jia_nan")
        #丢垃圾
        trash_controller.drop_binding_trashes(False)
        btn_controller.click_left_return()
        btn_controller.click_right_return()
        time.sleep(1.0)

    go_back_town_and_get_subsidy()
    fly_to_exp_map()


def go_back_town_and_get_subsidy():
    print("go_back_town_and_get_subsidy")
    # 回城
    move_controller.navigate_to_point((338,338), get_subsidy)


def get_subsidy():
    print("get_subsidy")
    while btn_controller.click_sure_btn():
        adb_controller.screenshot(settings.screenshot_path)
    #领取低保
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_npc_meng_zhong_lao_bing()
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)
    game_controller.wipe_down_npc_dialog_menu()
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_yellow_menu("领取低保")
    btn_controller.click_left_return()


def buy_supplies():
    print("buy_supplies")
    adb_controller.screenshot(settings.screenshot_path)
    while btn_controller.click_sure_btn():
        adb_controller.screenshot(settings.screenshot_path)

    item_list = {
    }
    if globals.current_lvl < 17:
        item_list = {
          "超级魔法药": 8,
          "超级金创药": 3,
          "随机传送卷包": 9,
          "地牢逃脱卷": 1,
          "棕色栗子": 1,
          "黄色药粉(中)": 1,
          "灰色药粉(中)": 1,
          "护身符(大)": 4,
          "技能书": 0,
          "技能书激活": 0,
          "回城卷": 0,
          "魔法药小量": 0,
          "魔法药中包": 0,
          "金创药小量": 0,
          "军饷": 0,
        }
    elif globals.current_lvl < 22:
        item_list = {
            "护身符(大)": 12,
            "超级魔法药": 12,
            "超级金创药": 3,
            "地牢逃脱卷": 1,
            "随机传送卷": 3,
            "棕色栗子": 1,
            "回城卷": 0,
        }
    else:
        item_list = {
            "护身符(大)": 12,
            "超级魔法药": 12,
            "超级金创药": 1,
            "地牢逃脱卷": 1,
            "随机传送卷": 3,
            "棕色栗子": 1,
            "回城卷": 0,
        }

    shortage_list = trash_controller.get_supply_shortage_list(item_list)
    trash_controller.buy_items(shortage_list)

def start_get_exp():
    print("开始练级")
    adb_controller.connect()
    #消除省电模式
    if game_controller.is_save_power_mode():
        btn_controller.click_center_of_screen()

    adb_controller.screenshot(settings.screenshot_path)
    #获取职业
    game_controller.set_occupation()
    #地图名称
    map_name = game_controller.read_map_name()
    #获取等级
    globals.current_lvl = game_controller.read_lv_text()
    if globals.current_lvl < 15:
        #检测是否设置随机和回城
        if not skill_controller.cast_random_fly(False):
            for index in range(30):
                print("技能未设置随机和回城快捷键")
            print("程序结束")
            return
    if globals.current_lvl < 7:
        routine_lvl_one()
        return
    elif globals.current_lvl < 15:
        routine_lvl_seven()
        return
    elif globals.current_lvl < 17:
        if map_name == "盟重土城":
            routine_lvl_fifteen()
        elif map_name == "洞1层": #骷髅两个字不识别
            get_exp_by_random_fly()
        return
    if not game_controller.active_pet():
        print('当前没有宠物')
        if globals.occupation == globals.Occupation.Taoist:
            summon_pet()
        elif globals.occupation == globals.Occupation.Magician:
            print("法师直接下线换道士")
            return
    else:
        if globals.occupation == globals.Occupation.Taoist:
            print('虽然有宝宝了，再用一下召唤宝宝，为了初始化globals.skill_xxx_pos')
            summon_pet()

    if "盟重" in map_name:
        print("当前位置，盟重土城")
        if globals.occupation == globals.Occupation.Taoist:
            # 当前等级最大血量
            current_pet_max_HP = game_controller.get_pet_current_max_HP()
            # 可以达到的最大血量
            pet_max_HP = game_controller.get_pet_max_HP()
            print("current_pet_max_HP: {}".format(str(current_pet_max_HP)))
            print("pet_max_HP: {}".format(str(pet_max_HP)))
            if current_pet_max_HP != pet_max_HP:
                print("current_pet_max_HP != pet_max_HP")
                move_controller.navigate_to_point((200,278), wait_till_max_lvl_max)
            else:
                go_back_town_and_fly()
        return
    elif map_name == "洞1层": #骷髅两个字不识别
        get_exp_by_random_fly()
        return
    elif map_name == "比奇矿区":
        go_to_east_waste_ore()
        return

    cave_path = game_controller.get_map_path(map_name)
    if len(cave_path) == 0:
        print("地图数据为空，回城重来")
        skill_controller.cast_back_town()
        time.sleep(3.0)
        start()
        return

    path_controller.set_map_data()

    # 转换为单步路径
    cave_path = game_controller.to_each_step_path(cave_path)

    nearest_pos = move_controller.get_nearest_pos(cave_path)
    globals.current_path_index = cave_path.index(nearest_pos)
    last_move_time = 0
    last_go_back_time = 0
    while(True):
        #检查血量
        my_lose_HP = game_controller.get_my_lose_HP()
        # 道士，移动完，先判断血量隐身
        if globals.occupation == globals.Occupation.Taoist:
            if 20 < my_lose_HP:
                skill_controller.cast_heal()
                skill_controller.cast_invisible()
                if game_controller.got_MP_Insufficient_text():
                    trash_controller.try_get_bag_space(1)
        # 法师血量低，可能背包满了，红喝不出来
        elif globals.occupation == globals.Occupation.Magician:
            if 90 < my_lose_HP:
                trash_controller.try_get_bag_space(1)

        #消除系统确定消息框
        while btn_controller.click_sure_btn():
            adb_controller.screenshot(settings.screenshot_path)
        #检测断开消息框
        if game_controller.connection_lose():
            print("断开")
            raise Exception("RESTART")

        if not game_controller.check_level():
            raise Exception("NeedGetMaster")

        if trash_controller.collect_ground_treasures() > 0:
            continue

        #检查宝宝血量是否健康
        if not game_controller.is_pet_healthy():
            if game_controller.select_boss():
                # 攻击boss
                if globals.occupation == globals.Occupation.Taoist:
                    skill_controller.cast_poison()
                    skill_controller.cast_defence()
                    skill_controller.cast_heal()
                    skill_controller.cast_talisman()
                elif globals.occupation == globals.Occupation.Magician:
                    skill_controller.cast_shield()
                    skill_controller.cast_lighting()
            else:
                if time.time() - last_go_back_time > settings.go_back_check_time:
                    # 往回跑，试图召回宠物
                    game_controller.reactive_pet()
                    if globals.occupation == globals.Occupation.Taoist:
                        skill_controller.cast_invisible()
                    elif globals.occupation == globals.Occupation.Magician:
                        skill_controller.cast_shield()
                    move_controller.go_to_previous_point(cave_path)
                    # 移动结束接隐身
                    if globals.occupation == globals.Occupation.Taoist:
                        skill_controller.cast_invisible()
                    game_controller.reactive_pet()
                    last_go_back_time = time.time()

            time.sleep(5.0)
            continue

        if game_controller.check_exp_getting():
            print("经验有增加")
            if time.time() - last_move_time > settings.move_check_time:
                while not game_controller.is_monster_nearby():
                    print("距离上次移动已达{}s，检查当前屏幕无怪，去下一个点".format(str(settings.move_check_time)))
                    move_controller.go_to_next_point(cave_path)
                    # 移动结束接隐身
                    if globals.occupation == globals.Occupation.Taoist:
                        skill_controller.cast_invisible()
                    last_move_time = time.time()
        else:
            print("经验没增加")
            #移动到下一个点
            move_controller.go_to_next_point(cave_path)
            # 移动结束接隐身
            if globals.occupation == globals.Occupation.Taoist:
                skill_controller.cast_invisible()
            last_move_time = time.time()
            while not game_controller.is_monster_nearby():
                move_controller.go_to_next_point(cave_path)
                # 移动结束接隐身
                if globals.occupation == globals.Occupation.Taoist:
                    skill_controller.cast_invisible()
                last_move_time = time.time()


def restart_routine(restart_emulator_adb = False):
    try:
        print("重启游戏")

        # win 下目前看不用重启模拟器和adb
        # if restart_emulator_adb:
        #     adb_controller.restart_emulator()
        #     time.sleep(30)
        #
        #     # mumu才重启adb
        #     if settings.device_address == "emulator-5554":
        #         adb_controller.restart_adb()

        game_controller.restart_game()
        success = game_controller.wait_till_finish_login(120, 1)
        if success:
            print("click login btn success")
            start()
        else:
            print("click login btn failed")
            restart_routine()
    except Exception as e:
        print('exception:', e)
        reason = e.args[0]
        if reason == "RESTART":
            restart_routine()
        elif "NoneType" in reason:
            print("adb 可能断开")
            restart_routine(True)
        else:
            restart_routine()


def start():
    try:
        start_get_exp()
    except Exception as e:
        print('exception:', e)
        reason = e.args[0]
        if reason == "RESTART":
            restart_routine()
        elif reason == "NeedGetMaster":
            print("到达必须拜师等级，停止程序")
            # 回城站着
            move_controller.go_back_town_and_stay()
        elif "NoneType" in reason:
            print("adb 可能断开")
            restart_routine(True)
        else:
            restart_routine()
