import unittest

from bs4 import BeautifulSoup

from termin import format_url_2


class FormatConcernUrlTests(unittest.TestCase):
    def test_uses_current_form_values_for_driver_license(self):
        soup = BeautifulSoup(
            """
            <form id="cnc-select-form" action="location">
              <input name="mdt" value="71">
              <div id="concerns_accordion-39395">
                <h3>Ersterteilung einer Fahrerlaubnis</h3>
                <div><input class="cnc-number" name="cnc-1277" value="0"></div>
              </div>
            </form>
            """,
            "html.parser",
        )

        success, url = format_url_2(
            soup,
            "Ersterteilung einer Fahrerlaubnis",
            page_url="https://termine.staedteregion-aachen.de/select2?md=2",
        )

        self.assertTrue(success)
        self.assertEqual(
            url,
            "https://termine.staedteregion-aachen.de/location"
            "?mdt=71&select_cnc=1&cnc-1277=1",
        )

    def test_uses_current_form_values_for_auslaenderamt(self):
        soup = BeautifulSoup(
            """
            <form id="cnc-select-form" action="location">
              <input name="mdt" value="95">
              <div id="concerns_accordion-1228">
                <h3>Infostelle</h3>
                <div><input class="cnc-number" name="cnc-341" value="0"></div>
              </div>
            </form>
            """,
            "html.parser",
        )

        success, url = format_url_2(
            soup,
            "Infostelle",
            page_url=(
                "https://termine.staedteregion-aachen.de/"
                "auslaenderamt/select2?md=1"
            ),
        )

        self.assertTrue(success)
        self.assertEqual(
            url,
            "https://termine.staedteregion-aachen.de/auslaenderamt/location"
            "?mdt=95&select_cnc=1&cnc-341=1",
        )

    def test_reports_missing_concern_position(self):
        soup = BeautifulSoup(
            """
            <form id="cnc-select-form" action="location">
              <input name="mdt" value="71">
              <div id="concerns_accordion-1">
                <h3>Only one concern</h3>
                <div><input class="cnc-number" name="cnc-1" value="0"></div>
              </div>
            </form>
            """,
            "html.parser",
        )

        success, message = format_url_2(
            soup,
            "Only one concern",
            form_options_position=1,
            page_url="https://termine.staedteregion-aachen.de/select2?md=2",
        )

        self.assertFalse(success)
        self.assertEqual(message, "No concern at position 1 for 'Only one concern'.")


if __name__ == "__main__":
    unittest.main()
