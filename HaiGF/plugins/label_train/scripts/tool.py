import cv2
import numpy as np

#图像增强类：用于改善图像的视觉效果，包括增强图像的对比度、亮度、色彩饱和度等函数。
class ImageEnhancement:
    def __init__(self):
        pass

    @staticmethod
    def adjust_contrast(img, factor):
        """
        调整图像的对比度
        :param img: 输入图像
        :param factor: 对比度调整因子，1表示不调整，大于1表示增加对比度，小于1表示降低对比度
        :return: 调整对比度后的图像
        """
       
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        # 增加图像对比度
        v = np.clip(cv2.add(factor*v, 0),0,255)
        v[v < 0] = 0
        v[v > 255] = 255
        v = np.uint8(v)

        hsv = np.uint8(cv2.merge((h, s, v)))
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return img

    @staticmethod
    def adjust_brightness(img, delta):
        """
        调整图像的亮度
        :param img: 输入图像
        :param delta: 亮度调整因子，正数表示增加亮度，负数表示降低亮度
        :return: 调整亮度后的图像
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        # 增加图像亮度
        v1 = np.clip(cv2.add(1*v,delta),0,255)
        v1[v1 < 0] = 0
        v1[v1 > 255] = 255
        res = np.uint8(cv2.merge((h, s, v1)))
        res = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
        return res

    @staticmethod
    def adjust_saturation(img, factor):
        """
        调整图像的色彩饱和度
        :param img: 输入图像
        :param factor: 色彩饱和度调整因子，1表示不调整，大于1表示增加饱和度，小于1表示降低饱和度
        :return: 调整饱和度后的图像
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = hsv[:, :, 1] * factor
        hsv[:, :, 1][hsv[:, :, 1] > 255] = 255
        hsv[:, :, 2] = hsv[:, :, 2] * factor
        hsv[:, :, 2][hsv[:, :, 2] > 255] = 255
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return img

#图像滤波类：用于对图像进行平滑处理，包括高斯滤波、中值滤波、双边滤波等函数。平滑图像、去除噪声、增强边缘函数
class ImageFilter:
    def __init__(self):
        pass

    @staticmethod
    def smooth(img, ksize=3):
        """
        平滑图像
        :param img: 输入图像
        :param ksize: 滤波器大小，必须是正奇数
        :return: 平滑后的图像
        """
        if ksize % 2 == 0:
            ksize = ksize + 1
        img_smoothed = cv2.GaussianBlur(img, (ksize, ksize), 0)
        return img_smoothed

    @staticmethod
    def denoise(img, h=10, h_color=10, template_size=7, search_size=21):
        """
        去除噪声
        :param img: 输入图像
        :param h: 色彩差异阈值
        :param h_color: 空间距离阈值
        :param template_size: 用于计算颜色相似性的窗口大小
        :param search_size: 用于搜索相似性的窗口大小
        :return: 去除噪声后的图像
        """
        img_denoised = cv2.fastNlMeansDenoisingColored(img, None, h, h_color, template_size, search_size)
        return img_denoised

    @staticmethod
    def enhance_edges(img, sigma=0.33):
        """
        增强边缘
        :param img: 输入图像
        :param sigma: 控制边缘强度的参数
        :return: 增强边缘后的图像
        """
        # 计算Canny边缘
        v = np.median(img)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edges = cv2.Canny(img, lower, upper)

        # 增强边缘
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel)
        img_enhanced = cv2.bitwise_and(img, img, mask=edges)

        return img_enhanced
    
    @staticmethod
    def gaussian_blur(img, ksize=3, sigma=0):
        """
        高斯滤波
        :param img: 输入图像
        :param ksize: 滤波器大小，必须是正奇数
        :param sigma: 高斯核的标准差，如果为0，则从ksize计算
        :return: 高斯滤波后的图像
        """
        if ksize % 2 == 0:
            ksize = ksize + 1
        if sigma == 0:
            sigma = (ksize - 1) * 0.5 - 1
        img_blur = cv2.GaussianBlur(img, (ksize, ksize, sigma), 0)
        return img_blur
    
    @staticmethod
    def median_blur(img, ksize=3):
        """
        中值滤波
        :param img: 输入图像
        :param ksize: 滤波器大小，必须是正奇数
        :return: 中值滤波后的图像
        """
        if ksize % 2 == 0:
            ksize = ksize + 1
        img_blur = cv2.medianBlur(img, ksize)
        return img_blur

    @staticmethod
    def bilateral_filter(img, d=5, sigma_color=10, sigma_space=10):
        """
        双边滤波
        :param img: 输入图像
        :param d: 滤波器大小，必须是正奇数
        :param sigma_color: 色彩相似性阈值
        :param sigma_space: 空间距离阈值
        :return: 双边滤波后的图像
        """
        if d % 2 == 0:
            d = d + 1
        img_blur = cv2.bilateralFilter(img, d, sigma_color, sigma_space)
        return img_blur


