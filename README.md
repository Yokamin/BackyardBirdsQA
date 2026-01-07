# Backyard Birds QA

Appium test suite for the Backyard Birds iOS app.

## App

The app is Apple's sample project: https://developer.apple.com/documentation/SwiftUI/Backyard-birds-sample

Download and build it in Xcode for simulator, then place the `.app` file in the project root as `Backyard Birds.app`.

## Setup

Tested with:
- Xcode 26.2
- iPhone 17 Pro Simulator (iOS 18)
- Appium 3.1.2
- Node v25.2.1
- Python 3.14

Install dependencies (recommend using a virtual environment):
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Simulator Config

Update `config/capabilities.py` with your own simulator info:
- `deviceName` - your simulator name
- `udid` - your simulator's udid (find it with `xcrun simctl list devices`)

## Running Tests

Start Appium server first, then:
```
pytest
```

For HTML report:
```
pytest --html=reports/report.html
```

Tests run in order: Smoke (S1-S3) → Navigation (N1-N5) → Functional (F1-F12)

## Structure

```
├── config/          # Appium capabilities
├── pages/           # Page objects
├── tests/           # Test files
├── screenshots/     # Failure screenshots (auto-generated)
└── reports/         # HTML reports
```

## Notes

- Used Appium Inspector to find element locators
- Screenshots are captured automatically on test failure
- N4 and F9 are skipped (pull-to-refresh doesn't exist, couldn't simulate offline on iOS simulator)
- F12 fails intentionally to demonstrate screenshot capture
