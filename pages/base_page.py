"""
BasePage - Parent class for all page objects.
Contains shared utilities like tab navigation, waits, and screenshots.
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class that all page objects inherit from."""

    # Default timeout for waiting (seconds)
    DEFAULT_TIMEOUT = 10

    # Tab bar locators (tabs are always visible, so they live in BasePage)
    TAB_BACKYARDS = (AppiumBy.IOS_PREDICATE, 'label == "Backyards" AND type == "XCUIElementTypeButton"')
    TAB_BIRDS = (AppiumBy.IOS_PREDICATE, 'label == "Birds" AND type == "XCUIElementTypeButton"')
    TAB_PLANTS = (AppiumBy.IOS_PREDICATE, 'label == "Plants" AND type == "XCUIElementTypeButton"')
    TAB_ACCOUNT = (AppiumBy.IOS_PREDICATE, 'label == "Account" AND type == "XCUIElementTypeButton"')

    def __init__(self, driver):
        """
        Initialize with Appium driver.

        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver

    # ==================== Wait Utilities ====================

    def wait_for_element(self, locator, timeout=None):
        """
        Wait for an element to be visible and return it.

        Args:
            locator: Tuple of (by, value) e.g. (AppiumBy.ACCESSIBILITY_ID, "BackButton")
            timeout: Seconds to wait (uses DEFAULT_TIMEOUT if not specified)

        Returns:
            WebElement if found

        Raises:
            TimeoutException if element not found within timeout
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for an element to be clickable and return it.

        Args:
            locator: Tuple of (by, value)
            timeout: Seconds to wait

        Returns:
            WebElement if found and clickable
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_invisible(self, locator, timeout=None):
        """
        Wait for an element to disappear.

        Args:
            locator: Tuple of (by, value)
            timeout: Seconds to wait

        Returns:
            True if element disappeared, False otherwise
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def is_element_visible(self, locator, timeout=3):
        """
        Check if an element is visible (non-blocking).

        Args:
            locator: Tuple of (by, value)
            timeout: Short timeout for quick check

        Returns:
            True if visible, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    # ==================== Element Interaction ====================

    def tap(self, locator, timeout=None):
        """
        Wait for element and tap it.

        Args:
            locator: Tuple of (by, value)
            timeout: Seconds to wait
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()

    def get_text(self, locator, timeout=None):
        """
        Wait for element and get its text.

        Args:
            locator: Tuple of (by, value)
            timeout: Seconds to wait

        Returns:
            Text content of the element
        """
        element = self.wait_for_element(locator, timeout)
        # iOS uses 'label' or 'value' attribute for text
        return element.get_attribute("label") or element.get_attribute("value") or element.text

    def get_elements(self, locator, timeout=None):
        """
        Wait for at least one element and return all matching elements.

        Args:
            locator: Tuple of (by, value)
            timeout: Seconds to wait

        Returns:
            List of WebElements
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def get_element_count(self, locator, timeout=None, wait=True):
        """
        Count elements matching a locator.

        Args:
            locator: Tuple of (by, value)
            timeout: Seconds to wait (only used if wait=True)
            wait: If True, wait for at least one element. If False, return immediately.

        Returns:
            Number of elements found (0 if none)
        """
        if not wait:
            return len(self.driver.find_elements(*locator))

        try:
            elements = self.get_elements(locator, timeout)
            return len(elements)
        except TimeoutException:
            return 0

    # ==================== Tab Navigation ====================

    def tap_backyards_tab(self):
        """Navigate to the Backyards tab."""
        self.tap(self.TAB_BACKYARDS)

    def tap_birds_tab(self):
        """Navigate to the Birds tab."""
        self.tap(self.TAB_BIRDS)

    def tap_plants_tab(self):
        """Navigate to the Plants tab."""
        self.tap(self.TAB_PLANTS)

    def tap_account_tab(self):
        """Navigate to the Account tab."""
        self.tap(self.TAB_ACCOUNT)

    # ==================== Scrolling ====================

    def scroll_down(self, start_pct=0.7, end_pct=0.3):
        """
        Scroll down on the current screen.

        Args:
            start_pct: Start position as percentage of screen height (default 0.7 = 70%)
            end_pct: End position as percentage of screen height (default 0.3 = 30%)
        """
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * start_pct)
        end_y = int(size['height'] * end_pct)

        self.driver.swipe(start_x, start_y, start_x, end_y, duration=500)

    def scroll_up(self, start_pct=0.3, end_pct=0.7):
        """
        Scroll up on the current screen.

        Args:
            start_pct: Start position as percentage of screen height (default 0.3 = 30%)
            end_pct: End position as percentage of screen height (default 0.7 = 70%)
        """
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * start_pct)
        end_y = int(size['height'] * end_pct)

        self.driver.swipe(start_x, start_y, start_x, end_y, duration=500)

    def scroll_to_element(self, locator, max_scrolls=5):
        """
        Scroll down until element is visible.

        Args:
            locator: Tuple of (by, value)
            max_scrolls: Maximum scroll attempts

        Returns:
            WebElement if found

        Raises:
            TimeoutException if element not found after max_scrolls
        """
        for _ in range(max_scrolls):
            if self.is_element_visible(locator, timeout=2):
                return self.wait_for_element(locator)
            self.scroll_down()

        raise TimeoutException(f"Element {locator} not found after {max_scrolls} scrolls")

    # ==================== Screenshots ====================

    def take_screenshot(self, name):
        """
        Take a screenshot and save it.

        Args:
            name: Filename for the screenshot (without extension)

        Returns:
            Path to saved screenshot
        """
        import os
        screenshots_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)

        path = os.path.join(screenshots_dir, f"{name}.png")
        self.driver.save_screenshot(path)
        return path
