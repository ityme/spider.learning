import time
from DrissionPage.common import By
from DrissionPage import ChromiumPage, ChromiumOptions

# 配置Edge浏览器路径
options = ChromiumOptions()
options.set_browser_path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')

driver = ChromiumPage(addr_or_opts=options)


driver.get("https://www.sogou.com/")

driver.set.window.max()


time.sleep(5)

driver.quit()
