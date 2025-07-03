import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException

class HiristBot:
    def __init__(self, email, password, skill, experience, locations, skill_search_apply):
        self.email = email
        self.password = password
        self.skill = skill
        self.experience = experience
        self.locations = locations
        self.skill_search_apply = skill_search_apply
        
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://www.hirist.tech/")
        self.driver.find_element(By.XPATH, "//button[.//p[text()='Jobseeker Login']]").click()
        self.driver.find_element(By.XPATH, "//a[normalize-space()='Sign In']").click()
        self.driver.find_element(By.NAME, "email").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[normalize-space()='Login']").click()
        time.sleep(5)

    def search_jobs(self):
        if self.skill_search_apply:
            # self.driver.find_element(By.CSS_SELECTOR, ".icon-search-big.search-icon").click()
            search_magnifier = self.driver.find_element(By.XPATH, "//img[@alt='Search']")
            search_magnifier.click()
            # search_box = self.driver.find_element(By.XPATH, "//input[@class='sc-lkqHmb ivKHiM']")
            search_box = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter skills/designations/companies']")
            search_box.send_keys(self.skill)
            exp_dropdown = self.driver.find_element(By.XPATH, "//div[contains(@class, 'filters experience')]//div[contains(@class, 'sc-')]")
            exp_dropdown.click()
            self.driver.find_element(By.XPATH, f"(//li[@value='{self.experience}'])[1]").click()
            self.driver.find_element(By.XPATH, "//form//button").click()

    def select_and_apply_jobs(self):
        self.driver.execute_script("document.body.style.zoom='50%'")
        clicked = set()
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        attempts = 0

        while len(clicked) < 10:
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            for cb in checkboxes:
                val = cb.get_attribute("value")
                if val and val not in clicked:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cb)
                        time.sleep(0.3)
                        cb.click()
                        clicked.add(val)
                    except ElementClickInterceptedException:
                        continue

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                attempts += 1
                if attempts > 2:
                    break
            else:
                attempts = 0
                last_height = new_height

        self.driver.find_element(By.XPATH, "//button[normalize-space()='Apply All']").click()
        tabs = self.driver.window_handles
        if len(tabs) > 1:
            self.driver.switch_to.window(tabs[1])
            total_applied = self.driver.find_element(By.CSS_SELECTOR, ".job-closed")
            print(total_applied.text)

    def run(self):
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.login()
        self.search_jobs()
        self.select_and_apply_jobs()
