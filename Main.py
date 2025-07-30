from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException
import time
import sys

def setup_chrome_driver():
    """Setup Chrome driver with optimized options for macOS"""
    chrome_options = Options()
    
    # Basic stability options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    
    # Performance optimizations
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-accelerated-video-decode")
    chrome_options.add_argument("--disable-accelerated-2d-canvas")
    
    # Additional stability options
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    
    # Automation detection prevention
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Window settings
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # User agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
    
    try:
        # Try to use the specific ChromeDriver path
        driver_path = "/usr/local/bin/chromedriver"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        print(f"Failed to initialize Chrome driver with specific path: {e}")
        try:
            # Fallback: let Selenium find ChromeDriver automatically
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e2:
            print(f"Failed to initialize Chrome driver automatically: {e2}")
            raise

def wait_for_page_load(driver, wait, timeout=10):
    """Wait for page to be fully loaded"""
    try:
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        return True
    except TimeoutException:
        print("Page load timeout")
        return False

def find_and_click_element(driver, wait, selectors, description):
    """Find an element and click it immediately"""
    for selector_type, selector_value in selectors:
        try:
            element = wait.until(EC.element_to_be_clickable((selector_type, selector_value)))
            element.click()
            return True
        except (TimeoutException, InvalidSessionIdException) as e:
            if isinstance(e, InvalidSessionIdException):
                raise e
            continue
    return False

def find_element_with_multiple_selectors(driver, wait, selectors, description):
    """Try multiple selectors to find an element"""
    for selector_type, selector_value in selectors:
        try:
            element = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
            return element
        except (TimeoutException, InvalidSessionIdException) as e:
            if isinstance(e, InvalidSessionIdException):
                raise e
            continue
    raise NoSuchElementException(f"Could not find {description} with any of the provided selectors")

def pause_video_with_space(driver):
    """Pause/continue video using SPACE key"""
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.SPACE).perform()
        return True
    except Exception as e:
        print(f"Error sending SPACE key: {e}")
        return False

def wait_for_video_state_change(driver, wait, timeout=5):
    """Wait for video state to change (play/pause)"""
    try:
        # Wait a short time for video state to change
        time.sleep(1)  # Minimal sleep for video state change
        return True
    except Exception as e:
        print(f"Error waiting for video state change: {e}")
        return False

