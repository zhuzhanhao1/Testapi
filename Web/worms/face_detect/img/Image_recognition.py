import pytesseract
from PIL import Image

image = Image.open("./caozuo.png")
code = pytesseract.image_to_string(image,lang="chi_sim")
print(code)



# 实现思路
# 1、截取元素位置、大小
# 2、获取元素位置、大小
# 3、截取元素图片并保存

# 时间格式进行格式化
# def time_format():
#     current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
#     return current_time
#
#
# # 区域截图（对指定的区域/元素截图）
# def element_screenshot(element):
#     # 截取全屏图片
#     driver.save_screenshot(".\\image\\full.png")
#     # 获取element的顶点坐标
#     x_Piont = element.location['x']
#     y_Piont = element.location['y']
#     # 获取element的宽、高
#     element_width = x_Piont + element.size['width']
#     element_height = y_Piont + element.size['height']
#
#     picture = Image.open(".\\image\\full.png")
#
#     picture = picture.crop((x_Piont, y_Piont, element_width, element_height))
#
#     '''
#     去掉截图下端的空白区域
#     '''
#     driver.execute_script(
#         """
#         $('#main').siblings().remove();
#         $('#aside__wrapper').siblings().remove();
#         $('.ui.sticky').siblings().remove();
#         $('.follow-me').siblings().remove();
#         $('img.ui.image').siblings().remove();
#         """
#     )
#
#     picture.save(".\\image" + time_format() + ".png")
#
#
# driver = webdriver.Chrome()
# driver.get("http://www.baidu.com/")
# driver.maximize_window()
#
# # 要截取的目标元素
# element = driver.find_element_by_id("su")
# # 调用element_screenshot()方法
# element_screenshot(element)
#
# sleep(2)
# driver.quit()
#
#
# def get_image(driver):  # 对验证码所在位置进行定位，然后截取验证码图片
#     img = driver.find_element_by_class_name('code')
#     time.sleep(2)
#     location = img.location
#     print(location)
#     size = img.size
#     left = location['x']
#     top = location['y']
#     right = left + size['width']
#     bottom = top + size['height']
#
#     page_snap_obj = get_snap(driver)
#     image_obj = page_snap_obj.crop((left, top, right, bottom))
#     # image_obj.show()
#     return image_obj  # 得到的就是
