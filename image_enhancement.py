from PIL import Image, ImageDraw

# 取得座標(x, y)附近的像素值
def getpixel(image, x, y):
    pixel_list = []

    # 取得3*3的像素值
    for i in range(-1, 2):
        for j in range(-1, 2):
            pixel = image.getpixel((x + j ,y + i))
            pixel_list.append(pixel)
    
    return(pixel_list)

# 調整像素值大小(像素值要在灰階影像的範圍)
def regulate_pixel(pixel):
    if pixel > 255:
        pixel = 255 
    elif pixel < 0: 
        pixel = 0
    
    return pixel

# 將灰階圖片做二階微分
def Laplacian_Mask(GrayImage):
    width, height = GrayImage.size
    LaplacianImage = Image.new(GrayImage.mode, (width, height) , (0))
    draw = ImageDraw.Draw(LaplacianImage)
    
    # Laplacian Mask
    Mask = [-1, -1, -1,
            -1, 8, -1,
            -1, -1, -1]

    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            new_pixel = 0
            pixel_list = getpixel(GrayImage, x, y)              # 取得灰階圖片中座標(x,y)附近的像素值

            # 取得經過Laplacian Mask(做二階微分)後的像素值
            for index in range(len(pixel_list)):
                new_pixel = new_pixel + (pixel_list[index] * Mask[index])

            new_pixel = regulate_pixel(new_pixel)               # 調整像素值大小
            draw.point((x, y), fill = (new_pixel))              # 將像素值填進新圖中

    return LaplacianImage

# 將灰階圖片加上LaplacianImage
def SharpenNoise(GrayImage, LaplacianImage):
    width, height = GrayImage.size
    SharpenNoiseImage = Image.new(GrayImage.mode, (width, height), (0))
    draw = ImageDraw.Draw(SharpenNoiseImage)

    for x in range(0, width):       
        for y in range(0, height):
            new_pixel = 0
            new_pixel = GrayImage.getpixel((x, y)) + LaplacianImage.getpixel((x, y))        # 將兩者的像素值相加
            new_pixel = regulate_pixel(new_pixel)               # 調整像素值大小
            draw.point((x, y), fill = (new_pixel))              # 將像素值填進新圖中

    return SharpenNoiseImage

# 將灰階圖片做一階微分
def Sobel_Mask(GrayImage):
    width, height = GrayImage.size
    SobelImage = Image.new(GrayImage.mode, (width, height), (0))
    draw = ImageDraw.Draw(SobelImage)

    # Sobel Mask(x_Mask和y_Mask)
    x_Mask = [-1, 0, 1,
              -2, 0, 2,
              -1, 0, 1]
    y_Mask = [-1, -2, -1,
               0, 0, 0,
               1, 2, 1]

    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            new_x_pixel = 0
            new_y_pixel = 0
            pixel_list = getpixel(GrayImage, x, y)              # 取得灰階圖片中座標(x,y)附近的像素值
            
            # 取得經過Sobel Mask(做一階微分)後的像素值
            for index in range(len(pixel_list)):
                new_x_pixel = new_x_pixel + (pixel_list[index] * x_Mask[index])
                new_y_pixel = new_y_pixel + (pixel_list[index] * y_Mask[index])

            new_pixel = abs(new_x_pixel) + abs(new_y_pixel)     # 將兩個新的像素值取絕對值後再相加
            new_pixel = regulate_pixel(new_pixel)               # 調整像素值大小
            draw.point((x, y), fill = (new_pixel))              # 將像素值填進新圖中

    return SobelImage

# 將SobelImage做模糊(去雜訊)
def Blur(SobelImage):
    width, height = SobelImage.size
    BlurImage = Image.new(SobelImage.mode, (width, height), (0))  
    draw = ImageDraw.Draw(BlurImage)

    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            new_pixel = 0
            pixel_list = getpixel(SobelImage, x, y)             # 取得SobelImage中座標(x,y)附近的像素值

            for index in range(len(pixel_list)):
                new_pixel = new_pixel + pixel_list[index]

            new_pixel = new_pixel / 9
            new_pixel = int(regulate_pixel(new_pixel))          # 調整像素值大小
            draw.point((x, y), fill = (new_pixel))              # 將像素值填進新圖中
    
    return BlurImage