def part1_sign_in(driver, wait):
    """Part 1: Sign in to the Platform"""
    print("PART 1: SIGN IN TO THE PLATFORM")
    
    driver.get("https://indeedemo-fyc.watch.indee.tv/")
    
    # Wait for page to load completely
    wait_for_page_load(driver, wait)
    
    # Find and fill PIN input
    pin_selectors = [
        (By.ID, "pin"),
        (By.NAME, "Pin"),
        (By.NAME, "pin"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]
    
    pin_input = find_element_with_multiple_selectors(driver, wait, pin_selectors, "PIN input field")
    pin_input.clear()
    pin_input.send_keys("WVMVHWBS")
    
    # Wait for input to be processed
    wait.until(lambda driver: pin_input.get_attribute("value") == "WVMVHWBS")
    
    # Try to click submit button
    submit_selectors = [
        (By.CSS_SELECTOR, "button.wds-bg-blue-primary"),
        (By.XPATH, "//button[contains(text(),'SIGN IN')]"),
        (By.XPATH, "//button[contains(text(),'Sign In')]"),
        (By.XPATH, "//button[contains(text(),'Submit')]"),
        (By.XPATH, "//button[contains(text(),'Login')]"),
    ]
    
    if find_and_click_element(driver, wait, submit_selectors, "submit button"):
        print("Login button clicked")
        # Wait for navigation after login
        wait.until(lambda driver: "login" not in driver.current_url.lower() or 
                  EC.presence_of_element_located((By.CSS_SELECTOR, ".brand-card")))
        print("Login successful")
    else:
        print("Could not find or click submit button")
        return False
    
    return True

def part2_navigate_to_project(driver, wait):
    """Part 2: Navigate to the 'Test Automation Project'"""
    print("PART 2: NAVIGATE TO THE 'TEST AUTOMATION PROJECT'")
    
    # Wait for brand cards to be present
    brand_selectors = [
        (By.CSS_SELECTOR, ".brand-card"),
        (By.XPATH, "//button[contains(@class, 'brand-card')]"),
        (By.XPATH, "//div[contains(@class, 'brand-card')]"),
        (By.XPATH, "//*[contains(@class, 'brand-card')]"),
    ]
    
    if find_and_click_element(driver, wait, brand_selectors, "first brand card"):
        print("Brand card clicked")
        # Wait for project page to load
        wait_for_page_load(driver, wait)
    else:
        print("Could not find brand card")
        return False

    # Look for "Test automation project" with explicit wait
    project_selectors = [
        (By.XPATH, "//*[contains(text(), 'Test automation project')]"),
        (By.XPATH, "//div[contains(text(), 'Test automation project')]"),
        (By.XPATH, "//div[contains(text(), 'automation')]"),
        (By.XPATH, "//div[contains(text(), 'test')]"),
        (By.CSS_SELECTOR, "[class*='project']"),
        (By.XPATH, "//div[contains(@class, 'project')]"),
        (By.XPATH, "//a[contains(text(), 'Test')]"),
        (By.XPATH, "//a[contains(text(), 'automation')]"),
        (By.XPATH, "//button[contains(text(), 'Test')]"),
        (By.XPATH, "//button[contains(text(), 'automation')]"),
    ]
    
    if find_and_click_element(driver, wait, project_selectors, "test automation project"):
        print("Test automation project clicked")
        # Wait for video page to load
        wait_for_page_load(driver, wait)
    else:
        print("Could not find test automation project")
        return False

    return True

def part3_play_video(driver, wait):
    """Part 3: Play the Video"""
    print("PART 3: PLAY THE VIDEO")
    
    # Save the current URL before going to video page
    projects_url = driver.current_url
    
    # Wait for video player elements to be present
    play_selectors = [
        (By.CSS_SELECTOR, "#vid-01j912gbvdnr5er79gqeb8k30w > div > div.play-section.wds-mb-2.wds-flex.wds-items-center.wds-justify-between.wds-gap-x-2 > button:nth-child(1) > svg"),
        (By.XPATH, "//*[@id='vid-01j912gbvdnr5er79gqeb8k30w']/div/div[1]/button[1]/svg"),
        (By.XPATH, "//*[@id='vid-01j912gbvdnr5er79gqeb8k30w']//button[1]"),
        (By.CSS_SELECTOR, "#vid-01j912gbvdnr5er79gqeb8k30w button"),
        (By.CLASS_NAME, "vjs-big-play-button"),
        (By.CSS_SELECTOR, ".vjs-big-play-button"),
        (By.XPATH, "//button[contains(@class, 'play')]"),
        (By.XPATH, "//div[contains(@class, 'play')]"),
        (By.XPATH, "//*[contains(@class, 'play')]"),
    ]
    
    if find_and_click_element(driver, wait, play_selectors, "play button"):
        print("Video play button clicked")
        wait_for_video_state_change(driver, wait)
    else:
        print("Could not find play button")
        return False, None
    
    # Play video for 10 seconds with dynamic wait
    print("Playing video for 10 seconds...")
    video_play_wait = WebDriverWait(driver, 15)
    
    # Wait for 10 seconds while monitoring if page is still active
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            # Check if we're still on the video page
            current_url = driver.current_url
            if "video" in current_url or "watch" in current_url or projects_url != current_url:
                time.sleep(0.5)  # Small incremental sleep
            else:
                break
        except InvalidSessionIdException:
            raise
        except Exception:
            break
    
    print("Video played for 10+ seconds")
    return True, projects_url

def part4_replay_video(driver, wait):
    """Part 4: Replay the Video (Pause, Resume, Pause cycle)"""
    print("PART 4: REPLAY THE VIDEO")
    
    print("Pausing video...")
    if pause_video_with_space(driver):
        wait_for_video_state_change(driver, wait)
        print("Video paused")
    
    # Wait 5 seconds while video is paused
    print("Waiting 5 seconds while video is paused...")
    pause_wait = WebDriverWait(driver, 6)
    try:
        # Use a condition that will timeout after 5 seconds
        pause_wait.until(lambda driver: False)  # This will always timeout after 5 seconds
    except TimeoutException:
        pass  # Expected timeout after 5 seconds
    
    # Resume video
    print("Resuming video...")
    if pause_video_with_space(driver):
        wait_for_video_state_change(driver, wait)
        print("Video resumed")

    # Play for 5 seconds
    print("Playing video for 5 seconds...")
    play_wait = WebDriverWait(driver, 6)
    try:
        play_wait.until(lambda driver: False)  # This will timeout after 5 seconds
    except TimeoutException:
        pass
    
    # Pause again
    print("Pausing video again...")
    if pause_video_with_space(driver):
        wait_for_video_state_change(driver, wait)
        print("Video paused again")
    
    print("Video replay cycle finished")
    return True

def part5_pause_and_exit(driver, wait, projects_url):
    """Part 5: Pause and Exit (Navigate back to projects)"""
    print("PART 5: PAUSE AND EXIT")
    
    # Navigate back to projects page using saved URL
    print("Navigating back to projects page...")
    try:
        driver.get(projects_url)
        # Wait for projects page to load
        wait_for_page_load(driver, wait)
        
        # Wait for project elements to be visible
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'project') or contains(text(), 'Project')]")))
        print("Successfully navigated back to projects page")
    except Exception as e:
        print(f"Error navigating back: {e}")
        return False

    return True

