# import os
# import PIL.Image as Image
# def calculate_relative_values(image_width, image_height, x1, y1, x2, y2):
#     # 计算相对值
#     relative_x1 = x1 / image_width
#     relative_y1 = y1 / image_height
#     relative_x2 = x2 / image_width
#     relative_y2 = y2 / image_height

#     # 返回相对值
#     return relative_x1, relative_y1, relative_x2, relative_y2

# # 读取图片尺寸
# image = Image.open('D:/10size/023_2700.jpg')

#     # 获取宽度和高度
# width, height = image.size

# x1 = 58
# y1 = 250
# x2 = 119
# y2 = 278

# relative_x1, relative_y1, relative_x2, relative_y2 = calculate_relative_values(width, height, x1, y1, x2, y2)
# print("相对值：", relative_x1, relative_y1, relative_x2, relative_y2)

# #008：1. 0.462 0.0 0.541 0.061  2. 0.741 0.864 0.856 0.983
# #015: 1. 0.462 0.0 0.539 0.075  2. 0.121 0.846 0.229 0.980
# #020: 1. 0.457 0.0 0.544 0.051  2. 0.120 0.840 0.241 0.930
# #023: 1. 0.456 0.0 0.539 0.060  2. 0.117 0.838 0.241 0.932s

def maximize_even_sum(nums, k):
    n = len(nums)
    dp = [[-1] * (k + 1) for _ in range(n + 1)]

    # 初始化 dp 数组
    for i in range(n + 1):
        dp[i][0] = 0

    # 动态规划计算最大偶数和
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            if dp[i -1][j] != -1:
                dp[i][j] = max(dp[i][j], dp[i - 1][j])
            if dp[i - 1][j - 1] != -1:
                temp = dp[i - 1][j - 1] + nums[i - 1]
                if temp % 2 == 0:
                    dp[i][j] = max(dp[i][j], temp)
                    

    return dp[n][k]

# 示例调用
nums = [1, 2, 3, 4, 5]
k = 2
result = maximize_even_sum(nums, k)
print(result)  # 输出: 12
