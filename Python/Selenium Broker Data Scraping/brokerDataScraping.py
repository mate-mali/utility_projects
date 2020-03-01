# -*- coding: utf-8 -*-
"""
This is demonstration script that was used to demonstrate capacity of 
Web Scraping to get supplementary (commonly available) data from Internet
To have this script working packages:
    + selenium
    + pandas
    + time
    
Needs to be installed in Python Environment.
What is more, that additional executable, called Chromedriver, need to be downloaded 
and its location need to be provided in the first variable, chromeDriverPath.
Executable can be downloaded here: https://chromedriver.chromium.org/home

NOTE: to see chromedriver visible and operating, please put comment
on instruction chrome_options.add_argument('--headless') - line 33 -  otherwise, 
browser instance will remain headless/hidden
"""

chromeDriverPath = r'C:\Users\YOUR_USER_NAME\Desktop\chromedriver.exe'

from selenium import webdriver
import time
import pandas

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path=chromeDriverPath,chrome_options=chrome_options)
                          
#compared to the original file, I have replaced the file with thousands of brokers id with 
# user prompt
brokersCRD = input("Please insert list of broker/s CRD numbers separated by semicolon: ")
brokersCRD = brokersCRD.split(";")

                         
brokerPath = 'https://brokercheck.finra.org/individual/summary/'


#this loop will perform as many times 
#   as many standalone CRD numbers were provided

outputTotal = []
for CRD in brokersCRD:
    brokerCRD = CRD[0]
    navigation_link = brokerPath + str(CRD)
    driver.get(navigation_link)
    time.sleep(5)
    #lets find name
    element_to_find = driver.find_element_by_xpath('//*/div[@class="namesummary flex-noshrink gutter-right layout-wrap ng-binding"]')
    brokerNameText = element_to_find.text
    outputTotal.append([brokerCRD,"name",brokerNameText])
    
    #we will check if the person is a Broker
    try:
        element_to_find = driver.find_element_by_xpath('//*/div[@ng-if="vm.item.isActiveBD()"]')
        outputTotal.append([brokerCRD,"is broker","True"])
    except:
        outputTotal.append([brokerCRD,"is broker","False"])
    
    #lets find latest company
    #name
    element_to_find = driver.find_element_by_xpath('//*/div[@ng-bind-html="vm.item.getCurrentEmployment().firmName"]')
    outputTotal.append([brokerCRD,"current company name",element_to_find.text])
    #crd
    element_to_find = driver.find_element_by_xpath('//*/span[@ng-bind-html="vm.item.getCurrentEmployment().firmId"]')
    outputTotal.append([brokerCRD,"current company CRD",element_to_find.text])
    #address
    element_to_find = driver.find_element_by_xpath('//*/span[@ng-bind-html="vm.item.getCurrentEmployment().branchAddress1"]')
    string_address = element_to_find.text
    element_to_find = driver.find_element_by_xpath('//*/span[@ng-bind-html="vm.item.getCurrentEmployment().branchAddress2"]')
    string_address += ", " + element_to_find.text
    element_to_find = driver.find_element_by_xpath('//*/span[@ng-bind-html="vm.item.getCurrentEmployment().branchCity"]')
    string_address += ", " + element_to_find.text
    element_to_find = driver.find_element_by_xpath('//*/span[@ng-bind-html="vm.item.getCurrentEmployment().branchState"]')
    string_address += ", " + element_to_find.text
    element_to_find = driver.find_element_by_xpath('//*/span[@ng-bind-html="vm.item.getCurrentEmployment().branchZip"]')
    string_address += ", " + element_to_find.text
    outputTotal.append([brokerCRD,"current company adress",string_address])

    #disclosures
    #ng-binding dtilecount layout-align-center-stretch
    element_to_find = driver.find_element_by_xpath('//*/div[contains(@class,"disclosures")]')
    element_to_find = element_to_find.find_element_by_xpath('.//div[contains(@ng-class,"vm.isCount(vm.params.count[$index])?")]')
    outputTotal.append([brokerCRD,"disclosures",element_to_find.text])
    
    #years of experience
    #ng-binding dtilecount layout-align-center-stretch
    element_to_find = driver.find_element_by_xpath('//*/div[contains(@class,"dtile experience")]')
    #experience in numbers
    outputTotal.append([brokerCRD,"years of experience",element_to_find.text.split()[0]])
    outputTotal.append([brokerCRD,"total firms",element_to_find.text.split()[4]])
    
    #exams
    element_to_find = driver.find_element_by_xpath('//*/div[contains(@class,"exams layout-align-center-stretch")]')
    element_to_find = element_to_find.find_element_by_xpath('.//div[contains(@ng-class,"vm.isCount(vm.params.count[$index])?")]')
    outputTotal.append([brokerCRD,"exams",element_to_find.text])
    
    #licenses layout
    element_to_find = driver.find_element_by_xpath('//*/div[contains(@class,"licenses layout")]')
    element_to_find = element_to_find.find_element_by_xpath('.//div[contains(@ng-class,"vm.isCount(vm.params.count[$index])?")]')
    outputTotal.append([brokerCRD,"licenses",element_to_find.text])
    
    #certifications
    try:
        i = 1 #counter for examinations
        element_to_find = driver.find_element_by_xpath('//*/div[contains(@id,"examsSection")]')
        #extract the list of examinations
        list_of_elements = element_to_find.find_elements_by_xpath(
            './/div[@class="md-list-item-text layout-xs-column layout-gt-xs-row layout-align-sm-space-between-center flex"]'
        )
        for exams in list_of_elements:
            exams.text.split('\n')
            outputTotal.append([brokerCRD,"exam "+str(i),exams.text.split('\n')[0],exams.text.split('\n')[1]])
            i +=1
    except Exception as e:
        outputTotal.append([brokerCRD,"exam","no examinations disclosed"])
        print(e.args)
    i=1
    
    #counter for employment history
    try:
        id = 1 #counter for employment history
        element_to_find = driver.find_element_by_xpath('//*/div[contains(@id,"timelineSection")]')
        element_to_find = element_to_find.find_element_by_xpath('.//*[@id="clip-path"]')
        list_of_elements = element_to_find.find_elements_by_xpath('.//*[@class="group"]')
        for employers in list_of_elements:
            outputTotal.append([brokerCRD,"employer "+str(i),employers.text.split('\n')[0],employers.text.split('\n')[1]])
            i +=1
    except Exception as e:
        outputTotal.append([brokerCRD,"employer","no employment disclosed"])
        print(e.args)

#lets convert scrapped output to dataframe
datasetOutput = pandas.DataFrame(outputTotal,columns=['CRD','Attribute Name','Attribute Value','Date Periods'])

#ask user if he/she would like to export to csv
if input("Would You like to export data to csv (y/n)?").upper() == 'Y':
    datasetOutput.to_csv(input("Please provide absolute path for output file to be generated (csv): "),
                         index = False)
else:
    print("Data was not exported.")
    
print(datasetOutput)
print("Operation completed successfully.")