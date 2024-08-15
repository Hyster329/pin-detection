import os
import cv2
import numpy as np
import math
import shutil
import time

start_time = time.time()
def process_image(image, padding=30, threshold=130, median_kernel=11):
    '''
    图像预处理，尺寸修改，边界填充，转灰度和二值图像
    注意：脚本参数均基于0.3缩放因子优化，不建议修改
    '''
    image_resize = cv2.resize(image, dsize=None, dst=None, fx=0.3, fy=0.3, interpolation=cv2.INTER_NEAREST)
    image_resize = cv2.rectangle(image_resize.copy(), (0, 0), (image_resize.shape[1], padding), (255, 255, 255), -1)
    image_resize = cv2.rectangle(image_resize.copy(), (0, image_resize.shape[0]-padding),
                                 (image_resize.shape[1], image_resize.shape[0]), (255, 255, 255), -1)
    # show_image(image_resize)
    image_gary = cv2.cvtColor(image_resize, cv2.COLOR_BGR2GRAY)
    _, image_bin = cv2.threshold(image_gary, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # _, image_bin = cv2.threshold(image_gary, threshold, 255, cv2.THRESH_BINARY)
    # show_image(image_bin)  # 展示灰度图像
    image_bin = cv2.medianBlur(image_bin, median_kernel)
    return image_resize, image_gary, image_bin


def show_image(image_show):
    '''展示图像，测试使用'''
    cv2.imshow("show", image_show)
    cv2.waitKey()


def rect_detect(image_bin, open_kernel=25, channy_open_kernel=13):
    '''检测针脚所在矩形区域'''
    # 腐蚀灰度图像，开操作去除连通
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_kernel, open_kernel))
    image_bin = cv2.dilate(image_bin.copy(), kernel, 0)
    image_bin = cv2.erode(image_bin.copy(), kernel, 0)
    # show_image(image_bin)
    # 进行边缘检测
    image_canny = cv2.Canny(image_bin, 150, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (channy_open_kernel, channy_open_kernel))
    image_canny = cv2.dilate(image_canny.copy(), kernel, 0)
    image_canny = cv2.erode(image_canny.copy(), kernel, 0)
    # show_image(image_canny)
    # 查找符合要求的矩形轮廓
    contours, hierarchy = cv2.findContours(image_canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 找出轮廓
    BoxArea = []
    for i in range(0, len(contours), 2):
        if cv2.contourArea(contours[i]) > 10000 and cv2.contourArea(contours[i]) < 20000:
            BoxArea.append(i)

    rect_roi_1 = np.zeros(image_bin.shape, np.uint8)

    cv2.fillConvexPoly(rect_roi_1, contours[BoxArea[1]], 255)
    # show_image(rect_roi_1)
    rect_roi_2 = np.zeros(image_bin.shape, np.uint8)
    cv2.fillConvexPoly(rect_roi_2, contours[BoxArea[0]], 255)
    # show_image(rect_roi_2)
    rect_roi_1 = cv2.erode(rect_roi_1, kernel, 0)
    rect_roi_2 = cv2.erode(rect_roi_2, kernel, 0)
    return rect_roi_1, rect_roi_2


def cricles_detect(image_gary, rect_roi):
    """检测针脚中心点，生成中心点坐标的列表"""
    image_gary_temp = image_gary.copy()
    image_gary_temp[rect_roi == 0] = 0
    _, image_bin = cv2.threshold(image_gary_temp, 225, 255, cv2.THRESH_BINARY)
    image_bin = cv2.medianBlur(image_bin, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    image_bin = cv2.dilate(image_bin, kernel, 0)
    cors = []
    num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(image_bin, connectivity=8)
    for i in range(num_labels):
        cors.append(tuple(centroids[i]))
    return cors


def calculate_distance(vec1, vec2):
    '''计算两个点的欧式距离'''
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dist = np.sqrt(np.sum(np.square(vec1 - vec2)))
    return dist


def check_distribution(cors: list, area: int):
    '''判断针脚的分布规律'''
    len_cors = len(cors)
    if area == 1:
        line_num = 0
        for i in range(len_cors-1):
            cor_ls = []
            for j in range(i+1, len_cors):
                vec1 = np.array(cors[i])
                vec2 = np.array(cors[j])
                K = (vec2 - vec1)[0] / ((vec2 - vec1)[1] + 1e-5)
                b = -K * vec2[0] + vec2[1]
                for cor in cors:
                    if abs(K * cor[0] - cor[1] + b) / math.sqrt(K**2 + 1) < 10:
                        cor_ls.append(cor)
            if area == 1:
                if len(cor_ls) >= 6:
                    line_num += 1
        return 1 if line_num >= 2 else 0
    if area == 2:
        dist_list = []
        for i in range(len_cors - 1):
            for j in range(i + 1, len_cors):
                dist = calculate_distance(cors[i], cors[j])
                dist_list.append(dist)
        dist_list.sort()
        check_num = 0
        for i in range(len(dist_list)-1):
            if dist_list[i+1] - dist_list[i] < 6.5:
                check_num += 1
        if check_num >= 3:
            return 1
        else:
            return 0


def checkpin_main(path, padding=30, threshold=130, median_kernel=11, open_kernel=25, channy_open_kernel=13):
    '''
    针脚检测主逻辑函数
    :param path: 图片输入路径
    :param padding: 预处理时对图片上下边界覆盖的矩形高度 default:30
    :param threshold: 灰度图像阈值分割的低阈值 default:130
    :param median_kernel: 原图二值图像中值滤波降噪，滤波器核心尺寸 default:11
    :param open_kernel: 矩形检测阶段开操作去除噪声的核心尺寸 default:30
    :param channy_open_kernel: 开操作去除channy边界检测的相连处，开操作滤波器核心尺寸 default:13
    :return:
    '''
    image = cv2.imread(path)
    image_resize, image_gary, image_bin = process_image(image, padding, threshold, median_kernel)

    # 得到二值化的两个矩形目标
    rect_roi_1, rect_roi_2 = rect_detect(image_bin, open_kernel, channy_open_kernel)

    cors_1 = cricles_detect(image_gary, rect_roi_1)
    cors_2 = cricles_detect(image_gary, rect_roi_2)
    if len(cors_1) >= len(cors_2):
        result_1 = check_distribution(cors_1, 1)
        result_2 = check_distribution(cors_2, 2)
    else:
        result_1 = check_distribution(cors_1, 2)
        result_2 = check_distribution(cors_2, 1)
    if result_1 and result_2:
        return 1
    else:
        return 0


if __name__ == '__main__':
    test = False  # 以下测试
    testname = r"B20210113182345_2.jpg"
    samples_path = r"C:\Users\Hyste\Desktop\samples"
    for name in os.listdir(samples_path):
        sample_path = os.path.join(samples_path, name)
        print(sample_path)
        if test:
            if name == testname:
                try:
                    result = checkpin_main(sample_path)
                    print(result)
                    break
                except IndexError:
                    print("识别异常")
                    break
            else:
                continue
        else:
            try:
                result = checkpin_main(sample_path,
                                       padding=30,
                                       threshold=130,
                                       median_kernel=11,
                                       open_kernel=25,
                                       channy_open_kernel=13)
                if result:
                    shutil.copyfile(sample_path, f"C:/Users/Hyste/Desktop/对的/{name}")
                else:
                    shutil.copyfile(sample_path, f"C:/Users/Hyste/Desktop/错的/{name}")
            except IndexError:
                shutil.copyfile(sample_path, f"C:/Users/Hyste/Desktop/异常/{name}")
                print("识别异常")

    cv2.destroyAllWindows()
# 记录结束时间
end_time = time.time()

# 计算运行时间
run_time = end_time - start_time
print("代码运行时间：", run_time, "秒")