from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import getpass

username = input("Please enter username: ")
password = getpass.getpass()
confirmPw = getpass.getpass()

if password != confirmPw:
	print("passwords do not match!!")
	exit()

driver = webdriver.Chrome(executable_path=r'C:\chromedriver_win32\chromedriver.exe')
driver.get("https://upassbc.translink.ca/")

schoolsDD = Select(driver.find_element_by_id("PsiId"))
schoolsDD.select_by_visible_text("University of British Columbia")

goBtn = driver.find_element_by_id("goButton")
goBtn.click();

#### Login to UBC CWL ####
username_f = driver.find_element_by_id("j_username")
password_f = driver.find_element_by_id("password")

username_f.send_keys(username)
password_f.send_keys(password)

password_f.submit();

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

dialog = driver.find_element_by_class_name("ui-dialog")

if dialog.is_displayed():
	logoutBtn = dialog.find_element_by_id("LogOutLink")
	logoutBtn.click()


time.sleep(3) # Let the user actually see something!
driver.quit()