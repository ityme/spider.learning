import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By


class LoginMail163:
    def __init__(self, login_url: str):
        self.driver = self.create_driver()
        self.login_url = login_url

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def create_driver(self):
        options = webdriver.EdgeOptions()
        options.add_experimental_option(
            # 禁止浏览器加载图片
            "prefs",
            {"profile.managed_default_content_settings.images": 2},
        )
        
        # 隐藏“正在受到自动软件的控制”信息栏
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 关闭自动化扩展
        options.add_experimental_option("useAutomationExtension", False)

        # 设置代理服务器
        # options.add_argument('--proxy-server=http://127.0.0.1:7896')

        self.driver = webdriver.Edge(
            service=Service(
                executable_path="E:/ityme/download/edgedriver_win64/msedgedriver.exe"
            ),
            options=options,
        )
        self.driver.maximize_window()

        return self.driver

    def open_login_email(self):
        self.driver.get(self.login_url)
        time.sleep(2)

    def login(self, username, password):
        iframe = self.driver.find_element(By.XPATH, "//div[@id='loginDiv']/iframe")
        self.driver.switch_to.frame(iframe)
        time.sleep(2)

        self.driver.find_element(By.XPATH, "//input[@name='email']").send_keys(username)

        time.sleep(4)
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(
            password
        )

        time.sleep(1)
        self.driver.find_element(By.XPATH, "//a[@id='dologin']").click()
        time.sleep(5)


def main():
    login_url = "https://mail.163.com/"
    username = input("请输入你的邮箱账号:")
    password = input("请输入你的邮箱密码:")
    client = LoginMail163(login_url)
    client.open_login_email()
    client.login(username, password)


if __name__ == "__main__":
    main()
