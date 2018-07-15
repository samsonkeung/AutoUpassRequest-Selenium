from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import time
import sys
import getpass

if len(sys.argv) < 1:
	print("autoUpassRenew.py <username>")
	exit()
else:
	username = sys.argv[1]
	password = getpass.getpass()

driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
driver.get("https://upassbc.translink.ca/")

schoolsDD = Select(driver.find_element_by_id("PsiId"))
schoolsDD.select_by_visible_text("University of British Columbia")

goBtn = driver.find_element_by_id("goButton")
goBtn.click();

#### Login to UBC CWL ####
username_f = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_username")));
password_f = driver.find_element_by_id("password")

username_f.send_keys(username)
password_f.send_keys(password)

password_f.submit();

if "Login Failed" in driver.page_source:
	driver.quit()
	input("Login Failed: press any key to close")
	exit()

#### Back to Translink ####
chkboxes = driver.find_elements_by_css_selector("form#form-request table [type=checkbox]")

if len(chkboxes) <= 0:
	print("No Upass to request!")
else:
	for chkbox in chkboxes:
		if not chkbox.is_selected():
			chkbox.click()
	chkboxes[0].submit()

## logout
logoutBtn = driver.find_element_by_css_selector("header #logout-link")
logoutBtn.click()

time.sleep(1)

try:
	dialog = driver.find_element_by_class_name("ui-dialog")

	if dialog.is_displayed():
		logoutBtn = dialog.find_element_by_id("LogOutLink")
		logoutBtn.click()
except NoSuchElementException:
	pass


time.sleep(3) # Let the user actually see something!
driver.quit()