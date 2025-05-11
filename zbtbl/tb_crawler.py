# 吴昊东 2022210027
# 从淘宝爬取商品信息并存入MySQL数据库
# 参考 https://blog.csdn.net/weixin_48266589/article/details/135303310

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

# 商品关键词
KEYWORD = "平板手写笔"
# 数据库表名
MYSQL_TABLE = "whd"
# Edge浏览器用户数据目录
EDGE_UESR_DATA_DIR = (
    "C:\\Users\\吴昊东\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"
)


# MySQL 数据库连接配置
db_config = {
    "host": "47.93.189.31",
    "port": 3306,
    "user": "inklue",
    "password": "20231017ink",
    "database": "lab4",
    "charset": "utf8mb4",
}

# 创建 MySQL 连接对象
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 打开浏览器
edge_options = webdriver.EdgeOptions()
# 使用用户配置文件, 用于保留登录状态
edge_options.add_argument("user-data-dir=" + EDGE_UESR_DATA_DIR)
driver = webdriver.Edge(options=edge_options)
driver.maximize_window()

# 打开淘宝
driver.get("https://www.taobao.com")
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
)

# 搜索关键词
print("正在搜索")
wait = WebDriverWait(driver, 15)
search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
submit = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")
    )
)
search_input.send_keys(KEYWORD)
submit.click()


# 获取商品信息
def get_goods():
    html = driver.page_source
    doc = pq(html)
    # 获取一页种所有商品卡片对象的列表
    items = doc(".doubleCard--gO3Bz6bu").items()
    # 循环处理列表中的每一个商品
    for item in items:
        # 获取商品的id，这是商品在淘宝中的唯一编号
        good_id = item.find(".wwWrap--hD8_39lb span[data-item]").attr("data-item")
        name = item.find(".title--qJ7Xg_90 span").text()
        # 价格由整数和小数两部分组成
        price_int = item.find(".priceInt--yqqZMJ5a").text()
        price_float = item.find(".priceFloat--XpixvyQ1").text()
        if price_int and price_float:
            price = price_int + price_float
        else:
            price = "0.0"
        # 在页面同一位置显示的商品信息有多种来源
        # 首先可能是商品参数，其次可能是排行榜信息，最后可能是秒杀促销信息
        info = item.find(".text--eAiSCa_r").text()
        if not info:
            info = item.find(".rankTitle--yz_cx9ah").text()
            if not info:
                info = item.find(".innerkillText--e3OKxpDk").text()
        shop = item.find(".shopNameText--DmtlsDKm").text()
        sales = item.find(".realSales--XZJiepmt").text()
        city = item.find(".procity--wlcT2xH9").text()
        product = {
            "id": good_id,
            "name": name,
            "type": KEYWORD,
            "price": price,
            "info": info,
            "shop": shop,
            "sales": sales,
            "city": city,
        }
        # 将商品信息存入数据库
        save_to_mysql(product)


# 保存数据到 MySQL
def save_to_mysql(result):
    try:
        sql = """
        INSERT INTO {} (id, name, type, price, info, shop, sales, city)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """.format(
            MYSQL_TABLE
        )
        cursor.execute(
            sql,
            (
                result["id"],
                result["name"],
                result["type"],
                result["price"],
                result["info"],
                result["shop"],
                result["sales"],
                result["city"],
            ),
        )
        conn.commit()
        print("存储到MySQL成功: ", result)
    except Exception as e:
        print("存储到MYSQL出错: ", result, e)


# 启动
if __name__ == "__main__":
    # 循环直到输入q
    # 虽然可以实现自动翻页，但是不稳定，所以最终采用了手动翻页
    while True:
        usr_input = input("翻页完成后按回车继续, 输入q结束")
        if usr_input == "q":
            break
        else:
            get_goods()

