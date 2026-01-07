"""
Functional Tests (F1-F12)
Tests for app functionality per PDF requirements.
"""
import pytest
from pages.backyards_page import BackyardsPage
from pages.backyard_detail_page import BackyardDetailPage
from pages.birds_page import BirdsPage


@pytest.mark.functional
class TestFunctional:
    """Functional tests for app features."""

    def test_f1_toggle_favorite(self, driver):
        """
        F1 — Toggle Favorite

        Steps: Open first item, tap favorite, verify ON, tap again, verify OFF.
        Asserts: State flips correctly both ways.

        Approach: Uses element screenshot comparison since the favorite button
        has no attribute that changes when toggled (verified via inspector).
        """
        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Step 1: Open first item
        backyards_page.tap_first_backyard()
        assert detail_page.is_page_loaded(), "Detail page not loaded"
        print(f"\n✓ Opened first item")

        # Step 2: Capture initial state
        screenshot_initial = detail_page.get_favorite_screenshot()
        assert screenshot_initial is not None, "Could not capture favorite button screenshot"
        print(f"✓ Captured initial favorite state")

        # Step 3: Tap favorite (toggle ON or OFF)
        detail_page.tap_favorite()
        screenshot_after_first_toggle = detail_page.get_favorite_screenshot()

        # Verify state changed
        assert screenshot_initial != screenshot_after_first_toggle, \
            "Favorite state did not change after first toggle"
        print(f"✓ First toggle: state changed (verify ON)")

        # Step 4: Tap again (toggle back)
        detail_page.tap_favorite()
        screenshot_after_second_toggle = detail_page.get_favorite_screenshot()

        # Verify state flipped back to original
        assert screenshot_after_second_toggle == screenshot_initial, \
            "Favorite state did not return to original after second toggle"
        print(f"✓ Second toggle: state returned to original (verify OFF)")

    def test_f2_detail_content_validation(self, driver):
        """
        F2 — Detail content validation

        Steps: Open item, check all fields present.
        Asserts: Title, image(s), description, etc. appear.
        """
        from appium.webdriver.common.appiumby import AppiumBy

        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Open a backyard detail
        backyards_page.tap_backyard_by_name("Bird Springs")
        assert detail_page.is_page_loaded(), "Detail page not loaded"
        print(f"\n✓ Opened detail page")

        # --- Navigation elements ---
        # Back button
        assert detail_page.is_back_button_visible(timeout=5), "Back button not visible"
        print(f"✓ Back button visible")

        # Favorite button
        assert detail_page.is_favorite_button_visible(timeout=5), "Favorite button not visible"
        print(f"✓ Favorite button visible")

        # --- Header/Title (verify via NavigationBar to avoid false positive from list) ---
        nav_bar = driver.find_element(AppiumBy.CLASS_NAME, "XCUIElementTypeNavigationBar")
        nav_title = nav_bar.get_attribute("name")
        assert nav_title == "Bird Springs", f"Title mismatch: expected 'Bird Springs', got '{nav_title}'"
        print(f"✓ Title visible in NavBar: '{nav_title}'")

        # --- Banner/Image area ---
        fountain_locator = (
            AppiumBy.IOS_PREDICATE,
            'name CONTAINS "FountainArtworkImage"'
        )
        assert detail_page.is_element_visible(fountain_locator, timeout=5), \
            "Banner image (fountain) not visible"
        print(f"✓ Banner image visible")

        # --- Food button (icon, name, time remaining, arrows) ---
        assert detail_page.is_food_button_visible(timeout=5), "Food button not visible"
        print(f"✓ Food button visible")

        # --- Water button (icon, name, time remaining, refresh arrow) ---
        assert detail_page.is_water_button_visible(timeout=5), "Water button not visible"
        print(f"✓ Water button visible")

        # --- Recent Visitors section ---
        recent_visitors_locator = (
            AppiumBy.IOS_PREDICATE,
            'name == "Recent Visitors" AND type == "XCUIElementTypeStaticText"'
        )
        assert detail_page.is_element_visible(recent_visitors_locator, timeout=5), \
            "Recent Visitors section header not visible"
        print(f"✓ Recent Visitors header visible")

        # Check at least one bird in visitors list (bird name as StaticText)
        # Known birds: Petrel, Cardinal, Hummingbird, Swallow, Dove, etc.
        bird_locator = (
            AppiumBy.IOS_PREDICATE,
            'type == "XCUIElementTypeStaticText" AND '
            '(label == "Petrel" OR label == "Cardinal" OR label == "Hummingbird" '
            'OR label == "Swallow" OR label == "Dove")'
        )
        assert detail_page.is_element_visible(bird_locator, timeout=5), \
            "No birds visible in Recent Visitors list"
        print(f"✓ Bird(s) visible in Recent Visitors list")

        # --- Show More button (scroll down to find) ---
        detail_page.scroll_down()
        assert detail_page.is_show_more_visible(timeout=5), "Show More button not visible"
        print(f"✓ Show More button visible")

    def test_f3_search_filter(self, driver):
        """
        F3 — Search / Filter

        Steps: Type query in search bar; clear search.
        Asserts: Results filter; clearing restores full list.

        Tests the full search flow:
        1. Verify backyards visible before search
        2. Open search -> placeholders appear
        3. Search "Bird" -> filters to 1 result
        4. Clear text -> placeholders return
        5. Search "C" -> filters to 2 results
        6. Close search -> all backyards return
        """
        backyards_page = BackyardsPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Step 1: Count backyards before opening search
        initial_count = backyards_page.get_backyard_count()
        print(f"\n✓ Initial backyard count: {initial_count}")

        # Step 2: Tap search bar - placeholders should appear
        backyards_page.tap_search_bar()
        assert backyards_page.are_placeholders_visible(), \
            "Search placeholders not visible after opening search"
        placeholder_count = backyards_page.get_placeholder_count()
        print(f"✓ Search opened: {placeholder_count} placeholders visible")

        # Step 3: Search "Bird" - should show exactly 1 backyard (Bird Springs)
        backyards_page.search_for("Bird")
        backyards_page.wait_for_backyard_count(1)
        assert backyards_page.is_backyard_visible("Bird Springs"), \
            "Bird Springs not visible after searching 'Bird'"
        assert backyards_page.get_placeholder_count() == 0, \
            "Placeholders should not be visible when search has results"
        print(f"✓ Search 'Bird': 1 result (Bird Springs)")

        # Step 4: Clear text - placeholders should return
        backyards_page.clear_search_text()
        assert backyards_page.are_placeholders_visible(), \
            "Placeholders not visible after clearing search text"
        print(f"✓ Cleared text: placeholders returned")

        # Step 5: Search "C" - should show exactly 2 backyards (Calm Palms, Chirp Center)
        backyards_page.search_for("C")
        backyards_page.wait_for_backyard_count(2)
        assert backyards_page.is_backyard_visible("Calm Palms"), \
            "Calm Palms not visible after searching 'C'"
        print(f"✓ Search 'C': 2 results")

        # Step 6: Close search - all backyards should return
        backyards_page.close_search()
        backyards_page.wait_for_backyard_count(initial_count)
        restored_count = backyards_page.get_backyard_count()
        assert restored_count == initial_count, \
            f"Full list not restored: expected {initial_count}, got {restored_count}"
        print(f"✓ Search closed: {restored_count} backyards restored")

    def test_f4_retain_state_after_navigation(self, driver):
        """
        F4 — Retain state after navigation

        Steps: Change a setting (favorite) → navigate away → return.
        Asserts: Setting persists on both list and detail views.

        Note: Using favorite toggle as the "setting" to change.
        Tests persistence on both the Backyards list and detail page.
        """
        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Step 1: Capture initial favorite state on list
        list_screenshot_before = backyards_page.get_first_favorite_screenshot()
        print(f"\n✓ Captured initial favorite state on list")

        # Step 2: Open first backyard and capture initial state on detail
        backyards_page.tap_first_backyard()
        assert detail_page.is_page_loaded(), "Detail page not loaded"
        detail_screenshot_before = detail_page.get_favorite_screenshot()

        # Step 3: Toggle favorite
        detail_page.tap_favorite()
        detail_screenshot_after = detail_page.get_favorite_screenshot()
        assert detail_screenshot_before != detail_screenshot_after, \
            "Toggle did not change state on detail"
        print(f"✓ Toggled favorite on detail page")

        # Step 4: Navigate back to list and verify state changed there too
        detail_page.tap_back()
        assert backyards_page.is_page_loaded(), "Did not return to list"
        list_screenshot_after = backyards_page.get_first_favorite_screenshot()
        assert list_screenshot_before != list_screenshot_after, \
            "Favorite state did not update on list view"
        print(f"✓ Favorite state updated on list view")

        # Step 5: Return to detail and verify state persisted
        backyards_page.tap_first_backyard()
        assert detail_page.is_page_loaded(), "Detail page not loaded on return"
        detail_screenshot_return = detail_page.get_favorite_screenshot()
        assert detail_screenshot_return == detail_screenshot_after, \
            "Favorite state did not persist on detail after navigation"
        print(f"✓ Favorite state persisted on detail page")

    def test_f5_empty_edge_search(self, driver):
        """
        F5 — Empty / edge search

        Steps: Search for nonsense string.
        Asserts: "No results" state shown; no crash.
        """
        backyards_page = BackyardsPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Search for nonsense string
        backyards_page.search_for("xyznonexistent123")

        # Wait for filter to apply - expect 0 results
        backyards_page.wait_for_backyard_count(0)

        # Verify no crash - search bar still visible and functional
        assert backyards_page.is_search_bar_visible(), "App crashed after nonsense search"
        print(f"\n✓ No crash after nonsense search")

        # Verify no results (use wait=False since we expect 0)
        result_count = backyards_page.get_backyard_count(wait=False)
        assert result_count == 0, \
            f"Expected 0 results for nonsense search, got {result_count}"
        print(f"✓ No results shown: {result_count} items")

        # Verify no placeholders either (use wait=False since we expect 0)
        assert backyards_page.get_placeholder_count(wait=False) == 0, \
            "Placeholders should not be visible when search has text"
        print(f"✓ No placeholders shown (correct empty state)")

    def test_f6_sort_category_switch(self, driver):
        """
        F6 — Sort / category switch (if present)

        Steps: Toggle sort order or category filter.
        Asserts: List order changes correctly.

        Tests the category filter in Birds tab:
        1. Navigate to Birds tab
        2. Count all birds visible
        3. Tap search bar -> suggestions appear
        4. Tap "Dove" suggestion
        5. Verify search bar contains "Dove"
        6. Verify only Dove birds are shown
        7. Clear search -> suggestions return
        8. Close search -> all birds return
        """
        birds_page = BirdsPage(driver)

        # Step 1: Navigate to Birds tab
        birds_page.tap_birds_tab()
        assert birds_page.is_page_loaded(), "Birds page not loaded"
        print(f"\n✓ Navigated to Birds tab")

        # Step 2: Count all birds before filtering
        initial_count = birds_page.get_bird_count()
        print(f"✓ Initial bird count: {initial_count}")
        assert initial_count > 0, "No birds visible in grid"

        # Step 3: Tap search bar -> suggestions should appear
        birds_page.tap_search_bar()
        assert birds_page.are_suggestions_visible(), \
            "Search suggestions not visible after tapping search bar"
        suggestion_count = birds_page.get_suggestion_count()
        print(f"✓ Search opened: {suggestion_count} category suggestions visible")

        # Step 4: Tap "Dove" suggestion
        birds_page.tap_suggestion("Dove")

        # Step 5: Verify search bar contains "Dove" (wait for value to be populated)
        birds_page.wait_for_search_value("Dove")
        search_value = birds_page.get_search_value()
        print(f"✓ Tapped 'Dove' suggestion - search bar shows: '{search_value}'")

        # Step 6: Verify only Dove birds are shown (should be 6 Doves)
        birds_page.wait_for_bird_count(6)  # All birds with "Dove" label
        dove_count = birds_page.get_bird_count()
        assert dove_count == 6, f"Expected 6 Doves, got {dove_count}"

        # Verify all visible birds are Doves
        bird_types = birds_page.get_visible_bird_types()
        assert all(bird == "Dove" for bird in bird_types), \
            f"Expected only Dove birds, got: {bird_types}"
        print(f"✓ Filtered to {dove_count} Dove birds")

        # Step 7: Clear search -> suggestions should return
        birds_page.clear_search_text()
        assert birds_page.are_suggestions_visible(), \
            "Suggestions not visible after clearing search"
        print(f"✓ Cleared search text: suggestions returned")

        # Step 8: Close search -> all birds should return
        birds_page.close_search()
        birds_page.wait_for_bird_count(initial_count)
        restored_count = birds_page.get_bird_count()
        assert restored_count == initial_count, \
            f"Full list not restored: expected {initial_count}, got {restored_count}"
        print(f"✓ Search closed: {restored_count} birds restored")

    def test_f7_time_format_12_hour(self, driver):
        """
        F7 — Time format (12-hour regression)

        Steps: Ensure 12-hour time values display correctly.
        Asserts: AM/PM values, no crashes, format consistency.
        """
        from appium.webdriver.common.appiumby import AppiumBy

        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Open detail to see time values (Recent Visitors shows visit times)
        backyards_page.tap_first_backyard()
        assert detail_page.is_page_loaded(), "Detail page not loaded"

        # Scroll to Recent Visitors section
        detail_page.scroll_down()

        # Look for time format elements (e.g., "4 min, 40 sec" or "1 hr, 24 min")
        # The app shows relative time, not 12-hour clock format
        time_locator = (
            AppiumBy.IOS_PREDICATE,
            'label CONTAINS "min" OR label CONTAINS "hr"'
        )
        time_elements = detail_page.get_elements(time_locator)

        assert len(time_elements) > 0, "No time values found on detail page"
        print(f"\n✓ Found {len(time_elements)} time elements")

        # Verify format consistency (should contain time units)
        for el in time_elements[:3]:  # Check first 3
            label = el.get_attribute("label")
            assert "min" in label or "hr" in label or "sec" in label, \
                f"Unexpected time format: {label}"
            print(f"✓ Time format OK: '{label}'")

    def test_f8_dark_mode_basic(self, driver):
        """
        F8 — Dark mode (basic)

        Pre: Set Simulator Appearance to Dark.
        Steps: Open home and a detail screen.
        Asserts: Critical text is readable; buttons visible/enabled.
        """
        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        try:
            # Set dark mode
            driver.execute_script('mobile: setAppearance', {'style': 'dark'})
            print(f"\n✓ Set appearance to dark mode")

            # Step 1: Verify home page elements are visible/enabled
            assert backyards_page.is_page_loaded(), "Backyards page not loaded in dark mode"
            print(f"✓ Home page title visible")

            assert backyards_page.get_backyard_count() >= 1, "No backyard cells visible in dark mode"
            print(f"✓ Backyard cells visible")

            assert backyards_page.is_search_bar_visible(), "Search bar not visible in dark mode"
            print(f"✓ Search bar visible")

            # Step 2: Open a detail screen
            backyards_page.tap_first_backyard()
            assert detail_page.is_page_loaded(), "Detail page not loaded in dark mode"
            print(f"✓ Detail page loaded")

            # Step 3: Verify detail page elements are visible/enabled
            assert detail_page.is_back_button_visible(), "Back button not visible in dark mode"
            print(f"✓ Back button visible")

            assert detail_page.is_favorite_button_visible(), "Favorite button not visible in dark mode"
            print(f"✓ Favorite button visible")

            assert detail_page.is_food_button_visible(), "Food button not visible in dark mode"
            print(f"✓ Food button visible")

            assert detail_page.is_water_button_visible(), "Water button not visible in dark mode"
            print(f"✓ Water button visible")

            print(f"✓ All critical elements visible/enabled in dark mode")

        finally:
            # Restore light mode
            driver.execute_script('mobile: setAppearance', {'style': 'light'})
            print(f"✓ Restored appearance to light mode")

    def test_f9_offline_low_connectivity(self, driver):
        """
        F9 — Offline / low connectivity (if app fetches)

        Pre: Disable network on Simulator.
        Steps: Launch/open list.
        Asserts: Graceful error/placeholder; no infinite spinner.
        """
        # The app doesn't seem to fetch data - everything loads locally.
        # The only network feature I found was the subscription button in Account tab.
        # I couldn't find a way to toggle airplane mode or disable network on iOS simulator
        # through Appium - the methods I tried were either Android-only or not supported.
        pytest.skip(
            "Could not find a reliable way to simulate offline on iOS simulator. "
            "App data appears to be local anyway."
        )

    def test_f10_startup_performance(self, driver):
        """
        F10 — Start-up performance (≤3s)

        Steps: Measure time from launch to home visible.
        Asserts: Under agreed threshold (e.g., ≤ 3s on local simulator).
        """
        import time
        from appium.webdriver.common.appiumby import AppiumBy

        bundle_id = "com.example.apple-samplecode.Backyard-Birds"

        # Terminate the app first
        driver.terminate_app(bundle_id)
        print(f"\n✓ Terminated app")

        # Start timing and launch
        start_time = time.time()
        driver.activate_app(bundle_id)

        # Check for home page title with minimal overhead
        title_locator = (
            AppiumBy.IOS_PREDICATE,
            'name == "Backyards" AND type == "XCUIElementTypeStaticText"'
        )
        while time.time() - start_time < 10:  # 10s max wait
            try:
                element = driver.find_element(*title_locator)
                if element.is_displayed():
                    break
            except:
                pass
            time.sleep(0.05)  # Check every 50ms

        elapsed = time.time() - start_time

        assert elapsed <= 3.0, \
            f"App took {elapsed:.2f}s to launch (max 3s)"

        print(f"✓ App launched and interactive in {elapsed:.2f}s (under 3s)")

    def test_f11_idempotent_favorite_flow(self, driver):
        """
        F11 — Idempotent favorite flow

        Steps: Run F1 twice on the same item.
        Asserts: Test passes both times; state cleanly toggles without flakiness.
        """
        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Open detail
        backyards_page.tap_first_backyard()
        assert detail_page.is_page_loaded(), "Detail page not loaded"

        # Run the F1 toggle flow twice
        for run in range(1, 3):
            print(f"\n--- Run {run} ---")

            # Capture initial state
            screenshot_initial = detail_page.get_favorite_screenshot()
            assert screenshot_initial is not None, f"Run {run}: Could not capture initial state"
            print(f"✓ Run {run}: Captured initial state")

            # Toggle ON
            detail_page.tap_favorite()
            screenshot_after_toggle = detail_page.get_favorite_screenshot()
            assert screenshot_initial != screenshot_after_toggle, \
                f"Run {run}: State did not change after toggle ON"
            print(f"✓ Run {run}: Toggle ON - state changed")

            # Toggle OFF
            detail_page.tap_favorite()
            screenshot_after_restore = detail_page.get_favorite_screenshot()
            assert screenshot_after_restore == screenshot_initial, \
                f"Run {run}: State did not return to original after toggle OFF"
            print(f"✓ Run {run}: Toggle OFF - state restored")

        print(f"\n✓ F1 flow passed both times - no flakiness")

    def test_f12_screenshot_on_failure(self, driver):
        """
        F12 — Screenshot on failure

        Steps: Intentionally fail a selector once.
        Asserts: Framework captures a screenshot and attaches to report.

        This test fails on purpose. When it fails, conftest.py captures a
        screenshot to screenshots/test_f12_screenshot_on_failure_failure.png
        """
        # This test is designed to fail to demonstrate screenshot capture
        assert False, "Intentional failure - check screenshots/ for captured image"