#图像分割类：用于对图像进行分割，包括基于颜色的分割、基于形状的分割、基于纹理的分割等函数。
class ImageSegmentation:
    def __init__(self):
        pass

    def color_based_segmentation(self, image, lower_color, upper_color):
        """
        基于颜色的图像分割
        :param image: 输入图像
        :param lower_color: 下限颜色阈值
        :param upper_color: 上限颜色阈值
        :return: 二值化分割图像
        """
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        result = cv2.bitwise_and(image, image, mask=mask)
        return result

    def shape_based_segmentation(self, image, threshold):
        """
        基于形状的图像分割
        :param image: 输入图像
        :param threshold: 阈值
        :return: 二值化分割图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)
        return result

    def texture_based_segmentation(self, image, kernel_size):
        """
        基于纹理的图像分割
        :param image: 输入图像
        :param kernel_size: 卷积核大小
        :return: 二值化分割图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        texture = cv2.medianBlur(gray, kernel_size)
        _, binary = cv2.threshold(texture, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        result = cv2.bitwise_and(image, image, mask=binary)
        return result
    
#特征提取类：用于对图像进行特征提取，包括基于颜色的特征提取、基于角点的特征提取、基于形状的特征提取、基于边缘的特征提取、基于纹理的特征提取等函数。
class FeatureExtractor:
    @staticmethod
    def color_histogram(img, bins=16):
        """
        基于颜色的特征提取（直方图）
        :param img: 输入图像
        :param bins: 直方图中bin的数量
        :return: 一个包含直方图数据的一维数组
        """
        hist = cv2.calcHist([img], [0, 1, 2], None, [bins, bins, bins],
                            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    @staticmethod
    def corner_detection(img, max_corners=100):
        """
        基于角点的特征提取
        :param img: 输入图像
        :param max_corners: 返回的角点数量
        :return: 返回包含角点坐标的二维数组
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, max_corners, 0.01, 10)
        corners = corners.reshape((-1, 2))
        return corners

    @staticmethod
    def shape_detection(img):
        """
        基于形状的特征提取
        :param img: 输入图像
        :return: 返回一个元组，包含物体面积和物体周长
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        return area, perimeter

    @staticmethod
    def edge_detection(img):
        """
        基于边缘的特征提取
        :param img: 输入图像
        :return: 返回包含边缘图像的数组
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return edges

    @staticmethod
    def texture_analysis(img, win_size=25):
        """
        基于纹理的特征提取
        :param img: 输入图像
        :param win_size: 纹理分析窗口大小
        :return: 返回一个包含纹理特征的一维数组
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        glcm = cv2.calcGLCM(gray, [0], None, [256], [0, 256])
        features = [cv2.mean(cv2.textureCorrelation(glcm, i))[0] for i in range(win_size)]
        return features

#目标检测与跟踪类：用于对图像进行目标检测与跟踪，包括基于颜色的目标检测与跟踪、基于形状的目标检测与跟踪、基于纹理的目标检测与跟踪等函数。
class ObjectDetection:
    def __init__(self):
        pass

    def color_based_detection(self, image, lower_color, upper_color):
        """
        基于颜色的目标检测与跟踪
        :param image: 输入图像
        :param lower_color: 下限颜色阈值
        :param upper_color: 上限颜色阈值
        :return: 二值化分割图像
        """
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        result = cv2.bitwise_and(image, image, mask=mask)
        return result

    def shape_based_detection(self, image, threshold):
        """
        基于形状的目标检测与跟踪
        :param image: 输入图像
        :param threshold: 阈值
        :return: 二值化分割图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)
        return result

    def texture_based_detection(self, image, kernel_size):
        """
        基于纹理的目标检测与跟踪
        :param image: 输入图像
        :param kernel_size: 卷积核大小
        :return: 二值化分割图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        texture = cv2.medianBlur(gray, kernel_size)
        _, binary = cv2.threshold(texture, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        result = cv2.bitwise_and(image, image, mask=binary)
        return result

