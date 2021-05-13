# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger()


class Hkuspace_bot():

    def __init__(self):
        self.driver = ""
        self.cookies = ""
        self.session_id = ""

    def login_space(self, username: str, password: str) -> bool:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        try:
            self.driver.get("http://cc4.hkuspace.hku.hk/cgi-bin/new_login.php")
            self.driver.find_element_by_id("username").send_keys(username)
            self.driver.find_element_by_id("password").send_keys(password)
            self.driver.find_element_by_xpath(
                "/html/body/div[2]/form/div[2]/div[3]/input[4]").click()
            self.cookies = self.driver.get_cookies()
            logger.debug(f"All cookies: {self.cookies}")
            logger.info(f"Login setting is completed!")
            return True
        except:
            self.driver.quit()
            return False

    def check_login(self):
        try:
            self.driver.quit()
            return True
        except Exception as e:
            return False

    def check_status(self):
        try:
            self.driver.find_element_by_xpath(
                "/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[1]/form/p/font/input").click()
            logger.info("The swap class platform is ready!")
            return True
        except:
            self.driver.refresh()
            return False

    def swap_class_check(self, class_id="CCIT4021"):
        self.driver.get("http://cc4.hkuspace.hku.hk/cgi-bin/select.php")
        result = []
        try:
            self.driver.find_element_by_name("ccseid").send_keys(class_id)
            self.driver.find_element_by_xpath(
                "/html/body/center[2]/form[2]/input[3]").click()
            self.driver.execute_script("window.scrollTo(0, 500)")
            self.driver.save_screenshot("class_time_table.png")
            request_data = self.driver.page_source
            soup = BeautifulSoup(request_data, features="html.parser")
            all_rows = soup.find("table").find("table").findAll("tr")[1:]
            for each_row in all_rows:
                course_information = soup.findAll(
                    "big")[1].find("b").text.split("\n")[0]
                logger.debug(f"Course information: {course_information}")
                each_class = {
                    "course_title": course_information.split(":")[1].split("-")[1].strip(),
                    "course_code": course_information.split(":")[1].split("-")[0].strip(),
                    "class": each_row.findAll("td")[0].text,
                    "room": each_row.findAll("td")[1].text,
                    "time": each_row.findAll("td")[2].text,
                    "vacancy": each_row.findAll("td")[3].text
                }
                result.append(each_class)
            self.driver.find_element_by_xpath(
                "/html/body/big/b/table/tbody/tr/td/center/form/input").click()
            return {"code": 200, "data": result}
        except:
            self.driver.find_element_by_xpath(
                "/html/body/center[2]/center/form/input").click()
            return {"code": 200, "data": None}

    def add_drop_class(self, class_drop: str, class_add: str, class_id: str, boost=False, target=20):
        logger.debug(
            f"Drop class code: {class_drop}, Class add code: {class_add}, Class id: {class_id}, Boost mode: {boost}, Target: {target}")
        count = 0
        self.driver.get("http://cc4.hkuspace.hku.hk/cgi-bin/select.php")
        self.driver.find_element_by_xpath(
            "/html/body/center[2]/form[3]/input").click()
        while True:
            self.driver.find_element_by_xpath(
                "/html/body/b/form/blockquote/table/tbody/tr[2]/td[2]/p/font/input").send_keys(class_drop)
            self.driver.find_element_by_xpath(
                "/html/body/b/form/blockquote/table/tbody/tr[2]/td[3]/p/font/input[1]").send_keys(class_add)
            self.driver.find_element_by_xpath(
                "/html/body/b/form/blockquote/table/tbody/tr[2]/td[3]/p/font/input[2]").send_keys(class_id)
            self.driver.find_element_by_xpath(
                "//input[@type='submit' and @value='Submit']").click()
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/b/center/form/center[3]/font/p/input").click()
                self.driver.find_element_by_xpath(
                    "/html/body/center[4]/font/form[1]/input[4]").click()
                self.driver.find_element_by_xpath(
                    "//input[@type='submit' and @value='Go Back to Main Menu']").click()
                return {"code": 200, "message": "Add/drop completed!"}
            except:
                self.driver.find_element_by_xpath(
                    "//input[@type='submit' and @value='Back']").click()
                if boost == False or count >= target:
                    self.driver.get(
                        "http://cc4.hkuspace.hku.hk/cgi-bin/select.php")
                    return {"code": 424, "message": "Fail to add/drop classes"}
            count += 1

    def get_time_table(self):
        self.driver.get("http://cc4.hkuspace.hku.hk/cgi-bin/select.php")
        self.driver.find_element_by_xpath(
            "/html/body/center[2]/form[6]/input").click()
        request_data = self.driver.page_source
        soup = BeautifulSoup(request_data, features="html.parser")
        time_table = soup.findAll("table")[4]
        self.driver.find_element_by_xpath(
            "/html/body/div/font[2]/form/div/div/center/p/input").click()
        return {"code": 200, "message": "Fail to add/drop classes"}


class Parallel_swap():

    def main(self, data):
        username = data["username"]
        password = data["password"]
        bot = Hkuspace_bot()
        bot.login_space(username, password)
        logger.debug(f"Request data: {data}")
        valid = False
        while valid == False:
            valid = bot.check_status()
            time.sleep(.2)
        class_drop = data["request_data"]["origin_code"]
        class_add = data["request_data"]["new_code"]
        class_id = data["request_data"]["new_class"]
        boost = data["request_data"]["boost"]
        if boost == True:
            target = data["request_data"]["crush_num"]
            bot.add_drop_class(class_drop, class_add, class_id, boost, target)
        else:
            bot.add_drop_class(class_drop, class_add, class_id, boost)