def part6_logout(driver, wait):
    """Part 6: Logout from the platform"""
    print("PART 6: LOGOUT")
    
    # Look for logout button
    logout_selectors = [
        (By.XPATH, "//*[@id='signOutSideBar']/svg"),
        (By.CSS_SELECTOR, "#signOutSideBar > svg"),
        (By.CSS_SELECTOR, "#signOutSideBar"),
        (By.XPATH, "//button[contains(text(), 'Logout')]"),
        (By.XPATH, "//*[contains(text(), 'Logout')]"),
        (By.XPATH, "//button[contains(text(), 'Sign Out')]"),
        (By.CSS_SELECTOR, "[class*='logout']"),
    ]
    
    if find_and_click_element(driver, wait, logout_selectors, "logout button"):
        print("Logout button clicked")
        
        # Wait for redirect to login page
        print("Waiting for redirect to login page...")
        try:
            # Wait for URL to change or login elements to appear
            wait.until(lambda driver: "login" in driver.current_url.lower() or 
                      EC.presence_of_element_located((By.ID, "pin")))
            print("Successfully redirected to login page")
        except TimeoutException:
            print("Timeout waiting for redirect, navigating manually...")
            driver.get("https://indeedemo-fyc.watch.indee.tv/")
            wait_for_page_load(driver, wait)
            
    else:
        print("Could not find logout button")
        return False
    
    # Wait on login page before closing (using WebDriverWait for consistency)
    print("Waiting 5 seconds on login page before closing...")
    final_wait = WebDriverWait(driver, 6)
    try:
        final_wait.until(lambda driver: False)  # Timeout after 5 seconds
    except TimeoutException:
        pass
    
    print("Successfully logged out")
    return True

def main():
    driver = None
    try:
        print("Starting Indee TV Automation...")
        
        # Initialize driver
        driver = setup_chrome_driver()
        wait = WebDriverWait(driver, 15)
        
        print("Chrome driver initialized successfully")
        
        # Execute all 6 parts in sequence
        projects_url = None
        
        # Part 1: Sign in to the Platform
        if not part1_sign_in(driver, wait):
            print("Part 1 failed - stopping execution")
            return
            
        # Part 2: Navigate to the 'Test Automation Project'
        if not part2_navigate_to_project(driver, wait):
            print("Part 2 failed - stopping execution")
            return
            
        # Part 3: Play the Video
        success, projects_url = part3_play_video(driver, wait)
        if not success:
            print("Part 3 failed - stopping execution")
            return
            
        # Part 4: Replay the Video
        if not part4_replay_video(driver, wait):
            print("Part 4 failed - stopping execution")
            return
            
        # Part 5: Pause and Exit
        if not part5_pause_and_exit(driver, wait, projects_url):
            print("Part 5 failed - stopping execution")
            return
            
        # Part 6: Logout
        if not part6_logout(driver, wait):
            print("Part 6 failed - stopping execution")
            return
        
        print("ALL 6 PARTS COMPLETED SUCCESSFULLY!")
        print("AUTOMATION SUMMARY:")
        print("1. Signed in to the platform")
        print("2. Navigated to 'Test Automation Project'")
        print("3. Played video for 10 seconds")
        print("4. Executed replay cycle (pause/resume/pause)")
        print("5. Exited video and returned to projects")
        print("6. Logged out successfully")

    except InvalidSessionIdException as e:
        print(f"Browser session lost: {e}")
        print("This usually happens when the browser closes unexpectedly.")
    except Exception as e:
        print(f"ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        if driver:
            try:
                print("Current URL:", driver.current_url)
                print("Page title:", driver.title)
            except InvalidSessionIdException:
                print("Cannot get page info - browser session lost")

    finally:
        if driver:
            try:
                print("Cleaning up...")
                # Small delay for cleanup
                cleanup_wait = WebDriverWait(driver, 3)
                try:
                    cleanup_wait.until(lambda driver: False)
                except TimeoutException:
                    pass
                driver.quit()
                print("Driver closed")
            except Exception as e:
                print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    main()
