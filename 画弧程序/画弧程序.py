import PIL
from PIL import Image       #用于图像生成、读取、保存、调整尺寸等
from PIL import ImageDraw   #用于绘图
import numpy as np
import math

#混合颜色
def mix_color(color1, color2, k):
        return [int(color1[0] * (1 - k) + color2[0] * k),
                int(color1[1] * (1 - k) + color2[1] * k),
                int(color1[2] * (1 - k) + color2[2] * k)]

class ArcDrawer:
    def __init__(self, size, background_color):
        self.size = size
        self.background_color = background_color
        self.img = Image.new('RGB', (size, size), background_color)
    #画弧线
    def draw_arc(self, acr_color, inner_r, outer_r, start_theta, end_theta):
        img_array = np.array(self.img)
        for i in range(self.size):
            for j in range(self.size):
                y = self.size / 2 - i
                x = j - self.size / 2
                if x == 0 and y == 0:
                    theta = 0
                elif x == 0:
                    if y > 0:
                        theta = 0
                    else:
                        theta = math.pi
                else:
                    r = (x**2 + y**2) ** 0.5
                    theta = math.acos(y / r)
                    if x < 0:
                        theta += math.pi
                if start_theta <= theta and theta < end_theta:
                    if inner_r - 1 < r and r < inner_r:
                        img_array[i, j] = mix_color(acr_color, self.background_color, inner_r - r)
                    elif inner_r <= r and r < outer_r:
                        img_array[i, j] = acr_color
                    elif outer_r <= r and r < outer_r + 1:
                        img_array[i, j] = mix_color(acr_color, self.background_color, r - outer_r)
        img2 = Image.fromarray(img_array)
        self.img = img2
        
    def get_image(self):
        return self.img

arc_drawer = ArcDrawer(240, (102,204,255))
arc_drawer.draw_arc((255,255,255),100,110,0,1)
arc_drawer.draw_arc(mix_color((255,255,255),(102,204,255),0.5),100,110,1,math.pi * 2)
img = arc_drawer.get_image()
img.show()
