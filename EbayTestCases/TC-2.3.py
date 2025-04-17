from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

#test credentials
USERNAME = "vimpandey2001@gmail.com"
PASSWORD = "wrong_password"
test_case_id = "TC-2.3"
description = "Invalid Username Login Attempt"
result = "FAIL"
screenshot_name = ""

driver = webdriver.Chrome()
driver.maximize_window()
os.makedirs("screenshots", exist_ok=True)

def take_screenshot(name):
    driver.save_screenshot(f"screenshots/{name}.png")

try:
    #enter the URL
    driver.get("https://www.ebay.com/")
    time.sleep(2)

    #click Sign in link
    sign_in_link = driver.find_element(By.LINK_TEXT, "Sign in")
    sign_in_link.click()
    #time for solving recaptcha
    time.sleep(20)

    #enter username
    user_field = driver.find_element(By.ID, "userid")
    user_field.send_keys("invaliduser@example.com")
    driver.find_element(By.ID, "signin-continue-btn").click()
    time.sleep(3)

    #check for error message
    error_msg = driver.find_elements(By.ID, "signin-error-msg")
    if error_msg:
        print("TC-2.3: PASS")
        screenshot_name = "invalid_username_detected.png"
        take_screenshot("invalid_username_detected")
        result = "PASS"
    else:
        print("TS-2.3: FAIL - No error message shown")
        screenshot_name = "invalid_username_not_detected.png"
        take_screenshot("invalid_username_not_detected")
except Exception as e:
    print(f"TC-2.3: FAIL - {e}")
    screenshot_name = "invalid_username_exception.png"
    take_screenshot("invalid_username_exception")

driver.quit()

#generate html report
report_dir = "selenium_reports"
os.makedirs(report_dir, exist_ok=True)
report_path = os.path.join(report_dir, f"{test_case_id}_Test_Report.html")

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Report - {test_case_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 80%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .result {{ font-weight: bold; color: {'green' if result == 'PASS' else 'red'}; }}
        img {{ border: 1px solid #ccc; margin-top: 10px; max-width: 600px; }}
    </style>
</head>
<body>
    <h1>Test Case Report</h1>
    <table>
        <tr>
            <th>Test Case ID</th>
            <td>{test_case_id}</td>
        </tr>
        <tr>
            <th>Description</th>
            <td>{description}</td>
        </tr>
        <tr>
            <th>Result</th>
            <td class="result">{result}</td>
        </tr>
        <tr>
            <th>Screenshot</th>
            <td><img src="../screenshots/{screenshot_name}" alt="Screenshot for {test_case_id}"></td>
        </tr>
    </table>
</body>
</html>
"""

with open(report_path, "w") as file:
    file.write(html_content)

print(f"HTML report generated: {report_path}")