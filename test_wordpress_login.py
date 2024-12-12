import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime

class TestWordPressSetupAndLogin(unittest.TestCase):

    def setUp(self):
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        # Set up the ChromeDriver service using webdriver-manager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("http://52.60.108.120/wp-admin/setup-config.php")
        self.driver.maximize_window()

    def test_setup_and_login(self):
        driver = self.driver

        # Step 1: Language selection
        try:
            print("Waiting for language selection page to appear...")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "language"))
            )
            language = driver.find_element(By.ID, "language")
            language.find_element(By.CSS_SELECTOR, "option[value='en_US']").click()
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            print("Language selected.")
        except Exception as e:
            print("Language selection failed.")
            self.fail("Language selection page not found!")

        # Step 2: Site information and user creation
        try:
            print("Waiting for site setup page to appear...")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "weblog_title"))
            )
            driver.find_element(By.ID, "weblog_title").send_keys("wordPressTest")
            driver.find_element(By.ID, "user_login").send_keys("Jinitusinu")
            driver.find_element(By.ID, "pass1").send_keys("password@11")
            driver.find_element(By.ID, "admin_email").send_keys("georgejinitus@gmail.com")
            driver.find_element(By.ID, "submit").click()
            print("Site information and user created.")
        except Exception as e:
            print("Site setup failed.")
            self.fail("Site setup page not found!")

        # Step 3: Log in to the new WordPress site
        try:
            print("Waiting for login page to appear...")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user_login"))
            )
            driver.find_element(By.ID, "user_login").send_keys("Jinitusinu")
            driver.find_element(By.ID, "user_pass").send_keys("password@11")
            driver.find_element(By.ID, "wp-submit").click()
            print("Logged in successfully.")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "wp-admin-bar-my-account"))
            )
            print("Successfully reached the dashboard.")
        except Exception as e:
            print("Login failed.")
            self.fail("Login page not found or login failed!")

        # Write the result to the report file
        report_dir = "/home/ubuntu/test_reports"
        os.makedirs(report_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(report_dir, f"setup_and_login_test_report_{timestamp}.txt")
        with open(report_file, "w") as f:
            f.write("Test case passed: Setup and login successful.")
        print(f"Report saved at: {report_file}")

    def tearDown(self):
        # Close the browser after the test
        print("Closing the browser...")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
