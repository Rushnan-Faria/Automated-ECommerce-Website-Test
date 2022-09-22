from itertools import product
from turtle import back
from jmespath import search
import re
from selenium import webdriver
from time import sleep
import requests
from urllib.request import Request,urlopen
from time import time
import pymongo
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
links=[]
b="chaldal.com"
a="http://"+b
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Quality"]
mycol = mydb[b]
load_time=[]
back_per=[]
front_per=[]
def searchCheck(c):
    try:
        base = driver.window_handles[0]
        driver.refresh()
        driver.execute_script("window.open('" + a +"');")
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        search=driver.find_element_by_xpath("//input[contains(@placeholder,'Search')]")
        search.send_keys("pen")
        search.send_keys(Keys.ENTER)
        c=c+1
        driver.close()
        driver.switch_to.window(base)
        return c
    except:
        return c
def loginCheck(c):
    if len(driver.find_elements("xpath", "//*[contains(text(),'Login')]"))>0:
        c=c+1
    elif len(driver.find_elements("xpath", "//*[contains(text(),'Log In')]"))>0:
        c=c+1
    elif len(driver.find_elements("xpath", "//*[contains(text(),'Log in')]"))>0:
        c=c+1
    elif len(driver.find_elements("xpath", "//*[contains(text(),'Sign in')]"))>0:
        c=c+1
    return c
def trackCheck(c):
    if len(driver.find_elements("xpath", "//*[contains(text(),'Track my order')]"))>0:
        c=c+1
    elif len(driver.find_elements("xpath", "//*[contains(text(),'Track your order')]"))>0:
        c=c+1
    return c
def getData():
    txt=driver.page_source
    txt=txt.lower()
    txt=re.sub('[\W]+', ' ', txt)
    mydict = { "data": txt }
    mycol.insert_one(mydict)
def loadTime(url):
    try:
        req=Request(url,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'})
        stream=urlopen(req)
        st=time()
        stream.read()
        et=time()
        t=et-st
        load_time.append(t)
    except Exception as e:
        print(str(e))
def responseTime():
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backendPerformance_calc = responseStart - navigationStart
    frontendPerformance_calc = domComplete - responseStart
    back_per.append(backendPerformance_calc)
    front_per.append(frontendPerformance_calc)
def getLinks():
    elems = driver.find_elements("tag name","a")
    for elem in elems:
                    x=elem.get_attribute("href")
                    if x!=None:
                            if c in x:
                                if x not in links:
                                    links.append(x)
                                else:
                                    continue
                    else :
                        continue
def scrape(url,t):
            try:
                base = driver.window_handles[0]
                driver.refresh()
                driver.execute_script("window.open('" + url +"');")
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)
                getData()
                if len(driver.find_elements("xpath", "//*[(text()='Add to bag')]"))>0:
                    txt=driver.find_element_by_xpath("/html/body").text
                    txt=txt.lower()
                    mydict = { "data": txt,"type":"product" }
                    mycol.insert_one(mydict)
                    if (t<1):
                         getLinks()
                    t=t+1
                elif len(driver.find_elements("xpath", "//*[(text()='Buy Now')]"))>0:
                    txt=driver.find_element_by_xpath("/html/body").text
                    txt=txt.lower()
                    mydict = { "data": txt,"type":"product" }
                    mycol.insert_one(mydict)
                    if (t<1):
                         getLinks()
                    t=t+1
                elif len(driver.find_elements("xpath", "//*[(text()='Add to cart')]"))>0:
                        txt=driver.find_element_by_xpath("/html/body").text
                        txt=txt.lower()
                        mydict = { "data": txt,"type":"product" }
                        mycol.insert_one(mydict)
                        if (t<1):
                                getLinks()
                        t=t+1
                elif len(driver.find_elements("xpath", "//*[(text()='Add to Cart')]"))>0:
                    txt=driver.find_element_by_xpath("/html/body").text
                    txt=txt.lower()
                    mydict = { "data": txt,"type":"product" }
                    mycol.insert_one(mydict)
                    if (t<1):
                         getLinks()
                    t=t+1
                elif len(driver.find_elements("xpath", "//*[(text()='BUY NOW')]"))>0:
                    txt=driver.find_element_by_xpath("/html/body").text
                    txt=txt.lower()
                    mydict = { "data": txt,"type":"product" }
                    mycol.insert_one(mydict)
                    if (t<1):
                         getLinks()
                    t=t+1
                elif len(driver.find_elements("xpath", "//*[(text()='ADD TO CART')]"))>0:
                    txt=driver.find_element_by_xpath("/html/body").text
                    txt=txt.lower()
                    mydict = { "data": txt,"type":"product" }
                    mycol.insert_one(mydict)
                    if (t<1):
                         getLinks()
                    t=t+1
                else: 
                    getLinks()
                loadTime(a)
                responseTime()
                driver.close()
                driver.switch_to.window(base)
                return t
            except StaleElementReferenceException as e1:
                print(e1)
                pass
PATH="C:\Program Files\chromedriver.exe"
driver=webdriver.Chrome(PATH)
driver.get(a)
driver.maximize_window()
driver.refresh()
c=driver.current_url
count=0
if "https" in c:
    count=count+1
test=0
getData()
if len(driver.find_elements("xpath", "//*[(text()='Add to bag')]"))>0 :
                        test=test+1
elif len(driver.find_elements("xpath", "//*[(text()='Buy Now')]"))>0:
    test=test+1
elif len(driver.find_elements("xpath", "//*[(text()='Add to cart')]"))>0:
    test=test+1
elif len(driver.find_elements("xpath", "//*[(text()='Add to Cart')]"))>0:
    test=test+1
elif len(driver.find_elements("xpath", "//*[(text()='BUY NOW')]"))>0:
    test=test+1
elif len(driver.find_elements("xpath", "//*[(text()='ADD TO CART')]"))>0:
    test=test+1
getLinks()
loadTime(a)
responseTime()
#feature=0
count=searchCheck(count)
count=loginCheck(count)
count=trackCheck(count)
l=0
j=0
while(1):
    print(len(links))
    for i in range(j,len(links)):
        print(i)   
        test=scrape(links[i],test)
        l=l+1
    if(l<len(links)):
        j=l
    else:
        driver.quit()
        print("done")
        break
criteria={1:["faq","help"], 2:["live chat","message","inbox","chat"],
3:["helpline","contact us"], 4:["privacy policy"],
5:["refund policy","replacement"],
6:["how to order","order process"],7:["terms of use","terms of services","terms conditions"]}
criteria2={1:["rating","review"],
2:["description", "specification","details"],}
t1=0
for key,values in criteria.items():
    for value in values:
        myquery = { "data": { "$regex": value } }
        mydoc = mycol.find(myquery)
        for x in mydoc:
            count=count+1
            t1=1
            break
        if(t1==1):
            t1=0
            break
t2=0
for key,values in criteria2.items():
    for value in values:
        myquery = { "data": { "$regex": value },"type":"product"}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(value)
            count=count+1
            t2=1
            break
        if(t2==1):
            t2=0
            break
load=sum(load_time)/len(load_time)
backend=sum(back_per)/len(back_per)
frontend=sum(front_per)/len(front_per)
print(load,count,backend,frontend)
mycol.drop()
result1=(count*70)/13
result2=max(10-load,0)
result3=max(10-backend/1000,0)
result4=max(10-frontend/1000,0)
result=result1+result2+result3+result4
print(result1,result2,result3,result4,result)