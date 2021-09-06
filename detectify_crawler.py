import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import json
import pandas as pd

def get_data(ID): 
  """
  Gets text data from the web page. It uses try for not all vulnerabilities have the same structure, so some elements are not present in some webpages. 
  Args:
    ID (str): the ID of the vulnerability, used to build the URL and to reffer the vulnerabilities in the database.
  """
    # Get Scan Data
    try:
        FoundAt = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[3]/section/div[1]').text
    except:
        FoundAt = ""
    try:
        Severity = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[3]/section/div[2]/span/div').text
    except:
        Severity = ""
    try:
        Status = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[3]/section/div[3]/strong').text
    except:
        Status = ""
    try:
        CVSSScore = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[3]/section/div[4]/strong').text
    except:
        CVSSScore = ""
    try:
        Meaning = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[4]').text
    except:
        Meaning = ""
    try:
        RequestResponse = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[5]').text
    except:
        RequestResponse = ""
    try:
        Details = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[6]').text
    except:
        Details = ""
    try:
        References = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[7]').text
    except:
        References = ""

    data = [
        ID,
        FoundAt,
        Severity,
        Status,
        CVSSScore,
        Meaning,
        RequestResponse,
        Details,
        References
    ]
    return data


def appendData(data): 
  """
  Appends the data to the CSV file.
  Args:
    data (lsit): list of data to be appended to the spreadsheet
  """
    # with open('DetectifyScans.csv','a') as fd:
    #     fd.write(data)
    with open(r'DetectifyScans.csv', 'a') as f:
        writer = csv.writer(f)
        try:
            writer.writerow(data)
        except:
            print('error writing data')

#Set up webdriver with Chrome
print('Setting up web driver... ')
options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" #path to chrome.exe
options.headless = False
options.add_argument("start-maximized")
driver = WebDriver(r"Cchromedriver.exe",options=options) #path to webdriver chromedriver.exe
driver.implicitly_wait(15)
driver.get("https://detectify.com/app/vulnerabilities")
#Log in
driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/form/div[1]/input').send_keys("user@login")
driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/form/div[2]/div/input').send_keys("passWord")
driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/button/span').click()
time.sleep(12)

scanIds = pd.read_csv('vulnerability_ids.csv') # list of vulnerabilities IDs

l = len(scanIds)
i=0
while i < l:
    driver.get('https://detectify.com/app/'+str(scanIds['Ids'][i])+'/vulnerability')
    scanData = get_data(scanIds['Ids'][i])
    appendData(scanData)
    print(scanData)
    i+=1

driver.close()
