"""
Navigation Tests (N1-N5)
Tests for navigating between screens, scrolling, and going back.
"""
import pytest
from pages.backyards_page import BackyardsPage
from pages.backyard_detail_page import BackyardDetailPage
from pages.birds_page import BirdsPage


@pytest.mark.navigation
class TestNavigation:
    """Navigation tests for moving between screens."""

    def test_n1_open_first_detail_and_go_back(self, driver):
        """
        N1 — Open first detail & go back

        Steps: Tap first cell → verify detail → navigate Back.
        Asserts: Detail header visible; list visible again after Back.
        """
        from appium.webdriver.common.appiumby import AppiumBy

        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        # Verify we start on the list (NavBar shows "Backyards")
        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Step 1: Tap first cell
        backyards_page.tap_first_backyard()

        # Step 2: Verify detail page - assert on MULTIPLE detail elements

        # 2a. Check header: NavBar title is NOT a tab name (proves we navigated into detail)
        # Tab names: Backyards, Birds, Plants, Account
        nav_bar = driver.find_element(AppiumBy.CLASS_NAME, "XCUIElementTypeNavigationBar")
        nav_title = nav_bar.get_attribute("name")
        TAB_NAMES = ["Backyards", "Birds", "Plants", "Account"]
        assert nav_title not in TAB_NAMES, f"Still on tab view, not detail: {nav_title}"
        print(f"\n✓ Detail header visible: '{nav_title}'")

        # 2b. Check detail content: Food and Water buttons (only exist on detail page)
        # This double-checks we're on the backyard detail, not some other non-tab page
        assert detail_page.is_food_button_visible(timeout=5), "Food button not visible"
        assert detail_page.is_water_button_visible(timeout=5), "Water button not visible"
        print(f"✓ Detail content visible (Food & Water buttons)")

        # Step 3: Navigate Back
        detail_page.tap_back()

        # Assert: List visible again after Back (NavBar shows "Backyards" again)
        assert backyards_page.is_page_loaded(), "List not visible after Back"
        print(f"✓ List visible again after Back")

    def test_n2_scroll_list_down_up(self, driver):
        """
        N2 — Scroll list (down/up)

        Steps: Scroll to bottom, then to top.
        Asserts: List scrolls smoothly; no visual glitches.

        Approach: Verifies element count and order at top, bottom, and back to top.
        Open to feedback on alternative approaches for visual verification.
        """
        backyards_page = BackyardsPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Step 1: Capture initial state (names in display order)
        initial_names = backyards_page.get_backyard_names()
        initial_count = len(initial_names)
        print(f"\n✓ Initial state: {initial_count} backyards")
        print(f"  Order: {initial_names}")

        # Step 2: Scroll down twice (toward bottom)
        backyards_page.scroll_down()
        backyards_page.scroll_down()
        print(f"✓ Scrolled to bottom")

        # Step 3: Check state at bottom (catch glitches that might self-heal on scroll back)
        bottom_names = backyards_page.get_backyard_names()
        bottom_count = len(bottom_names)
        assert bottom_count == initial_count, \
            f"Element count changed at bottom: {initial_count} → {bottom_count}"
        assert bottom_names == initial_names, \
            f"Element order changed at bottom!\nInitial: {initial_names}\nAt bottom: {bottom_names}"
        print(f"✓ At bottom: still {bottom_count} backyards in same order")

        # Step 4: Scroll back up twice (toward top)
        backyards_page.scroll_up()
        backyards_page.scroll_up()
        print(f"✓ Scrolled back to top")

        # Step 5: Capture final state and compare
        final_names = backyards_page.get_backyard_names()
        final_count = len(final_names)

        # Assert: Same count (no elements lost or duplicated)
        assert final_count == initial_count, \
            f"Element count changed after scrolling: {initial_count} → {final_count}"

        # Assert: Same order (no visual glitches like shuffling)
        assert final_names == initial_names, \
            f"Element order changed!\nBefore: {initial_names}\nAfter: {final_names}"

        print(f"✓ No visual glitches detected: {final_count} backyards in same order")

    def test_n3_deep_navigation_path(self, driver):
        """
        N3 — Deep navigation path

        Steps: Open item A → Back → open item B.
        Asserts: Correct titles for A and B; no stale state.
        """
        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Step 1: Open item A (first backyard - Bird Springs)
        backyards_page.tap_backyard_by_name("Bird Springs")
        assert detail_page.is_page_loaded(), "Detail page A did not load"
        assert detail_page.is_title_visible("Bird Springs"), "Title A not correct"
        print(f"\n✓ Opened item A: Bird Springs")

        # Step 2: Back to list
        detail_page.tap_back()
        assert backyards_page.is_page_loaded(), "List not visible after Back"

        # Step 3: Open item B (different backyard - Feathered Friends)
        backyards_page.tap_backyard_by_name("Feathered Friends")
        assert detail_page.is_page_loaded(), "Detail page B did not load"
        assert detail_page.is_title_visible("Feathered Friends"), \
            "Title B not correct - possible stale state from item A"
        print(f"✓ Opened item B: Feathered Friends (no stale state)")

    def test_n4_pull_to_refresh(self, driver):
        """
        N4 — Pull-to-refresh (if available)

        Steps: Pull to refresh on list.
        Asserts: Spinner appears and disappears; list re-renders.
        """
        # This app does not have pull-to-refresh functionality.
        # Verified manually: no loading spinner appears when pulling down on any tab/view.
        pytest.skip("App does not have pull-to-refresh feature")

    def test_n5_external_entry(self, driver):
        """
        N5 — External entry

        Steps: From detail, use any in-app link/button to another screen (e.g., "See more").
        Asserts: Target screen loads and is interactable; Back returns to previous context.

        Approach: From detail, open food popup, then tap "Bird Food Shop" to prove popup
        is interactable. Navigate back through: Shop → Popup → Detail → List.
        Note: "Show More/Less" also exists but only expands a list, doesn't open a new screen.
        """
        backyards_page = BackyardsPage(driver)
        detail_page = BackyardDetailPage(driver)

        assert backyards_page.is_page_loaded(), "Backyards page not loaded"

        # Step 1: Navigate to detail page
        backyards_page.tap_first_backyard()
        assert detail_page.is_page_loaded(), "Detail page did not load"
        print(f"\n✓ On detail page")

        # Step 2: Tap food button (opens food popup)
        assert detail_page.is_food_button_visible(timeout=5), "Food button not visible"
        detail_page.tap_food_button()
        print(f"✓ Tapped food button")

        # Step 3: Assert food popup appears
        assert detail_page.is_food_popup_visible(timeout=5), "Food popup did not appear"
        print(f"✓ Food popup visible")

        # Step 4: Tap "Bird Food Shop" to prove popup is interactable
        detail_page.tap_food_popup_shop()
        print(f"✓ Tapped 'Bird Food Shop' (proves popup is interactable)")

        # Step 5: Assert shop screen loads
        assert detail_page.is_food_shop_visible(timeout=5), "Food shop screen did not load"
        print(f"✓ Shop screen loaded")

        # Step 6: Navigate back to food popup
        detail_page.tap_food_shop_back()
        assert detail_page.is_food_popup_visible(timeout=5), "Did not return to food popup"
        print(f"✓ Back to food popup")

        # Step 7: Close popup, return to detail
        detail_page.tap_food_popup_done()
        assert detail_page.is_page_loaded(), "Did not return to detail page"
        print(f"✓ Back to detail page")

        # Step 8: Return to list
        detail_page.tap_back()
        assert backyards_page.is_page_loaded(), "Could not return to list"
        print(f"✓ Back to list - full navigation path works")
