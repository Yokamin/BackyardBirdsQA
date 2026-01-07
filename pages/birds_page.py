"""
BirdsPage - The Birds tab.
Contains methods for the birds grid (used for S2 alternate test).
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class BirdsPage(BasePage):
    """Page object for the Birds tab."""

    # ==================== Locators ====================

    # Page title
    TITLE = (AppiumBy.IOS_PREDICATE, 'name == "Birds" AND type == "XCUIElementTypeStaticText"')

    # Search bar
    SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "Search")
    SEARCH_CLOSE = (AppiumBy.ACCESSIBILITY_ID, "Close")

    # Search suggestions (category buttons shown when search is open but empty)
    SEARCH_SUGGESTIONS = (
        AppiumBy.IOS_PREDICATE,
        'name == "BirdsNavigationStack_SearchSuggestions"'
    )

    # Clear text button in search bar
    SEARCH_CLEAR_TEXT = (AppiumBy.ACCESSIBILITY_ID, "Clear text")

    # Birds grid container
    BIRDS_GRID = (AppiumBy.ACCESSIBILITY_ID, "BirdsNavigationStack_Grid")

    # Bird name texts (each bird has a name label)
    # These have names like "BirdsNavigationStack_GridItem_<UUID>" and labels like "Hummingbird"
    BIRD_NAMES = (
        AppiumBy.IOS_PREDICATE,
        'name BEGINSWITH "BirdsNavigationStack_GridItem_" AND type == "XCUIElementTypeStaticText" '
        'AND (label == "Hummingbird" OR label == "Swallow" OR label == "Dove" '
        'OR label == "Chickadee" OR label == "Petrel" OR label == "Cardinal")'
    )

    # Alternative: All static text elements in the grid (includes names and "last seen" texts)
    BIRD_TEXT_ELEMENTS = (
        AppiumBy.IOS_PREDICATE,
        'name BEGINSWITH "BirdsNavigationStack_GridItem_" AND type == "XCUIElementTypeStaticText"'
    )

    # ==================== Page State ====================

    def is_page_loaded(self, timeout=10):
        """
        Check if the Birds page is loaded.

        Returns:
            True if page title is visible
        """
        return self.is_element_visible(self.TITLE, timeout)

    def get_title(self):
        """Get the page title text."""
        return self.get_text(self.TITLE)

    # ==================== Birds Grid ====================

    def is_grid_visible(self, timeout=10):
        """
        Check if the birds grid is visible.

        Returns:
            True if grid is visible
        """
        return self.is_element_visible(self.BIRDS_GRID, timeout)

    def get_bird_names(self):
        """
        Get all visible bird name elements.

        Returns:
            List of WebElements for bird names
        """
        return self.get_elements(self.BIRD_NAMES)

    def get_bird_count(self):
        """
        Count unique birds visible in the grid.

        Note: Each bird has multiple elements (images, name, last seen).
        This counts the name labels to get actual bird count.

        Returns:
            Number of birds visible
        """
        try:
            names = self.get_bird_names()
            return len(names)
        except:
            return 0

    def get_bird_text_count(self):
        """
        Count all text elements in birds grid.

        Each bird has 2 text elements (name + "last seen").
        So bird count = text_count / 2.

        Returns:
            Number of text elements
        """
        return self.get_element_count(self.BIRD_TEXT_ELEMENTS)

    def get_visible_bird_types(self):
        """
        Get list of bird types visible.

        Returns:
            List of bird names (e.g., ["Hummingbird", "Swallow", "Dove"])
        """
        names = self.get_bird_names()
        return [name.get_attribute("label") for name in names]

    # ==================== Search ====================

    def is_search_bar_visible(self, timeout=3):
        """Check if search bar is visible."""
        return self.is_element_visible(self.SEARCH_BAR, timeout)

    def tap_search_bar(self):
        """Tap the search bar."""
        self.tap(self.SEARCH_BAR)

    def search_for(self, query):
        """
        Search for a bird.

        Args:
            query: Search text
        """
        search_element = self.wait_for_element(self.SEARCH_BAR)
        search_element.click()
        search_element.send_keys(query)

    def get_search_value(self):
        """
        Get the current value of the search bar.

        Note: Uses specific locator to avoid matching the keyboard's "Search" button.

        Returns:
            Current search text or None if empty
        """
        search_field_locator = (
            AppiumBy.IOS_PREDICATE,
            'type == "XCUIElementTypeSearchField" AND name == "Search"'
        )
        search_element = self.wait_for_element(search_field_locator)
        return search_element.get_attribute("value")

    def wait_for_search_value(self, expected_value, timeout=5):
        """
        Wait for the search bar to contain the expected value.

        Args:
            expected_value: The value to wait for
            timeout: Seconds to wait

        Returns:
            True if value matches

        Raises:
            TimeoutException if value doesn't match within timeout
        """
        from selenium.webdriver.support.ui import WebDriverWait

        def value_matches(driver):
            return self.get_search_value() == expected_value

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(value_matches)

    def clear_search_text(self):
        """Clear the search text but keep search view open."""
        if self.is_element_visible(self.SEARCH_CLEAR_TEXT, timeout=2):
            self.tap(self.SEARCH_CLEAR_TEXT)

    def close_search(self):
        """Close the search view entirely."""
        if self.is_element_visible(self.SEARCH_CLOSE, timeout=2):
            self.tap(self.SEARCH_CLOSE)

    # ==================== Search Suggestions ====================

    def are_suggestions_visible(self, timeout=3):
        """Check if search suggestions are visible."""
        return self.is_element_visible(self.SEARCH_SUGGESTIONS, timeout)

    def get_suggestion_count(self, wait=True):
        """
        Count the search suggestions (category buttons).

        Args:
            wait: If True, wait for at least one element.

        Returns:
            Number of suggestion buttons visible
        """
        return self.get_element_count(self.SEARCH_SUGGESTIONS, wait=wait)

    def tap_suggestion(self, bird_type):
        """
        Tap a search suggestion by its label (bird type).

        Args:
            bird_type: Bird type name (e.g., "Dove", "Cardinal")
        """
        locator = (
            AppiumBy.IOS_PREDICATE,
            f'name == "BirdsNavigationStack_SearchSuggestions" AND label == "{bird_type}"'
        )
        self.tap(locator)

    def wait_for_bird_count(self, expected_count, timeout=5):
        """
        Wait until the bird count equals the expected value.

        Args:
            expected_count: The count to wait for
            timeout: Seconds to wait

        Returns:
            True if count reached expected value

        Raises:
            TimeoutException if count doesn't match within timeout
        """
        from selenium.webdriver.support.ui import WebDriverWait

        def count_matches(driver):
            current = self.get_bird_count()
            return current == expected_count

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(count_matches)
