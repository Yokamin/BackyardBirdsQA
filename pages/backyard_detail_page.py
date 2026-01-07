"""
BackyardDetailPage - Inside a specific backyard.
Contains methods for favorite, back button, food/water, birds list, etc.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class BackyardDetailPage(BasePage):
    """Page object for the backyard detail view."""

    # ==================== Locators ====================

    # Navigation
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "BackButton")
    FAVORITE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Favorite")

    # Show More/Less for birds list
    SHOW_MORE_BUTTON = (AppiumBy.IOS_PREDICATE, 'name == "Show More"')
    SHOW_LESS_BUTTON = (AppiumBy.IOS_PREDICATE, 'name == "Show Less"')

    # Food and Water buttons (using stable part of the dynamic names)
    FOOD_BUTTON = (AppiumBy.IOS_PREDICATE, 'name CONTAINS "Choose Food"')
    WATER_BUTTON = (AppiumBy.IOS_PREDICATE, 'name CONTAINS "Refill Water"')

    # Food popup
    FOOD_POPUP_DONE = (AppiumBy.IOS_PREDICATE, 'name == "BirdFoodPicker_DoneButton"')
    FOOD_POPUP_TITLE = (AppiumBy.IOS_PREDICATE, 'name == "Bird Food" AND type == "XCUIElementTypeStaticText"')
    FOOD_POPUP_SHOP = (AppiumBy.ACCESSIBILITY_ID, "BirdFoodPicker_ShopLinkButton")

    # Food Shop screen (opened from food popup)
    FOOD_SHOP_BACK = (AppiumBy.IOS_PREDICATE, 'name == "BackButton" AND label == "Bird Food"')

    # ==================== Navigation ====================

    def tap_back(self):
        """Tap back button to return to backyard list."""
        self.tap(self.BACK_BUTTON)

    def is_back_button_visible(self, timeout=10):
        """Check if back button is visible (indicates we're in detail view)."""
        return self.is_element_visible(self.BACK_BUTTON, timeout)

    # ==================== Favorite ====================

    def tap_favorite(self):
        """Toggle the favorite button."""
        self.tap(self.FAVORITE_BUTTON)

    def is_favorite_button_visible(self, timeout=5):
        """Check if favorite button is visible."""
        return self.is_element_visible(self.FAVORITE_BUTTON, timeout)

    def get_favorite_button(self):
        """
        Get the favorite button element.

        Returns:
            WebElement for the favorite button
        """
        return self.wait_for_element(self.FAVORITE_BUTTON)

    def get_favorite_screenshot(self):
        """
        Capture a screenshot of just the favorite button.

        Used for visual comparison since the app does not expose
        favorite state through element attributes.

        Returns:
            Base64 encoded screenshot string
        """
        fav_button = self.get_favorite_button()
        return fav_button.screenshot_as_base64

    # ==================== Title ====================

    def get_title(self, expected_name=None):
        """
        Get the backyard title.

        Args:
            expected_name: If provided, look for this specific name

        Returns:
            Title text
        """
        if expected_name:
            locator = (
                AppiumBy.IOS_PREDICATE,
                f'label == "{expected_name}" AND type == "XCUIElementTypeStaticText"'
            )
        else:
            # This is trickier without knowing the name - may need to use hierarchy
            # For now, we'll rely on expected_name being passed
            raise ValueError("expected_name must be provided to get title")

        return self.get_text(locator)

    def is_title_visible(self, name, timeout=5):
        """
        Check if a specific title is visible.

        Args:
            name: Expected backyard name

        Returns:
            True if title is visible
        """
        locator = (
            AppiumBy.IOS_PREDICATE,
            f'label == "{name}" AND type == "XCUIElementTypeStaticText"'
        )
        return self.is_element_visible(locator, timeout)

    # ==================== Birds List (Recent Visitors) ====================

    def tap_show_more(self):
        """Tap Show More to expand birds list."""
        self.scroll_to_element(self.SHOW_MORE_BUTTON)
        self.tap(self.SHOW_MORE_BUTTON)

    def tap_show_less(self):
        """Tap Show Less to collapse birds list."""
        self.scroll_to_element(self.SHOW_LESS_BUTTON)
        self.tap(self.SHOW_LESS_BUTTON)

    def is_show_more_visible(self, timeout=3):
        """Check if Show More button is visible."""
        return self.is_element_visible(self.SHOW_MORE_BUTTON, timeout)

    def is_show_less_visible(self, timeout=3):
        """Check if Show Less button is visible."""
        return self.is_element_visible(self.SHOW_LESS_BUTTON, timeout)

    # ==================== Food ====================

    def tap_food_button(self):
        """Tap the food button to open food picker."""
        self.tap(self.FOOD_BUTTON)

    def is_food_button_visible(self, timeout=5):
        """Check if food button is visible."""
        return self.is_element_visible(self.FOOD_BUTTON, timeout)

    def is_food_popup_visible(self, timeout=5):
        """Check if food picker popup is open."""
        return self.is_element_visible(self.FOOD_POPUP_TITLE, timeout)

    def tap_food_popup_done(self):
        """Tap Done to close food picker popup."""
        self.tap(self.FOOD_POPUP_DONE)

    def tap_food_popup_shop(self):
        """Tap Bird Food Shop link in food popup."""
        self.tap(self.FOOD_POPUP_SHOP)

    def is_food_shop_visible(self, timeout=5):
        """Check if food shop screen is visible (back button shows 'Bird Food')."""
        return self.is_element_visible(self.FOOD_SHOP_BACK, timeout)

    def tap_food_shop_back(self):
        """Tap back from food shop to return to food popup."""
        self.tap(self.FOOD_SHOP_BACK)

    # ==================== Water ====================

    def tap_water_button(self):
        """Tap the water button to refill water."""
        self.tap(self.WATER_BUTTON)

    def is_water_button_visible(self, timeout=5):
        """Check if water button is visible."""
        return self.is_element_visible(self.WATER_BUTTON, timeout)

    # ==================== Page State ====================

    def is_page_loaded(self, timeout=10):
        """
        Check if backyard detail page is loaded.

        Returns:
            True if back button and favorite button are visible
        """
        return (
            self.is_back_button_visible(timeout) and
            self.is_favorite_button_visible(timeout)
        )

    def is_detail_content_visible(self, timeout=5):
        """
        Check if main detail content is visible (food/water buttons).

        Returns:
            True if food and water buttons are visible
        """
        return (
            self.is_food_button_visible(timeout) and
            self.is_water_button_visible(timeout)
        )
