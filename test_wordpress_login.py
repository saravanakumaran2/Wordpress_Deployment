import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime

class TestWordPressLogin(unittest.TestCase):

    def setUp(self):
        # Get the path of the installed ChromeDriver
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://localhost:8080/wp-login.php")
        self.driver.maximize_window()

    def test_login(self):
        driver = self.driver

        # Step 1: Check if the WordPress login page is loaded
        try:
            print("Waiting for login form to appear...")
            # Wait until the login form is visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "loginform"))
            )
            print("WordPress login page is up and running!")
        except Exception as e:
            print("WordPress login page is not accessible.")
            self.fail("WordPress login page not found!")

        # Step 2: Find the username, password fields, and the login button
        print("Locating login elements...")
        username_field = driver.find_element(By.ID, "user_login")
        password_field = driver.find_element(By.ID, "user_pass")
        login_button = driver.find_element(By.ID, "wp-submit")

        # Step 3: Provide username and password for login
        username = "Jinitusinu"  # Replace with your WordPress username
        password = "Jinitus@11"  # Replace with your WordPress password

        print("Entering username and password...")
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Step 4: Submit the login form
        print("Submitting the login form...")
        login_button.click()

        # Wait for the page to load after login (wait until a specific element is visible after login)
        try:
            print("Waiting for the dashboard link to confirm successful login...")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "wp-admin-bar-my-account"))
            )
            print("Login successful!")
            result = "Test case passed: Login successful."
        except Exception as e:
            print("Login failed!")
            result = "Test case failed: Login failed - Unable to find dashboard link."
            self.fail(result)

        # Write the result to the report file
        report_dir = "/home/ubuntu/test_reports"
        os.makedirs(report_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(report_dir, f"login_test_report_{timestamp}.txt")
        with open(report_file, "w") as f:
            f.write(result)
        print(f"Report saved at: {report_file}")

    def tearDown(self):
        # Close the browser after the test
        print("Closing the browser...")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
