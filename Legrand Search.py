#SAV Digital Enviroments
#Julian Kizanis
print("Powered by Anaconda")

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

#from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
#from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
#from pandas import DataFrame
import pandas as pd
#import os
import time
import csv
import re


modelIndex = 0
specURL = []
Height = []
Width = []
Depth = []
Weight = []
Specifications = []
temp =""
attempts = 0
modelNumber = ""
noSpec = 0
noCAD = 0
noRVT = 0
shortDelay = .5

with open('ON-QModelList.csv', 'r') as f:
    reader = csv.reader(f)
    ModelNumbersTemp = list(reader)
ModelNumbers = [j for sub in ModelNumbersTemp for j in sub]

#for modelOg in ModelNumbers:
#    modelOg.replace("'", "")
#    modelOg.replace("'", "")
    
#i = 0
#for model in ModelNumbersAdj:
#    model = model.replace("-XX", "-WH")
    #ModelNumbers[i] = model
#    print(model)
    
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome()    
for model in ModelNumbers:
    modeltemp = model.replace("-XX", "-WH")
#    driver = webdriver.Chrome() 
    attempts = 0
    while attempts < 3:
        modelURL = f"https://www.legrand.us/onq/structured-wiring/preconfigured/customizable/{modeltemp}"        
        driver.get(modelURL)
#        print(modelURL)
    
        time.sleep(1)
    
        try:
            driver.find_element_by_xpath("(//div[@id='productDetailSpecifications'])").click()    #Product Specification Submittals
            specURL.insert(modelIndex,modelURL)
            time.sleep(1)
            driver.find_element_by_xpath("(//div[@id='productDetailResources'])").click()    #Product Specification Submittals
        except:
            try:
                driver.find_element_by_xpath("(//div[@id='productDetailResources'])").click()
                specURL.insert(modelIndex,modelURL)
            except:
                modelURL = f"https://www.legrand.us/onq/networking/wired-networks/data-modules/{modeltemp}"
                driver.get(modelURL)
#                print(modelURL)
                time.sleep(1)
            
                try:
                    driver.find_element_by_xpath("(//div[@id='productDetailSpecifications'])").click()    #Product Specification Submittals
                    specURL.insert(modelIndex,modelURL)
                    time.sleep(1)
                    driver.find_element_by_xpath("(//div[@id='productDetailResources'])").click()    #Product Specification Submittals
                except:
                    try:
                        driver.find_element_by_xpath("(//div[@id='productDetailResources'])").click()    #Product Specification Submittals
                        specURL.insert(modelIndex,modelURL)
                    except:
                        modelURL = f"https://www.legrand.us/onq/structured-wiring/preconfigured/inserts/{modeltemp}"
                        driver.get(modelURL)
#                        print(modelURL)
                        time.sleep(1)
                    
                        try:
                            driver.find_element_by_xpath("(//div[@id='productDetailSpecifications'])").click()    #Product Specification Submittals
                            specURL.insert(modelIndex,modelURL)
                            time.sleep(1)
                            driver.find_element_by_xpath("(//div[@id='productDetailResources'])").click()    #Product Specification Submittals
                        except:
                            try:
                                driver.find_element_by_xpath("(//div[@id='productDetailResources'])").click()    #Product Specification Submittals
                                specURL.insert(modelIndex,modelURL)
                            except:
                                specURL.insert(modelIndex,"")
                                Depth.insert(modelIndex, "")  
                                Height.insert(modelIndex, "")  
                                Width.insert(modelIndex, "")  
                                attempts += 3
        attempts = 3
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
    
        try:
            tempSoup = soup.find_all(string = re.compile('Depth'))
            for temp in tempSoup:                
                if "(US)" in temp:
                    Depth.insert(modelIndex, temp.replace("Depth (US):", "").strip().replace('"','').replace(" in",""))

            tempSoup = soup.find_all(string = re.compile('Height'))
            for temp in tempSoup:                
                if "(US)" in temp:
                    Height.insert(modelIndex, temp.replace("Height (US):", "").strip().replace('"','').replace(" in",""))
                    
            tempSoup = soup.find_all(string = re.compile('Width'))
            for temp in tempSoup:
                if "(US)" in temp:
                    Width.insert(modelIndex, temp.replace("Width (US):", "").strip().replace('"','').replace(" in",""))
            
        except AttributeError:
            Depth.insert(modelIndex, "")  
            Height.insert(modelIndex, "")  
            Width.insert(modelIndex, "")  
        attempts = 3
        print(f"Height: {Height[modelIndex]}")
        print(f"Width: {Width[modelIndex]}")
        print(f"Depth: {Depth[modelIndex]}")
        print(f"specURL: {specURL[modelIndex]}")
        print(f"modelIndex: {modelIndex}")
        modelIndex += 1
        
        df = pd.DataFrame(list(zip(ModelNumbers, Height, Width, Depth, specURL)), columns =['Model Number', 'Height', 'Width', 'Depth', 'URL'])  
        #df is a panda object that contains: ModelCategory, ModelName, ModelPdf
        export_csv = df.to_csv ('ON-QSpecSheet HxWxD URL.csv', header=True) #Don't forget to add '.csv' at the end of the path
        
df = pd.DataFrame(list(zip(ModelNumbers, Height, Width, Depth, specURL)), columns =['Model Number', 'Height', 'Width', 'Depth', 'URL'])  
#df is a panda object that contains: ModelCategory, ModelName, ModelPdf
export_csv = df.to_csv ('Complete ON-Q Spec Sheet HxWxD URL.csv', header=True) #Don't forget to add '.csv' at the end of the path
        
        
        
        
        
        
        
        
        
