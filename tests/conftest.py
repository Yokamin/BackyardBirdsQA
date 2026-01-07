import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions

from config.capabilities import APPIUM_SERVER, CAPABILITIES

# Store screenshots in project root
import os
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


@pytest.fixture(scope="function")
def driver():
    """
    Creates an Appium driver for each test.

    scope="function" means:
    - New driver (fresh app session) for each test
    - App resets to default state before each test
    """
    # Convert capabilities dict to XCUITestOptions
    options = XCUITestOptions()
    for key, value in CAPABILITIES.items():
        # Remove 'appium:' prefix if present for the options object
        clean_key = key.replace("appium:", "")
        options.set_capability(clean_key, value)

    # Connect to Appium and launch app
    app_driver = webdriver.Remote(APPIUM_SERVER, options=options)

    # Give driver to the test
    yield app_driver

    # After test completes, quit the driver
    app_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test.
    If a test fails, capture a screenshot.
    """
    outcome = yield
    report = outcome.get_result()

    # Only capture on actual test failure (not setup/teardown)
    if report.when == "call" and report.failed:
        # Try to get the driver from the test's fixtures
        driver = item.funcargs.get("driver")
        if driver:
            # Create screenshots folder if it doesn't exist
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

            # Save screenshot with test name
            screenshot_path = os.path.join(
                SCREENSHOTS_DIR,
                f"{item.name}_failure.png"
            )
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
