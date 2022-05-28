from os import popen, path

user_home = str(popen(r'echo C:\Users\%USERNAME%').readline()).strip('\n')
user_video = path.join(user_home, 'Videos')
user_photo = path.join(user_home, 'Pictures')
user_document = path.join(user_home, 'Documents')
user_download = path.join(user_home, 'Downloads')
user_music = path.join(user_home, 'Music')
user_onedrive = path.join(user_home, 'OneDrive')
user_menu = path.join(user_home, r'\AppData\Roaming\Microsoft\Windows\Start Menu')
myFile = r'D:\我的文件\我的收藏库'

# find_all 将搜索此文件夹,在find_all里自定义添加选项
find_all = [
    myFile,
    user_menu
]
for _ in range(4, 20, 2):
    try:
        find_all.append([str(i).strip('\n " "') for i in popen('wmic logicaldisk get caption')][_])
    except IndexError:
        pass

search_list = find_all[0:-2]
# 设置过滤精准性，数字越大，精确度越高,最大值为100
filter_intensity = 80

ico = "药丸.png"

APP_TITLE = '药丸搜索 0.0.1beta'

select_task_file = r'./data/TaskDB.json'

task_db = r'./data/TaskDB.db'
