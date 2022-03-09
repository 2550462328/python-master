# pip3 install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By


# 模拟浏览器 打开网站 -> 找到指定文本框 / 按钮 -> 填充文字 / 触发按钮
def mock_browser():
    browser_chrome = webdriver.Chrome()
    browser_chrome.maximize_window()
    # 模拟打开 网页
    browser_chrome.get('https://www.baidu.com')
    # 模拟触发 事件
    browser_chrome.find_element(By.ID, 'kw').send_keys('科大讯飞')
    browser_chrome.find_element(By.ID, 'su').click()
    browser_chrome.close()
    browser_chrome.quit()


if __name__ == '__main__':
    mock_browser()
