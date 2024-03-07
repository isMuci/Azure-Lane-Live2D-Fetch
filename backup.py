import subprocess
from selenium import webdriver
from selenium.webdriver.edge.options import Options


# 连接浏览器
def linkEdge():
    print('正在启动浏览器......')
    # msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\zlh13\AppData\Local\Microsoft\Edge\User Data"
    subprocess.Popen(
        f'msedge.exe --remote-debugging-port=9225 --user-data-dir="C:\Users\Muci\AppData\Local\Microsoft\Edge\User Data"')

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:9225")
    options.page_load_strategy = 'eager'

    print('正在连接浏览器......')
    browser = webdriver.Edge(options=options)
    return browser

def linkWeb(material):
    browser = linkEdge()
    try:
        print('正在打开铁道站养成计算页面...')
        browser.get("https://blhx.willlan.net/")
    except:  # 捕获timeout异常
        print('打开失败，停止加载页面....')
        browser.execute_script('window.stop()')  # 执行Javascript来停止页面加载 window.stop()

    print(f'已经打开 {browser.title} ......')