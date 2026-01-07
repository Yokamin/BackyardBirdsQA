"""
BackyardsPage - The main Backyards tab (home screen).
Contains methods for interacting with the backyard list.
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class BackyardsPage(BasePage):
    """Page object for the Backyards list (home screen)."""

    # ==================== Locators ====================

    # Page title
    TITLE = (AppiumBy.IOS_PREDICATE, 'name == "Backyards" AND type == "XCUIElementTypeStaticText"')

    # Search bar
    SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "Search")
    SEARCH_CLOSE = (AppiumBy.ACCESSIBILITY_ID, "Close")
    SEARCH_CLEAR_TEXT = (AppiumBy.ACCESSIBILITY_ID, "Clear text")

    # Search placeholders (shown when search is open but empty)
    SEARCH_PLACEHOLDERS = (
        AppiumBy.IOS_PREDICATE,
        'label CONTAINS "is currently in"'
    )

    # Backyard cells - main card buttons (excludes favorite buttons which share the name prefix)
    BACKYARD_CELLS = (
        AppiumBy.IOS_PREDICATE,
        'type == "XCUIElementTypeButton" AND name BEGINSWITH "BackyardGridItem_ZStack_" AND label != "Favorite"'
    )

    # Favorite buttons on backyard cards (in grid view)
    FAVORITE_BUTTONS = (
        AppiumBy.IOS_PREDICATE,
        'name BEGINSWITH "BackyardGridItem_ZStack_" AND label == "Favorite"'
    )

    # ==================== Page State ====================

    def is_page_loaded(self, timeout=10):
        """
        Check if the Backyards page is loaded.

        Returns:
            True if page title is visible
        """
        return self.is_element_visible(self.TITLE, timeout)

    def get_title(self):
        """Get the page title text."""
        return self.get_text(self.TITLE)

    # ==================== Backyard List ====================

    def get_backyard_count(self, wait=True):
        """
        Count the number of backyard cells visible.

        Args:
            wait: If True, wait for at least one element. If False, return immediately.

        Returns:
            Number of backyard cells
        """
        return self.get_element_count(self.BACKYARD_CELLS, wait=wait)

    def get_backyard_cells(self):
        """
        Get all backyard cell elements.

        Returns:
            List of backyard cell WebElements
        """
        return self.get_elements(self.BACKYARD_CELLS)

    def get_backyard_names(self):
        """
        Get all backyard names in display order (sorted by y-coordinate).

        Returns:
            List of backyard name strings in top-to-bottom order
        """
        # Backyard names are StaticText elements within BackyardGridItem cells
        locator = (
            AppiumBy.IOS_PREDICATE,
            'type == "XCUIElementTypeStaticText" AND name BEGINSWITH "BackyardGridItem_ZStack_"'
        )
        elements = self.get_elements(locator)

        # Get name and y-position for each, then sort by y-position
        backyards_with_position = []
        for el in elements:
            name = el.get_attribute("label")
            y_pos = el.location['y']
            backyards_with_position.append((y_pos, name))

        # Sort by y-position (top to bottom) and return just the names
        backyards_with_position.sort(key=lambda x: x[0])
        return [name for (y, name) in backyards_with_position]

    def tap_first_backyard(self):
        """Tap the first backyard in the list."""
        cells = self.get_backyard_cells()
        if cells:
            cells[0].click()

    def tap_backyard_by_name(self, name):
        """
        Tap a specific backyard by its name.

        Args:
            name: Backyard name (e.g., "Bird Springs")
        """
        locator = (
            AppiumBy.IOS_PREDICATE,
            f'type == "XCUIElementTypeStaticText" AND label == "{name}"'
        )
        self.tap(locator)

    def tap_backyard_by_index(self, index):
        """
        Tap a backyard by its position in the list.

        Args:
            index: 0-based index (0 = first backyard)
        """
        cells = self.get_backyard_cells()
        if index < len(cells):
            cells[index].click()
        else:
            raise IndexError(f"Backyard index {index} out of range. Only {len(cells)} backyards found.")

    def is_backyard_visible(self, name, timeout=3):
        """
        Check if a specific backyard is visible.

        Args:
            name: Backyard name

        Returns:
            True if visible
        """
        locator = (
            AppiumBy.IOS_PREDICATE,
            f'type == "XCUIElementTypeStaticText" AND label == "{name}"'
        )
        return self.is_element_visible(locator, timeout)

    # ==================== Favorites ====================

    def get_favorite_button_count(self):
        """Count favorite buttons visible in the list."""
        return self.get_element_count(self.FAVORITE_BUTTONS)

    def tap_first_favorite_button(self):
        """Tap the favorite button on the first backyard."""
        buttons = self.get_elements(self.FAVORITE_BUTTONS)
        if buttons:
            buttons[0].click()

    def get_first_favorite_button(self):
        """Get the first favorite button element."""
        buttons = self.get_elements(self.FAVORITE_BUTTONS)
        if buttons:
            return buttons[0]
        return None

    def get_first_favorite_screenshot(self):
        """Capture screenshot of the first favorite button."""
        button = self.get_first_favorite_button()
        if button:
            return button.screenshot_as_base64
        return None

    # ==================== Search ====================

    def tap_search_bar(self):
        """Tap the search bar to open search."""
        self.tap(self.SEARCH_BAR)

    def search_for(self, query):
        """
        Search for a backyard.

        Args:
            query: Search text
        """
        search_element = self.wait_for_element(self.SEARCH_BAR)
        search_element.click()
        search_element.send_keys(query)

    def clear_search_text(self):
        """Clear the search text but keep search view open."""
        if self.is_element_visible(self.SEARCH_CLEAR_TEXT, timeout=2):
            self.tap(self.SEARCH_CLEAR_TEXT)

    def close_search(self):
        """Close the search view entirely."""
        if self.is_element_visible(self.SEARCH_CLOSE, timeout=2):
            self.tap(self.SEARCH_CLOSE)

    def is_search_bar_visible(self, timeout=3):
        """Check if search bar is visible (it hides when scrolling)."""
        return self.is_element_visible(self.SEARCH_BAR, timeout)

    def get_placeholder_count(self, wait=True):
        """
        Count the search placeholders (e.g., "Dove is currently in Quiet Haven").

        Args:
            wait: If True, wait for at least one element. If False, return immediately.

        Returns:
            Number of placeholder elements visible
        """
        return self.get_element_count(self.SEARCH_PLACEHOLDERS, wait=wait)

    def are_placeholders_visible(self, timeout=3):
        """Check if search placeholders are visible."""
        return self.is_element_visible(self.SEARCH_PLACEHOLDERS, timeout)

    def wait_for_backyard_count(self, expected_count, timeout=5):
        """
        Wait until the backyard count equals the expected value.

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
            current = self.get_backyard_count(wait=False)
            return current == expected_count

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(count_matches)
