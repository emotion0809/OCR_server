from globals import gb
import canvas_updata as cu
import pattern_recognition as pr
import TCP_socket as tsk
import threading
import json
import sys
import time
import tkinter as tk

class UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("720x450+0+0")
        self.window.title(f"OCR {gb.save_data.get('OCR_ID', 'Unknown')}")
        self.image_id = None
        
        self.setup_ui()
        self.setup_bindings()

    def setup_ui(self):
        #主要框架
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill="both",expand=1)

        #第二框架
        self.second_frame = tk.Frame(self.main_frame,bg="#FFFFFF")
        self.second_frame.pack(fill="both",side="top",expand=1)

        #第三框架
        self.third_frame = tk.Frame(self.second_frame,bg="#FFFFFF")

        #第四框架
        self.fourth_frame = tk.LabelFrame(self.second_frame, text='標註',bg="#FFFFFF")

        #放置第二框架的物件
        self.third_frame.pack(side="left",fill="both",expand=1)
        self.fourth_frame.pack(side="right",fill="both",pady=5,padx=5)

        #新增截圖案紐
        self.button_screenshot = tk.Button(
            self.third_frame,text="截圖",
            font=("Arial",10,"bold"),
            width=8,
            bg = "#F3F3FA",
            activebackground = "#5A5AAD",
            command=self.press_button_screenshot)

        #新增截圖循環選項
        self.start_screenshot_loop = tk.StringVar()
        self.start_screenshot_loop.set(1)
        self.check_screenshot_loop = tk.Checkbutton(self.third_frame,
            text="loop",
            font=("Arial",8,"bold"),
            variable=self.start_screenshot_loop,
            command=self.click_screenshot_loop)
    
        #放置第三三框架的物件
        self.button_screenshot.grid(row=0,column=0,padx=20,pady=5,ipady=3)
        self.check_screenshot_loop.grid(row=1,column=0,padx=20,pady=3)

        #新增標註按鈕
        self.button_label_register_hint = tk.Button(
            self.fourth_frame,text="Register hint",
            font=("Arial",8,"bold"),
            width=15,
            bg = "#F3F3FA",
            command=lambda: self.press_button_label("Register hint")
        )
    
        self.button_label_register_hint.grid(row=0,column=0,padx=5,pady=15,ipady=3)
    
        #第三框架
        self.third_frame = tk.Frame(self.main_frame)
        self.third_frame.pack(fill="both",side="top",expand=1)

        #創建畫布
        self.screenshot_canvas = tk.Canvas(self.third_frame)

        
        #新增滾動條
        self.xscollbar = tk.Scrollbar(self.third_frame, orient="horizontal",command=self.screenshot_canvas.xview)
        self.yscollbar = tk.Scrollbar(self.third_frame, orient="vertical",command=self.screenshot_canvas.yview)

        #綁定畫布
        self.screenshot_canvas.configure(xscrollcommand=self.xscollbar.set, yscrollcommand=self.yscollbar.set)

        #設定滾動條的範圍
        self.screenshot_canvas.bind("<Configure>",lambda e: self.screenshot_canvas.configure(scrollregion= self.screenshot_canvas.bbox("all")))

        #放置第三框架的物件
        self.xscollbar.pack(side="bottom",fill="x",ipadx=20)
        self.yscollbar.pack(side="right",fill="y",ipady=20)
        self.screenshot_canvas.pack(fill="both",expand=1)

    def setup_bindings(self):
        # 綁定事件
        self.screenshot_canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.screenshot_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.screenshot_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def run(self):
        #啟動並隱藏視窗
        self.window.protocol("WM_DELETE_WINDOW", self.close_application)
        self.window.state("iconic")
        self.window.after(100,self.open_application)
        self.window.mainloop()

    def toggle_labeling(self,rectangle_data,button):
        """準備或取消標記作業作業"""
        is_labeling = rectangle_data.ready_to_label
        # 取消所有標註
        gb.register_hint_rectangle.ready_to_label = False
        for buttons in [self.button_label_register_hint]:
            buttons["bg"] = "#F3F3FA"

        if not is_labeling:
            gb.ready_to_label_something = True
            rectangle_data.ready_to_label = True
            button["bg"] = "#0080FF"
        else:
            gb.ready_to_label_something = False
            rectangle_data.ready_to_label = False

    def cancel_label(self,cancel_button):
        """取消標記的作業"""
        cancel_button['bg'] = "#F3F3FA"
        gb.ready_to_label_something = False
        return False

    def save_coordinate_to_json(self,rectangle_name,rectangle_data):
        """紀錄座標到json檔"""
        global json_file
        try:
            gb.save_data[rectangle_name] = rectangle_data.get_coordinate_dict()
            write_data = json.dumps(gb.save_data) #將資料重dict轉換為json格式
            json_file = open(gb.json_path,"w")
            json_file.write(write_data)
            json_file.close()
        except Exception as e:
            print(f"儲存json資料失敗:{e}")

    def after_finish_label(self,rectangle_name,rectangle_data,button):
        rectangle_data.ready_to_label = self.cancel_label(button) #取消標註作業
        self.save_coordinate_to_json(rectangle_name,rectangle_data) # 存檔

    #region UI互動
    def press_button_screenshot(self):
        """觸發截圖動作，並重新繪製方框"""
        cu.screenshot()

    def press_button_label(self,rectangle_type):
        rectangle_map = {
            "Register hint": (gb.register_hint_rectangle, self.button_label_register_hint),
        }
        rectangle, button = rectangle_map.get(rectangle_type, (None, None))
        if rectangle:
            self.toggle_labeling(rectangle, button)

    def click_screenshot_loop(self):
        """啟動截圖循環的執行緒"""
        thread_screenshot = threading.Thread(target=cu.screenshot_loop)
        thread_screenshot.start()

    def on_mouse_press(self, event):
        """滑鼠按下事件處理"""
        cu.start_rectangle(event,gb.register_hint_rectangle) #標註Standard Setting

    def on_mouse_drag(self, event):
        """滑鼠拖曳事件處理"""
        cu.update_rectangle(event,gb.register_hint_rectangle) #標註Standard Setting

    def on_mouse_release(self, event):
        """滑鼠釋放事件處理"""
        #完成標註Standard_Setting
        if cu.end_rectangle(gb.register_hint_rectangle):
            self.after_finish_label("Register_hint",gb.register_hint_rectangle,self.button_label_register_hint)

    def open_application(self):
    # 啟動循環截圖執行緒
        cu.screenshot_loop()
        pr.loop_pattern_recognition()
    # 啟動 TCP 背景執行緒
        thread_TCP_server = threading.Thread(target= tsk.running_TCP_server, daemon=True)
        thread_TCP_server.start()
    # 重新繪製方框
        cu.paint_save_rectangle()

    def close_application(self):
        """關閉應用程式"""
        gb.stop_event.set()
        try:
            json_file.close()
        except:
            print("json檔已經關閉")
        self.window.destroy()
        time.sleep(5)
        sys.exit()
    #endregion



