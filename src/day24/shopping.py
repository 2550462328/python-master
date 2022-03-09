from selenium import webdriver
from selenium.webdriver.common.by import By


# 模拟 商城购物
def mock_shopping_visit():
    broswer_chrome = webdriver.Chrome()

    broswer_chrome.maximize_window()

    broswer_chrome.get('https://www.hisense.com/')

    search_button1 = broswer_chrome.find_element_by_id('form-search')
    search_button1.click()
    search_text1 = broswer_chrome.find_element_by_name('q')
    search_text1.send_keys('冰箱')
    search_text1.submit()
    # 说明
    # find_element_by_xpath("//[@id=‘属性值’]")
    # find_element_by_xpath("//标签名[@id=‘属性值’]"）
    # find_element_by_xpath("//标签名[@name=‘属性值’]"）
    # find_element_by_xpath("//标签名[@class_name=‘属性值’]"）
    broswer_chrome.find_element(By.XPATH, "//span[@data-index = '4']").click()
    broswer_chrome.find_element(By.XPATH, "//div[@class='filter-banner']/span[1]").click()


if __name__ == '__main__':
    mock_shopping_visit()
