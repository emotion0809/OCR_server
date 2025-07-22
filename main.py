import UI 
from globals import gb
import json
import os
from rectangle_data import *

def load_save_data():
    try:
        #取得json檔的絕對位置
        current_directory = os.path.dirname(os.path.abspath(__file__))
        print(current_directory)
        gb.json_path = os.path.join(current_directory,"save\\save.json")
        print(gb.json_path)
        #讀取json檔的資料
        if not os.path.isfile(gb.json_path):
            open(gb.json_path, "x") #如果json檔不在創建json檔
        json_file = open(gb.json_path,"r")
        read_data = json_file.read()
        gb.save_data = json.JSONDecoder().decode(read_data)
        json_file.close()
    except Exception as e:
        print(f"存取json檔失敗:{e}" )

if __name__ == '__main__':
    #取得json檔的資料
    load_save_data()
    # 啟動 GUI 主程式
    gb.UI = UI.UI()
    gb.UI.run()
    



