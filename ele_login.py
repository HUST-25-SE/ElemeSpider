# -*- coding: utf-8 -*-
import json 
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def login_and_cookie_get():
    # 浏览器配置
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    try:
        # 访问登录页面
        driver.get("https://tb.ele.me/wow/msite/act/login")
        
        # 等待并切换到登录iframe
        print("等待登录页面加载...")
        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "alibaba-login-box"))
        )
        
        # 输入手机号
        phone = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="fm-sms-login-id"]'))
        )
        phonenumber = input('请输入手机号,回车键确认:') 
        phone.clear()
        phone.send_keys(phonenumber)
        
        # 勾选同意协议复选框
        try:
            agreement_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "fm-agreement-checkbox"))
            )
            
            if not agreement_checkbox.is_selected():
                agreement_checkbox.click()
                print("已自动勾选同意协议复选框")
            else:
                print("协议复选框已被选中")
                
        except Exception as e:
            print(f"勾选协议复选框时出错: {e}")
        
        # 点击发送验证码
        send_btn = driver.find_element(By.XPATH, "//a[@class='send-btn-link']")
        send_btn.click()
        print("已点击发送验证码，验证码已发送")
        
        # 等待验证码发送完成
        time.sleep(3)
        
        # 直接输入验证码
        vali = input('请输入验证码,回车键确认:') 
        code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="fm-smscode"]'))
        )
        code_input.clear()
        code_input.send_keys(vali)
        print("验证码已输入")
        
        # 点击登录
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_btn.click()
        print("已点击登录")
        
        # 等待登录完成
        time.sleep(5)
        
        # 检查登录是否成功
        try:
            # 切换到默认内容，检查是否还在登录页面
            driver.switch_to.default_content()
            if "alibaba-login-box" in driver.page_source:
                print("登录可能未成功，仍在登录页面")
                # 尝试处理可能的错误信息
                try:
                    error_msg = driver.find_element(By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'msg')]")
                    print(f"错误信息: {error_msg.text}")
                except:
                    print("未找到明确错误信息")
            else:
                print("登录可能成功，已离开登录页面")
        except:
            pass
        
        # 获取cookies
        print("获取cookies...")
        time.sleep(3)
        
        # 获取并保存cookies
        dictCookies = driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        
        # 确保目录存在
        os.makedirs('./data', exist_ok=True)
        
        with open('./data/cookies.json', 'w', encoding='utf-8') as f:
            f.write(jsonCookies)
        print('cookie加载完毕')
        
        # 打印一些调试信息
        print(f"获取到 {len(dictCookies)} 个cookie")
        for cookie in dictCookies:
            if cookie['name'] in ['SID', 'USERID', 'token']:
                print(f"重要cookie: {cookie['name']} = {cookie['value'][:20]}...")
                
    except Exception as e:
        print(f"登录过程出错: {e}")
        import traceback
        traceback.print_exc()
        # 保存当前页面源码用于调试
        with open('./data/error_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("错误页面已保存到 ./data/error_page.html")
    finally:
        input("按回车键关闭浏览器...")
        driver.quit()

def cookie_process():
    try:
        with open("./data/cookies.json", "r", encoding='utf-8') as f:
            load_data = json.load(f)
        
        for i in load_data:
            if i["name"] == "SID":
                mycookie = i["value"]
                return mycookie
        print("未找到SID cookie")
        return None
    except FileNotFoundError:
        print("cookies.json文件不存在，请先运行登录")
        return None
    except Exception as e:
        print(f"处理cookie时出错: {e}")
        return None

# 测试代码
if __name__ == "__main__":
    login_and_cookie_get()
    cookie = cookie_process()
    if cookie:
        print(f"获取到的SID: {cookie[:50]}...")