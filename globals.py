"""區域變數儲存"""
from rectangle_data import rectangle_data
from threading import Event

class Config:
    def __init__(self):
        self.stop_event = Event()
        self.auto_rectangle = rectangle_data("green")
        self.B_manual_rectangle = rectangle_data("purple")
        self.Standard_Setting_rectangle = rectangle_data("red")
        self.UI = None
        self.screenshot_image = None
        self.send_message_to_kvm = False
        self.json_path = "./save/save.json"
        self.save_data = {}

gb = Config()



