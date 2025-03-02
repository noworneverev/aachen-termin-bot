from playwright.sync_api import sync_playwright
import re
import json
from html import unescape
import logging

# Assuming Appointment is a defined class
class Appointment:
    @staticmethod
    def from_json(data):
        # Placeholder implementation; adjust based on your actual class
        return data

def get_appointments() -> list[Appointment]:
    with sync_playwright() as p:
        # Launch browser in headless mode (required for GitHub Actions)
        browser = p.chromium.launch(headless=True)

        # Create a browser context with stealth settings
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",  # Do Not Track
            }
        )
        page = context.new_page()

        # Mask automation indicators
        page.evaluate("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3].map(() => ({})) });
        """)

        # Visit homepage to establish session and set referer
        homepage = "https://stadt-aachen.saas.smartcjm.com/"
        page.goto(homepage)
        page.wait_for_load_state("networkidle")

        # Navigate to the target URL
        initial_url = "https://stadt-aachen.saas.smartcjm.com/m/buergerservice/extern/calendar/?uid=15940648-b483-46d9-819e-285707f1fc34"
        page.goto(initial_url)
        page.wait_for_load_state("networkidle")

        # Get page content and check for Cloudflare block
        content = page.content()
        if "Sorry, you have been blocked" in content:
            logging.error("Blocked by Cloudflare")
            browser.close()
            raise Exception("Failed to bypass Cloudflare protection")

        # Extract the request verification token
        pattern = r"<input\b[^>]*\bname=['\"]__RequestVerificationToken['\"][^>]*\bvalue=['\"](.*?)['\"][^>]*>"
        match = re.search(pattern, content)
        if not match:
            logging.error("Could not find request verification token")
            browser.close()
            raise Exception("Token extraction failed")
        form_token = match.group(1)

        # Construct and submit form data (adjust based on your actual needs)
        form_data = {
            "__RequestVerificationToken": form_token,
            "action_type": "",
            "steps": "serviceslocationssearch_resultsbookingfinish",
            "step_current": "services",
            "step_current_index": "0",
            "step_goto": "+1",
            "services": "7bee4872-ba56-4070-9f6d-f45afdf491cb",
            "service_7bee4872-ba56-4070-9f6d-f45afdf491cb_amount": "1"
        }
        response = page.request.post(initial_url, form=form_data)
        
        # Navigate to search results (adjust URL construction as needed)
        base_url = initial_url.split("?")[0]
        search_result_url = f"{base_url}search_result?search_mode=all&uid=15940648-b483-46d9-819e-285707f1fc34"
        page.goto(search_result_url)
        page.wait_for_load_state("networkidle")
        content = page.content()

        # Extract JSON data (adjust pattern based on actual page structure)
        json_pattern = r"(?<=<div id=\"json_appointment_list\">).*?(?=</div>)"
        json_match = re.search(json_pattern, content, flags=re.DOTALL)
        if not json_match:
            logging.error("JSON data not found in page content")
            browser.close()
            raise Exception("Failed to extract appointment data")

        appointments_json = json.loads(unescape(json_match.group(0)))
        if "nothing_Found" in appointments_json.get("appointments", ""):
            logging.info("No appointments found")
            browser.close()
            return []

        # Parse appointments
        appointments = [Appointment.from_json(appointment) for appointment in appointments_json["appointments"]]
        
        browser.close()
        return appointments

# Example usage
if __name__ == "__main__":
    try:
        appointments = get_appointments()
        print(f"Found {len(appointments)} appointments")
    except Exception as e:
        print(f"Error: {str(e)}")