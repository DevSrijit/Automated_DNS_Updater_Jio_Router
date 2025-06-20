from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from os import getenv
from time import sleep
from ipaddress import ip_address
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/dns_updater.log') if os.path.exists('/app/logs') else logging.StreamHandler(),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()


# Variables
url = getenv("router_url")
username = getenv("user_name")
password = getenv("password")
ipv4_dns_server1 = getenv("ipv4_dns_server1")
ipv4_dns_server2 = getenv("ipv4_dns_server2")
ipv6_dns_server1 = getenv("ipv6_dns_server1")
ipv6_dns_server2 = getenv("ipv6_dns_server2")
update_interval_time = int(getenv("update_interval_time"))


def display_settings():
    logger.info("Router IP: %s", url)
    logger.info("Username: %s", username)
    logger.info("IPv4 DNS Server 1: %s", ipv4_dns_server1)
    logger.info("IPv4 DNS Server 2: %s", ipv4_dns_server2)
    logger.info("IPv6 DNS Server 1: %s", ipv6_dns_server1)
    logger.info("IPv6 DNS Server 2: %s", ipv6_dns_server2)
    logger.info("Update interval: %s seconds (%.2f hours)", update_interval_time, update_interval_time / 3600)


def check_DNS_IPs():
    try:
        ip_address(ipv4_dns_server1)
        ip_address(ipv4_dns_server2)
        ip_address(ipv6_dns_server1)
        ip_address(ipv6_dns_server2)
        logger.info("DNS IPs are in valid format")
        return True
    except Exception as e:
        logger.error("DNS servers IP's not valid: %s", e)
        exit()


def create_web_driver():
    try:
        logger.info("Creating Webdriver")
        # Create a Chrome/Chromium WebDriver instance optimized for container
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--memory-pressure-off")
        options.add_argument("--max_old_space_size=4096")
        
        # Try Chromium first (better for ARM), fallback to Chrome
        try:
            options.binary_location = "/usr/bin/chromium-browser"
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except:
            logger.info("Chromium not found, trying Chrome...")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        logger.info("Webdriver created successfully")
        return driver
    except Exception as e:
        logger.error("Failed to create web driver: %s", e)
        exit()


def login_jio_router(driver):
    try:
        logger.info("Logging into router...")
        driver.get(url)
        username_field = driver.find_element("xpath", '//input[@name="users.username"]')
        password_field = driver.find_element("xpath", '//input[@name="users.password"]')
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Find the login button and click it
        login_button = driver.find_element("xpath", '//button[@class="loginBtn"]')
        login_button.click()
        logger.info("Login successful")
        return driver
    except Exception as e:
        logger.error("Failed to login: %s", e)
        exit()


def open_lan_setting_page(driver):
    try:
        logger.info("Opening LAN setting page...")
        lan_setting = driver.find_element("xpath", '//a[@id="tf1_network_lanIPv4Config"]')
        driver.execute_script("arguments[0].click();", lan_setting)
        logger.info("LAN setting page opened successfully")
        return driver
    except Exception as e:
        logger.error("Failed to open LAN setting page: %s", e)
        exit()


def change_ipv4_dns_setting(driver):
    try:
        logger.info("Changing IPv4 DNS settings...")
        # Select Dropdown
        ipv4_dns_dropdown = driver.find_element("xpath", '//select[@id="tf1_DnsSvrs"]')
        select = Select(ipv4_dns_dropdown)
        select.select_by_value("3")

        ipv4_dns_1 = driver.find_element("xpath", '//input[@id="tf1_priDnsServer"]')
        ipv4_dns_2 = driver.find_element("xpath", '//input[@id="tf1_secDnsServer"]')

        ipv4_dns_1.clear()
        ipv4_dns_2.clear()
        ipv4_dns_1.send_keys(ipv4_dns_server1)
        ipv4_dns_2.send_keys(ipv4_dns_server2)

        save_ipv4 = driver.find_element("xpath", '//input[@name="button.config.lanIPv4Config.lanIPv4Config.-1"]')
        driver.execute_script("arguments[0].click();", save_ipv4)
        logger.info("IPv4 DNS settings changed successfully")
        return driver

    except Exception as e:
        logger.error("Failed to change IPv4 DNS settings: %s", e)
        exit()


