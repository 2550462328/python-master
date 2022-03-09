from selenium import webdriver
from selenium.webdriver.common.by import By


# 模拟 gitee 登录
def mock_gitee_login():
    browser_chrome = webdriver.Chrome()
    browser_chrome.maximize_window()
    browser_chrome.get('http://gitee.com/login')

    browser_chrome.find_element(By.ID, 'user_login').send_keys('2550462328@qq.com')
    browser_chrome.find_element(By.ID, 'user_password').send_keys('13966945097zhang')
    browser_chrome.find_element(By.NAME, 'commit').click()


if __name__ == '__main__':
    mock_gitee_login()
