"""
Smoke Tests (S1-S3)
Basic tests to verify the app launches and core elements are present.
"""
import pytest
from pages.backyards_page import BackyardsPage
from pages.birds_page import BirdsPage


@pytest.mark.smoke
class TestSmoke:
    """Smoke tests for basic app functionality."""

    def test_s1_app_launches(self, driver):
        """
        S1 — App launch

        Steps: Launch the app.
        Asserts: Home/landing element visible within 10s; no crash.
        """
        import time

        start_time = time.time()

        backyards_page = BackyardsPage(driver)

        # Verify the home/landing page loads
        assert backyards_page.is_page_loaded(), "App did not launch - home element not visible"

        # Calculate launch time
        launch_time = time.time() - start_time

        # Assert it was within 10 seconds
        assert launch_time <= 10, f"App took {launch_time:.2f}s to launch (max 10s)"

        # Print the actual time for visibility in test output
        print(f"\nApp launched in {launch_time:.2f} seconds")

    def test_s2_list_renders(self, driver):
        """
        S2 — List renders

        Steps: Wait for birds list to load.
        Asserts: ≥1 cells present; no error/placeholder banners.

        Note: Ambiguous test case, could be birds within a Backyard too.
        Error check uses common error text patterns since no actual error states observed.
        """
        backyards_page = BackyardsPage(driver)
        birds_page = BirdsPage(driver)

        # Navigate to Birds tab
        assert backyards_page.is_page_loaded(), "Home page not loaded"
        backyards_page.tap_birds_tab()

        # Wait for birds list to load
        assert birds_page.is_page_loaded(), "Birds page did not load"
        assert birds_page.is_grid_visible(), "Birds grid not visible"

        # Assert ≥1 cells present
        bird_count = birds_page.get_bird_count()
        assert bird_count >= 1, f"Expected ≥1 bird cells, found {bird_count}"

        # Verify no error/placeholder banners
        from appium.webdriver.common.appiumby import AppiumBy
        error_patterns = ["Error", "Failed", "Unable to load", "No data", "Something went wrong"]
        for pattern in error_patterns:
            error_locator = (
                AppiumBy.IOS_PREDICATE,
                f'label CONTAINS[c] "{pattern}" AND visible == true'
            )
            assert not birds_page.is_element_visible(error_locator, timeout=1), \
                f"Error banner found containing: '{pattern}'"

        print(f"\n✓ Birds list loaded with {bird_count} bird(s) visible")
        print(f"✓ No error/placeholder banners detected")

    def test_s3_basic_accessibility(self, driver):
        """
        S3 — Basic accessibility

        Steps: Inspect home title and first cell.
        Asserts: Locatable by accessibility id (or stable fallback).
        """
        from appium.webdriver.common.appiumby import AppiumBy

        backyards_page = BackyardsPage(driver)
        assert backyards_page.is_page_loaded(), "Home page not loaded"

        # Step 1: Inspect home title - locatable by accessibility ID
        title_locator = (AppiumBy.ACCESSIBILITY_ID, "Backyards")
        title_element = backyards_page.wait_for_element(title_locator, timeout=5)
        assert title_element is not None, "Home title not locatable by accessibility ID"
        print(f"\n✓ Home title: locatable by ACCESSIBILITY_ID 'Backyards'")

        # Step 2: Inspect first cell - locatable by stable fallback (predicate)
        # Cells have name attributes like "BackyardGridItem_ZStack_<UUID>"
        # Using IOS_PREDICATE pattern as the "stable fallback" option from requirements
        first_cell_locator = (
            AppiumBy.IOS_PREDICATE,
            'type == "XCUIElementTypeButton" AND name BEGINSWITH "BackyardGridItem_ZStack_"'
        )
        first_cell = backyards_page.wait_for_element(first_cell_locator, timeout=5)
        assert first_cell is not None, "First cell not locatable by accessibility ID pattern"

        cell_name = first_cell.get_attribute("name")
        print(f"✓ First cell: locatable by stable pattern '{cell_name[:40]}...'")
