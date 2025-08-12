import time
import logging
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC



class InstahyreBot:
    def __init__(self, email, password, skills, yoe, locations, search_mode, job_functions_roles = ""):
        self.email = email
        self.password = password
        self.skills = skills
        self.yoe = yoe
        self.locations = locations
        self.search_mode = search_mode
        self.job_functions_roles = job_functions_roles

        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=chrome_options)


    def login(self):
        self.driver.get("https://www.instahyre.com/")
        self.driver.find_element(By.ID, "nav-user-login").click()
        self.driver.execute_script("window.scrollTo(0,500)")
        self.driver.find_element(By.ID, "email").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']"))
        ).click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "nav-candidates-logout")))
        except Exception as e:
            logging.info(f"Log in failed due to {e}")
            raise Exception("Login failed: possibly invalid credentials or network error")
        logging.info("Logged in sucessfully on Instahyre...")
        time.sleep(3)

    def search_jobs(self):
        try:
            # Wait for the element to be present
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "i.fa.ng-scope"))
            )
            # Get the class attribute
            time.sleep(3)
            class_value = element.get_attribute("class").strip()

            # Check if it contains 'fa-angle-down'
            # logging.info(f"this is the required class value: {class_value}")
            time.sleep(2)
            if "fa-angle-down" in class_value:
                logging.info("Detected 'fa-angle-down'. Clicking to expand.")
                element.click()
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "skills-selectized"))
                )
            # else:
            #     logging.info("Element already in 'up' state. No action taken.")

        except Exception as e:
            logging.info(f"Error: {e}")

        skills_elem = self.driver.find_element(By.ID, "skills-selectized")
        yoe_elem = self.driver.find_element(By.ID, "years")
        show_elem = self.driver.find_element(By.ID, "show-results")
        loc_elem = self.driver.find_element(By.ID, "locations-selectized")
        job_func_elem = self.driver.find_element(By.ID, "job-functions-selectized")

        for skill in self.skills:
            skills_elem.send_keys(skill.strip())

            # Waiting for dropdown to appear
            # skills_elem.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "selectize-dropdown"))
            )

            # Selecting the first suggestion
            skills_elem.send_keys(Keys.ARROW_DOWN)
            skills_elem.send_keys(Keys.ENTER)
            time.sleep(0.5)

        yoe_elem.send_keys(str(self.yoe))
        if self.locations[0] != "ALL":
            for loc in self.locations:
                loc_elem.send_keys(loc.strip())
                loc_elem.send_keys(Keys.ENTER)
        if self.job_functions_roles:
            job_func_elem.send_keys(self.job_functions_roles)
            job_func_elem.send_keys(Keys.ENTER)
        time.sleep(5) #Just to check the details in the UI
        show_elem.send_keys(Keys.SPACE)


    def apply_jobs(self):
        if not self.search_mode:
            logging.info("Applying to recomended job(s) only...")
        total_jobs = self.driver.find_element(By.XPATH, "//div[@class='page-heading text-center']//p[1]")
        logging.info(total_jobs.text)
        if "No matching" in total_jobs.text:
            logging.info("Quitting this automation run as there are no specified jobs for the given specifications")
            return
        total_applied = 0
        delay_between_applies = 3
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "interested-btn"))
        ).click()

        while True:
            try:
                apply_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply')]"))
                )
                apply_btn.click()
                time.sleep(delay_between_applies)  # wait to simulate human interaction
                try:
                    popup_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply') and contains(@class, 'btn-success')]"))
                    )
                    popup_btn.click()
                except:
                    pass
                total_applied += 1
                logging.info(f"Applied to {total_applied} job(s) upto now.")
            except NoSuchElementException:
                logging.info("No more jobs available. Stopping loop.")
                break
            except Exception as e:
                logging.info(f"Unexpected error: {e}")
                break
        logging.info(f"Applied to a total of {total_applied} {self.skills} jobs in this run")

    def run(self):
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.login()
        if self.search_mode:
            self.search_jobs()
        time.sleep(3)
        self.apply_jobs()
