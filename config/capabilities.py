import os

# Path to the app (relative to project root)
APP_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Backyard Birds.app"
)

# Appium server URL
APPIUM_SERVER = "http://127.0.0.1:4723"

CAPABILITIES = {
    # Platform settings
    "platformName": "iOS",
    "appium:automationName": "XCUITest",

    # Device settings
    "appium:deviceName": "iPhone 17 Pro",
    "appium:udid": "9E4CCD55-0747-4369-9E9B-C6C0545EA79E",

    # App settings
    "appium:app": APP_PATH,
    "appium:bundleId": "com.example.apple-samplecode.Backyard-Birds",

    # Reset behavior - start fresh each test run
    "appium:noReset": False,

    # Timeouts (in seconds)
    "appium:newCommandTimeout": 300,
}