def change_ipv6_dns_setting(driver):
    try:
        logger.info("Changing IPv6 DNS settings...")

        # find IPv6 Setting page
        ipv6_dns_setting = driver.find_element("xpath", '//a[contains(text(), "LAN IPv6 Configuration")]')
        driver.execute_script("arguments[0].click();", ipv6_dns_setting)

        ipv6_dns_dropdown = driver.find_element("xpath", '//select[@id="tf1_DnsSvrs"]')
        select = Select(ipv6_dns_dropdown)
        select.select_by_value("3")
        ipv6_dns_1 = driver.find_element("xpath", '//input[@id="tf1_ipv6_PriDnsServer"]')
        ipv6_dns_2 = driver.find_element("xpath", '//input[@id="tf1_ipv6_SecDnsServer"]')

        ipv6_dns_1.clear()
        ipv6_dns_2.clear()
        ipv6_dns_1.send_keys(ipv6_dns_server1)
        ipv6_dns_2.send_keys(ipv6_dns_server2)

        save_ipv6 = driver.find_element("xpath", '//input[@name="button.ipv6Config.lanIPv6Config.lanIPv6Config"]')
        driver.execute_script("arguments[0].click();", save_ipv6)
        logger.info("IPv6 DNS settings changed successfully")
        return driver

    except Exception as e:
        logger.error("Failed to change IPv6 DNS settings: %s", e)
        exit()


def logout(driver):
    try:
        logger.info("Logging out...")
        logout_url = f"{url}/platform.cgi?page=index.html"
        driver.get(logout_url)
        logger.info("Logout successful")
        return driver
    except Exception as e:
        logger.error("Failed to log out: %s", e)
        exit()


def create_health_file():
    """Create a health check file for Docker health checks"""
    try:
        with open('/tmp/dns_updater_healthy', 'w') as f:
            f.write(str(datetime.now()))
    except:
        pass  # Ignore if we can't create the file


def main():
    logger.info("Starting DNS Updater Service")
    
    while True:
        try:
            if url and username and password and ipv4_dns_server1 and ipv4_dns_server2 and ipv6_dns_server1 and ipv6_dns_server2 and update_interval_time:
                logger.info("=== Starting DNS Update Cycle ===")
                display_settings()
                check_DNS_IPs()
                
                driver = None
                try:
                    driver = create_web_driver()
                    driver = login_jio_router(driver)
                    driver = open_lan_setting_page(driver)
                    driver = change_ipv4_dns_setting(driver)
                    driver = change_ipv6_dns_setting(driver)
                    driver = logout(driver)
                    
                    logger.info("=== DNS Update Completed Successfully ===")
                    create_health_file()
                    
                except Exception as e:
                    logger.error("Error during DNS update process: %s", e)
                finally:
                    if driver:
                        try:
                            driver.quit()
                        except:
                            pass
                
                next_run = datetime.now().timestamp() + update_interval_time
                next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
                logger.info("Sleeping for %s seconds (%.2f hours). Next run at: %s", 
                           update_interval_time, update_interval_time / 3600, next_run_time)
                sleep(update_interval_time)
            else:
                logger.error("Missing required environment variables")
                logger.error("Required: router_url, user_name, password, ipv4_dns_server1, ipv4_dns_server2, ipv6_dns_server1, ipv6_dns_server2, update_interval_time")
                exit(1)
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal, exiting gracefully...")
            break
        except Exception as e:
            logger.error("Unexpected error in main loop: %s", e)
            logger.info("Retrying in 60 seconds...")
            sleep(60)


if __name__ == "__main__":
    main()
