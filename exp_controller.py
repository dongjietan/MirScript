import os
import time
import re
import cv2
import random
import numpy
import datetime

import globals
import settings
import image_processor
import adb_controller
import game_controller
import path_controller
import move_controller
import trash_controller


def start_get_exp():
    print("开始练级")
    adb_controller.connect()

    cave_path = game_controller.get_map_path()
    if len(cave_path) == 0:
        print("程序结束")
        return

    game_controller.set_occupation()

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
                game_controller.cast_heal()
                game_controller.cast_invisible()
                if game_controller.got_MP_Insufficient_text():
                    trash_controller.try_get_bag_space(1)
        # 法师血量低，可能背包满了，红喝不出来
        elif globals.occupation == globals.Occupation.Magician:
            if 90 < my_lose_HP:
                trash_controller.try_get_bag_space(1)

        #消除系统确定消息框
        game_controller.click_sure_btn()
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
                    game_controller.cast_poison()
                    game_controller.cast_defence()
                    game_controller.cast_heal()
                    game_controller.cast_talisman()
                elif globals.occupation == globals.Occupation.Magician:
                    game_controller.cast_shield()
                    game_controller.cast_lighting()
            else:
                if time.time() - last_go_back_time > settings.go_back_check_time:
                    # 往回跑，试图召回宠物
                    game_controller.reactive_pet()
                    if globals.occupation == globals.Occupation.Taoist:
                        game_controller.cast_invisible()
                    elif globals.occupation == globals.Occupation.Magician:
                        game_controller.cast_shield()
                    move_controller.go_to_previous_point(cave_path)
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
                    last_move_time = time.time()
        else:
            print("经验没增加")
            #移动到下一个点
            move_controller.go_to_next_point(cave_path)
            last_move_time = time.time()
            while not game_controller.is_monster_nearby():
                move_controller.go_to_next_point(cave_path)
                last_move_time = time.time()


def restart_routine(restart_emulator_adb = False):
    try:
        print("重启游戏")

        if restart_emulator_adb:
            adb_controller.restart_emulator()
            time.sleep(30)

            # mumu才重启adb
            if settings.device_address == "emulator-5554":
                adb_controller.restart_adb()

        game_controller.restart_game()
        success = game_controller.wait_till_finish_login(120, 1)
        if success:
            if game_controller.active_pet():
                start()
            else:
                print('当前没有宠物，程序终止：道士重新召唤宝宝，自动挂等级，跑图，法师直接下线换道士')
        else:
            game_controller.restart_game()
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
    else:
        print('unknown exception')
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
            # 回城
            move_controller.go_to_town()
        elif "NoneType" in reason:
            print("adb 可能断开")
            restart_routine(True)
        else:
            restart_routine()
    else:
        print('unknown exception')
        restart_routine()
