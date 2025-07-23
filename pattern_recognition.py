from globals import gb
import pytesseract
import numpy as np
from PIL import Image

def OCR(rectangle):
    """圖片文字辨識"""
    try:
        image = split_image(rectangle)
        text = pytesseract.image_to_string(image, lang='eng')
        return text
    except Exception as e:
        print(f"文字辨識失敗:{e}")
        return "error"
    
def loop_pattern_recognition():
    """持續執行圖片辨識的背景執行緒"""
    try:
        Standard_Setting = OCR(gb.register_hint_rectangle)
        #條件符合後向KVM程式，傳送執行命令
        gb.send_message_to_kvm = "The data have changed. Do you register the data?" in Standard_Setting
        print(gb.send_message_to_kvm)
    except Exception as e:
        print(f"圖片辨識失敗:{e}")
    gb.UI.window.after(100,loop_pattern_recognition)
        

def calculate_color_pixel_ratio(rectangle, color):
    """計算顏色的比例"""
    if not rectangle.rectangle: #如果沒標註方框則不執行
        return 0
    try:
        image = split_image(rectangle)
        # 轉換為 NumPy 陣列
        image_array = np.array(image)
        # 提取 RGB 通道
        red_channel = image_array[:, :, 0]
        green_channel = image_array[:, :, 1]
        blue_channel = image_array[:, :, 2]
        # 找出符合指定顏色條件的像素
        if color == "red":
            color_pixels = (red_channel > 150) & (green_channel < 100) & (blue_channel < 100)
        if color == "white":
            color_pixels = (red_channel > 200) & (green_channel > 200) & (blue_channel > 200)
        # 計算指定顏色像素的數量和總像素數量
        color_pixel_count = np.sum(color_pixels)
        total_pixel_count = image_array.shape[0] * image_array.shape[1]
        # 計算比例
        color_pixel_ratio = color_pixel_count / total_pixel_count
        return color_pixel_ratio
    except Exception as e:
        print(f"顏色比例計算失敗:{e}")
        return 0

def split_image(rectangle):
    """分割圖片"""
    if not rectangle.rectangle: #如果沒標註方框則不執行
        return ""
    try:
        #取得方框的邊界座標
        left,top,right,bottom = rectangle.get_coordinate()

        #依照方框切割圖片
        original_image = gb.screenshot_image
        split_image = original_image.crop((left,top, right, bottom))
        return(split_image)
    except Exception as e:
        print(f"圖片分割失敗:{e}")
