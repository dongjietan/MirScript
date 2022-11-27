# 包名activity查看方法
# win: adb shell dumpsys window | findstr mCurrentFocus
# mac: adb shell dumpsys window | grep mCurrentFocus
# 获取UserId
# win: adb shell ps | findstr air.com.PaladinOfMarphaNew
# mac: adb shell ps | grep air.com.PaladinOfMarphaNew

# adb.exe 的路径，模拟器安装路径下的bin文件夹里面有
adb_path = "/Applications/NemuPlayer.app/Contents/MacOS/adb"

# 模拟器的地址
device_address = "emulator-5554"

# 包名
package_name = "air.com.PaladinOfMarphaNew"

# 包启动activity
package_activity = "AppEntry"

# 获取UserId, mumu 原生 0, #N1 10, #N2 11, #N3 12, #N4 13
package_UserId = "10"

# 截屏保存路径
screenshot_path = r"temp_screenshot/screenshot.png"

# 检查屏幕是否有怪间隔时间（距离上次移动），单位秒
move_check_time = 40

# 读取当前坐标失败，尝试重新读取最大次数
read_coordinate_fail_limit = 60

# 最大尝试移动次数
move_try_limit = 60

# 单次移动距离
one_time_move_distance = 8

# 检测未拜师最大尝试次数（容错）
check_has_master_fail_limit = 10

########### 练级路径 ###########
# 僵尸洞二层路径
zombie_cave_path = [(14,144),(20,138),(26,132),(33,132),(36,139),(42,145),(47,150),(51,154),(56,159),(61,164)
                    ,(67,164),(67,173),(72,173),(78,173),(78,166),(85,166),(90,160),(94,163),(100,158),(104,154)
                    ,(110,154),(114,154),(120,160),(125,165),(129,169),(133,165),(138,165),(142,169),(146,169)
                    ,(151,164),(156,159),(151,154),(157,148),(149,140),(149,136),(155,130),(155,124),(149,118)
                    ,(146,115),(142,111),(142,105),(142,98),(151,88),(151,78),(158,78),(165,78),(171,72),(177,78)
                    ,(181,82),(171,72),(166,77),(162,73),(158,73),(152,79),(146,73),(140,67),(135,62),(135,52)
                    ,(130,47),(130,40),(136,34),(142,34),(146,38),(154,38),(160,32),(166,26),(172,20),(175,17)
                    ,(170,12),(166,16),(160,10),(158,8),(154,16),(166,28),(154,40),(151,37),(141,37),(134,33)
                    ,(128,39),(123,39),(117,39),(112,34),(107,39),(101,39),(96,39),(90,45),(90,52),(90,60),(86,65)
                    ,(86,70),(86,76),(93,83),(100,90),(100,100),(100,109),(106,115),(113,122),(116,134),(113,122)
                    ,(106,115),(100,109),(100,100),(100,90),(93,83),(86,76),(82,81),(82,85),(78,89),(72,89),(72,95)
                    ,(66,95),(62,99),(58,103),(50,103),(44,103),(39,108),(31,100),(31,90),(25,84),(25,74),(18,67)
                    ,(25,60),(33,52),(33,44),(33,36),(39,42),(31,50),(31,57),(21,67),(32,78),(23,87),(32,96)
                    ,(32,110),(27,105),(22,110),(28,116),(22,122),(28,128),(20,138),(14,144)]


# 生死之间路径
centipede_cave_path = [(15,55),(21,61),(26,61),(31,61),(39,67),(46,74),(52,80),(59,80),(65,80),(71,80),(76,75),
                        (81,70),(81,64),(81,56),(73,48),(64,48),(58,42),(52,36),(46,30),(41,25),(35,19),(29,13),
                        (26,17),(17,17),(24,17),(31,17),(37,17),(44,25),(52,32),(59,39),(59,53),(52,53),(46,53),
                        (40,59),(34,65),(26,57),(19,57),(13,57)]

test_path = [(60,78),(62,76),(64,76),(64,78),(61,81),(60,80),(59,80)]

# 押镖
ya_biao_path = [(439,207),(467,207),(467,307),(500,340),(500,357),(517,373),(539,373),(626,460),(630,460),(640,470)
                ,(640,475),(652,487),(652,492),(662,502),(662,508),(677,523),(689,523),(754,588),(794,588),(797,591)
                ,(797,595),(807,605),(808,611),(838,641)]
