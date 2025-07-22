from globals import gb
import pyautogui
from PIL import ImageTk, Image

def screenshot():
    """截取螢幕並顯示在畫布上"""
    global tkinter_image
    gb.screenshot_image = pyautogui.screenshot()
    tkinter_image = ImageTk.PhotoImage(gb.screenshot_image) #將圖片轉換為Tkinter可用的格式
    if not gb.UI.image_id:
        gb.UI.image_id = gb.UI.screenshot_canvas.create_image(0,0, anchor="nw", image=tkinter_image)
    gb.UI.screenshot_canvas.itemconfig(gb.UI.image_id, image=tkinter_image)

def screenshot_loop():
    """截圖循環，適用於循環模式"""
    try:
        if gb.UI.start_screenshot_loop.get() != "1":
            return 0
        screenshot()
        gb.UI.window.after(100,screenshot_loop)
    except Exception :
        print(f"截圖失敗{e}")

def start_rectangle(event,rectangle_data):
    """開始繪製方框"""
    if not rectangle_data.ready_to_label:
        return False
    global start_x, start_y
    color = rectangle_data.color
    start_x, start_y = gb.UI.screenshot_canvas.canvasx(event.x), gb.UI.screenshot_canvas.canvasy(event.y)
    if rectangle_data.rectangle:
        gb.UI.screenshot_canvas.delete(rectangle_data.rectangle)
    rectangle_data.rectangle = gb.UI.screenshot_canvas.create_rectangle(start_x, start_y, start_x, start_y, outline=color, width=2)

def update_rectangle(event,rectangle_data):
    """更新方框大小"""
    if not rectangle_data.ready_to_label:
        return False
    if not rectangle_data.rectangle:
        return False
    x, y = gb.UI.screenshot_canvas.canvasx(event.x), gb.UI.screenshot_canvas.canvasy(event.y)
    gb.UI.screenshot_canvas.coords(rectangle_data.rectangle, start_x, start_y, x, y)

def end_rectangle(rectangle_data):
    """完成方框繪製並記錄座標"""
    if not rectangle_data.ready_to_label:
        return False
    x0, y0, x1, y1 = gb.UI.screenshot_canvas.coords(rectangle_data.rectangle)
    #紀錄座標與方框到rectangle_data類別
    rectangle_data.set_coordinate(x0, y0, x1, y1)
    print(f"Rectangle coordinates: ({x0}, {y0}) to ({x1}, {y1})")
    return True

def repaint_rectangle(rectangle_data):
    """重新繪製方框"""
    try:
        left,top,right,bottom = rectangle_data.get_coordinate()
        color = rectangle_data.color
        rectangle = gb.UI.screenshot_canvas.create_rectangle(left, top, right, bottom, outline=color, width=2)
        rectangle_data.rectangle = rectangle
    except Exception as e:
        print(f"重新繪製方框失敗:{e}")

def paint_save_rectangle():
    """在程式從新啟動時，繪製新的方框"""
    try:
        gb.auto_rectangle.set_coordinate(
            gb.save_data["Auto"]["left"],
            gb.save_data["Auto"]["top"],
            gb.save_data["Auto"]["right"],
            gb.save_data["Auto"]["bottom"])
        gb.B_manual_rectangle.set_coordinate(
            gb.save_data["B_manual"]["left"],
            gb.save_data["B_manual"]["top"],
            gb.save_data["B_manual"]["right"],
            gb.save_data["B_manual"]["bottom"])
        gb.Standard_Setting_rectangle.set_coordinate(
            gb.save_data["Standard_Setting"]["left"],
            gb.save_data["Standard_Setting"]["top"],
            gb.save_data["Standard_Setting"]["right"],
            gb.save_data["Standard_Setting"]["bottom"])
        repaint_rectangle(gb.auto_rectangle)
        repaint_rectangle(gb.B_manual_rectangle)
        repaint_rectangle(gb.Standard_Setting_rectangle)
    except Exception as e:
        print(f"重新繪製方框失敗:{e}")