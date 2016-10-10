#coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
import time
import urllib2
import json
import ConfigParser

#读取配置文件
config = ConfigParser.RawConfigParser()
config.read('conf.properties')

username =  config.get('userconf','username')
password = config.get('userconf','password')
timeout = config.get('userconf','timeout')
interval = config.get('userconf','interval')
bid_amount = config.get('userconf','bidamount')
isusecoupon = config.get('userconf','usecoupon')

print u'开始读取配置信息'
print u'用户名:' + username
print u'密码:' + password
print u'过期时间:' + timeout
print u'扫描间隔:' + interval
print u'投标金额:' + bid_amount


loadId = ''
coupon = ''
#循环获取标书列表，直到获取符合条件的标书（期限低于40天)
print u'开始扫描标书：'
got = False
while True:

    retJson = ''

    try:
        resp = urllib2.urlopen('http://m.gomefinance.com.cn/api/v4/product/index/productList?page=1&pageSize=3&type=DQ')
        retJson = json.loads(resp.read())
    except:
        retJson = ''
    
    if retJson != '':
        productList =  retJson['data']['product']
        print str(len(productList))

        #扫描前三条数据
        print u'最新三条定期标书信息'
        for i in range(3):

            loanId =  retJson['data']['product'][i]['id']
            days = retJson['data']['product'][i]['totalDays']
            title = retJson['data']['product'][i]['loanTitle']
            coupon = retJson['data']['product'][i]['useCoupon']
            print '\n'
            print 'loanId' + ':' +  loanId
            print 'days:' + str(days)
            print 'loadTitle:' + title
            print 'coupon:' + str(coupon)
            print '\n' 
    
            if days < 80:
                got = True
                print u'扫描到符合条件的标书，开始加载...'
                break
        if got:
            break
        print u'没有扫描到符合条件的标书，休眠...'
        time.sleep(int(interval))
                
    else:
        time.sleep(int(interval))
        print '加载列表失败'
        continue
    
print '\n'

browser = webdriver.Chrome()
browser.set_window_size(480, 800)


url = 'http://m.gomefinance.com.cn/loan/' + loanId + '/invest?go_back_path=list'

print url
browser.get(url)

WebDriverWait(browser, int(timeout)).until(lambda browser : browser.find_element_by_name("mobile")) 

print 'current_url:' + browser.current_url
browser.find_element_by_name('mobile').clear()
browser.find_element_by_name('mobile').send_keys(username)
browser.find_element_by_name('password').clear()
browser.find_element_by_name('password').send_keys(password)

loginBtn = WebDriverWait(browser,int(timeout)).until(lambda browser : browser.find_element_by_xpath('//*[@id="register"]/div[2]/form/div[4]/button[2]'))

time.sleep(2)
loginBtn.click()

print u'登录成功！'
#页面加载完成后 自动填写金额
print u'页面加载完成后 自动填写金额'
inverstBtn = WebDriverWait(browser,int(timeout)).until(lambda browser: browser.find_element_by_xpath('//*[@id="loan-invest"]/form/div[4]'))
amountInput = browser.find_element_by_xpath('//*[@id="loan-invest"]/form/div[1]/div[1]/div/span/input')
amountInput.send_keys(bid_amount)
time.sleep(1)

#可用红包
if isusecoupon == '1' and coupon:

    selBtn = browser.find_element_by_xpath('//*[@id="coupon"]')
    selBtn.click()
    couponDiv = WebDriverWait(browser,int(timeout)).until(lambda browser:browser.find_element_by_xpath('//*[@id="select_coupon"]/section/div/div/div[2]'))
    couponDiv.click()


#inverstBtn.click()
