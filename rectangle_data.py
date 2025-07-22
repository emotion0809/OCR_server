class rectangle_data:
    def __init__(self,color):
        self.rectangle = None
        self.left = None
        self.top = None
        self.right = None
        self.bottom =  None
        self.ready_to_label = False
        self.color = color
    
    def set_coordinate(self,left,top,right,bottom):
        """紀錄方框座標"""
        self.left, self.top, self.right, self.bottom = left, top, right, bottom

    def get_coordinate(self):
        """回傳方框座標"""
        return [self.left,self.top,self.right,self.bottom]
    
    def get_coordinate_dict(self):
        """回傳方框座標dict格式"""
        return {"left": self.left,"top": self.top,"right": self.right,"bottom": self.bottom}