# 將BlurImage正規化到0.0~1.0，乘上LaplacianImage
def Normalization(BlurImage, LaplacianImage):
    width, height = BlurImage.size
    NormalizationImage = Image.new(BlurImage.mode, (width, height), (0))
    draw = ImageDraw.Draw(NormalizationImage)

    for x in range(0, width):       
        for y in range(0, height):
            new_pixel = 0
            new_pixel = (BlurImage.getpixel((x, y)) / 255) * LaplacianImage.getpixel((x,y))     # 將BlurImage正規化到0.0~1.0，乘上LaplacianImage
            new_pixel = regulate_pixel(new_pixel)               # 調整像素值大小
            draw.point((x, y), fill = (int(new_pixel)))         # 將像素值填進新圖中

    return NormalizationImage

# 將NormalizationImage加上灰階圖片
def Sharpen(GrayImage, NormalizationImage):
    width, height = GrayImage.size
    SharpenImage = Image.new(GrayImage.mode, (width, height), (0)) 
    draw = ImageDraw.Draw(SharpenImage)

    for x in range(0, width):       
        for y in range(0, height):
            new_pixel = GrayImage.getpixel((x, y)) + NormalizationImage.getpixel((x, y))        # 將兩者的像素值相加
            new_pixel = regulate_pixel(new_pixel)               # 調整像素值大小
            draw.point((x, y), fill = (int(new_pixel)))         # 將像素值填進新圖中
    
    return SharpenImage

# 將銳化後的圖調高1.1倍的亮度
def Increase_Brightness(SharpenImage):
    width, height = SharpenImage.size
    SharpenBrightnessImage = Image.new(SharpenImage.mode, (width, height), (0)) 
    draw = ImageDraw.Draw(SharpenBrightnessImage)

    for x in range(0, width):       
        for y in range(0, height):
            new_pixel = SharpenImage.getpixel((x, y)) * 1.1     # 將像素值調高1.1倍的亮度
            new_pixel = regulate_pixel(new_pixel)               # 調整像素值大小
            draw.point((x, y), fill = (int(new_pixel)))         # 將像素值填進新圖中
    
    return SharpenBrightnessImage

def main():
    OriginalImage = Image.open('Crescent_Bay.jpg')              # 載入原圖

    # 創建灰階的圖
    GrayImage = OriginalImage.convert('L')                      # 轉成灰階圖片(轉換公式: L = R * 299/1000 + G * 587/1000+ B * 114/1000)
    GrayImage.save( "GrayImage.jpg" )

    # 創建二階微分後的圖
    LaplacianImage = Laplacian_Mask(GrayImage)                  # 將灰階圖片做二階微分
    LaplacianImage.save( "LaplacianImage.jpg" )

    # 創建有雜訊的銳化圖片
    SharpenNoiseImage = SharpenNoise(GrayImage, LaplacianImage) # 將灰階圖片加上LaplacianImage
    SharpenNoiseImage.save( "SharpenNoiseImage.jpg" )

    # 創建一階微分後的圖
    SobelImage = Sobel_Mask(GrayImage)                          # 將灰階圖片做一階微分
    SobelImage.save( "SobelImage.jpg" )

    # 創建模糊後的圖
    BlurImage = Blur(SobelImage)                                # 將SobelImage做模糊(去雜訊)
    BlurImage.save( "BlurImage.jpg" )

    # 創建正規化後的圖
    NormalizationImage = Normalization(BlurImage, LaplacianImage)       # 將BlurImage正規化到0.0~1.0，乘上LaplacianImage
    NormalizationImage.save( "NormalizationImage.jpg" )

    # 創建銳化後的圖 
    SharpenImage = Sharpen(GrayImage, NormalizationImage)       # 將NormalizationImage加上灰階圖片
    SharpenImage.save( "SharpenImage.jpg" )

    # 創建1.1倍亮度的銳化圖
    SharpenBrightnessImage = Increase_Brightness(SharpenImage)          # 將NormalizationImage加上灰階圖片
    SharpenBrightnessImage.save( "SharpenBrightnessImage.jpg" )


if __name__ == '__main__':
    main()