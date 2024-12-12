import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class TestWordPressSetup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure Chrome for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Set up ChromeDriver using webdriver-manager
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.get("http://52.60.108.120/wp-admin/install.php")
        cls.driver.maximize_window()

    def test_language_selection_and_site_setup_and_login(self):
        driver = self.driver
        print("Testing language selection, site setup, and login process...")

        # Step 1: Select Language and Click Continue
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "language"))
            )
            language_dropdown = driver.find_element(By.ID, "language")
            language_option = language_dropdown.find_element(By.XPATH, "//option[@value='en_US' and @data-installed='1']")
            print(f"Found language option: {language_option.text}")
            language_option.click()
            driver.find_element(By.ID, "language-continue").click()
            print("Language selection completed.")
        except Exception as e:
            print(f"Language selection failed: {e}")
            print(driver.page_source)  # Print the page source for debugging
            self.fail("Language selection page not found!")

        # Step 2: Fill the Site Setup Form
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "weblog_title"))
            )
            site_title = "My WordPress Site"
            username = "admin_user"
            password = "StrongPassword123!"
            email = "admin@example.com"

            driver.find_element(By.ID, "weblog_title").send_keys(site_title)
            driver.find_element(By.ID, "user_login").send_keys(username)
            driver.find_element(By.ID, "pass1").clear()
            driver.find_element(By.ID, "pass1").send_keys(password)
            driver.find_element(By.ID, "admin_email").send_keys(email)

            # (Optional) Uncheck 'Search Engine Visibility'
            search_engine_visibility = driver.find_element(By.ID, "blog_public")
            if search_engine_visibility.is_selected():
                search_engine_visibility.click()

            # Submit the form
            driver.find_element(By.ID, "submit").click()
            print("Site setup completed.")
        except Exception as e:
            print(f"Site setup failed: {e}")
            print(driver.page_source)  # Print the page source for debugging
            self.fail("Site setup page not found!")

        # Step 3: Verify Success Page and Click Login
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Log In"))
            )
            driver.find_element(By.LINK_TEXT, "Log In").click()
            print("Clicked on the 'Log In' link.")
        except Exception as e:
            print(f"Installation success page not found: {e}")
            print(driver.page_source)  # Print the page source for debugging
            self.fail("Installation success page not found!")

        # Step 4: Fill Login Form
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "user_login"))
            )
            driver.find_element(By.ID, "user_login").send_keys("admin_user")  # Use the username you set up
            driver.find_element(By.ID, "user_pass").send_keys("StrongPassword123!")  # Use the password you set up
            driver.find_element(By.ID, "wp-submit").click()
            print("Login process completed.")

            # Verify Dashboard
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "wp-admin-bar-my-account"))
            )
            print("Dashboard loaded successfully. Test passed.")
        except Exception as e:
            print(f"Login failed: {e}")
            print(driver.page_source)  # Print the page source for debugging
            self.fail("Login page not found or login failed!")

    @classmethod
    def tearDownClass(cls):
        print("Closing the browser...")
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
