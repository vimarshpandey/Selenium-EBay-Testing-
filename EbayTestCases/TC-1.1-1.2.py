from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

driver = webdriver.Chrome()
driver.maximize_window()
os.makedirs("screenshots", exist_ok=True)

def take_screenshot(name):
    driver.save_screenshot(f"screenshots/{name}.png")

results = {}

# TS-1.1 - valid search
try:
    driver.get("https://www.ebay.com/")
    search_box = driver.find_element(By.ID, "gh-ac")
    search_box.clear()
    search_box.send_keys("laptop")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    items = driver.find_elements(By.CSS_SELECTOR, ".s-item")
    assert len(items) > 0
    take_screenshot("valid_search")
    results["TC-1.1"] = ("PASS", "valid_search.png")
except Exception as e:
    take_screenshot("valid_search_fail")
    results["TC-1.1"] = (f"FAIL - {e}", "valid_search_fail.png")

# TS-1.2 - invalid search
try:
    driver.get("https://www.ebay.com/")
    search_box = driver.find_element(By.ID, "gh-ac")
    search_box.clear()
    search_box.send_keys("asdfghjkllzz")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    result_text = driver.find_element(By.CSS_SELECTOR, ".srp-controls__count-heading").text
    assert "0" in result_text or "results" in result_text.lower()
    take_screenshot("invalid_search")
    results["TC-1.2"] = ("PASS", "invalid_search.png")
except Exception as e:
    take_screenshot("invalid_search_fail")
    results["TC-1.2"] = (f"FAIL - {e}", "invalid_search_fail.png")

#output
driver.quit()
print("\nTEST RESULTS:")
for k, v in results.items():
    print(f"{k}: {v[0]}")

#generate html report
report_dir = "selenium_reports"
os.makedirs(report_dir, exist_ok=True)
report_path = os.path.join(report_dir, "TC-1_Search_Functionality_Report.html")

html_rows = ""
for case_id, (result_text, screenshot_file) in results.items():
    html_rows += f"""
    <tr>
        <td>{case_id}</td>
        <td>{"Valid Search" if case_id == "TC-1.1" else "Invalid Search"}</td>
        <td style="color:{'green' if 'PASS' in result_text else 'red'}; font-weight:bold;">{result_text}</td>
        <td><img src="../screenshots/{screenshot_file}" alt="{case_id}" style="max-width:400px;"></td>
    </tr>
    """

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Report - Search Functionality</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        img {{ border: 1px solid #ccc; margin-top: 10px; }}
    </style>
</head>
<body>
    <h1>Test Case Report: Search Functionality</h1>
    <table>
        <tr>
            <th>Test Case ID</th>
            <th>Description</th>
            <th>Result</th>
            <th>Screenshot</th>
        </tr>
        {html_rows}
    </table>
</body>
</html>
"""

with open(report_path, "w") as file:
    file.write(html_content)

print(f"\nHTML report generated: {report_path}")