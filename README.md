# Image_Enhancement
對圖片進行銳化，使其更能突顯出細節(線條與邊界)。

## 環境需求
- python 3.6+
- Pillow 8.0.1
### PIP 安裝 requirements.txt 的套件
```
pip install -r requirements.txt
```
## Demo
```
python image_enhancement.py
```
## 結果說明
- GrayImage.jpg : 將原圖轉成灰階圖片(轉換公式: L = R * 299/1000 + G * 587/1000+ B * 114/1000)
- LaplacianImage.jpg : 將灰階圖片做二階微分
- SharpenNoiseImage.jpg : 將灰階圖片加上LaplacianImage
- SobelImage.jpg : 將灰階圖片做一階微分
- BlurImage.jpg : 將SobelImage做模糊(去雜訊)
- NormalizationImage.jpg : 將BlurImage正規化到0.0~1.0，乘上LaplacianImage
- SharpenImage.jpg : 將NormalizationImage加上灰階圖片
- SharpenBrightnessImage.jpg : 將SharpenImage調高的1.1倍亮度
