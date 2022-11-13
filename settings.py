# adb.exe 的路径，模拟器安装路径下的bin文件夹里面有
adb_path = "/Applications/NemuPlayer.app/Contents/MacOS/adb"

# 模拟器的地址
device_address = "emulator-5554"

# 包名
package_name = "com.abc.def"

except_dist = 5

screenshot_path = r"temp_screenshot/screenshot.png"

last_screenshot_path = r"temp_screenshot/last_screenshot.png"

temp_path = []

current_x = 0
current_y = 0

current_path_index = 0

#左上和中间没录
zombie_cave_path = [(14,144),(20,138),(26,132),(33,132),(36,139),(42,145),(47,150),(51,154),(56,159),(61,164)
                    ,(67,164),(67,173),(72,173),(78,173),(78,166),(85,166),(90,160),(94,163),(100,158),(104,154)
                    ,(110,154),(114,154),(120,160),(125,165),(129,169),(133,165),(138,165),(142,169),(146,169)
                    ,(151,164),(156,159),(151,154),(157,148),(149,140),(149,136),(155,130),(155,124),(149,118)
                    ,(146,115),(142,111),(142,105),(142,98),(151,88),(151,78),(158,78),(65,78),(171,72),(177,78)
                    ,(181,82),(171,72),(166,77),(162,73),(158,73),(152,79),(146,73),(140,67),(135,62),(135,52)
                    ,(130,47),(130,40),(136,34),(142,34),(146,38),(154,38),(160,32),(166,26),(172,20),(175,17)
                    ,(170,12),(166,16),(160,10),(158,8),(154,16),(166,28),(154,40),(151,37),(141,37),(134,33),(128,39)
                    ,(123,39),(117,39),(112,34),(107,39),(101,39),(96,39),(90,45),(90,52),(90,60),(86,65),(86,70)
                    ,(86,76),(82,81),(82,85),(78,89),(72,89),(72,95),(66,95),(62,99),(58,103),(50,103),(44,103)
                    ,(39,108),(34,113),(29,118),(29,123),(26,123),(26,131),(20,138),(14,144)]
