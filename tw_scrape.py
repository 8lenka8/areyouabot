import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def tw_extract_d(twitter_url,un,pw,scrolls):

    o = webdriver.ChromeOptions()
    o.add_argument('headless')
    o.add_argument('log-level=3')
    w = webdriver.Chrome(chrome_options=o)

    w.get(twitter_url)
    w.execute_script('document.getElementsByName(\'session[username_or_email]\')[1].setAttribute(\'value\',\''+ un +'\')')
    w.execute_script('document.getElementsByName(\'session[password]\')[1].setAttribute(\'value\',\''+ pw +'\')')
    sleep(1)
    w.execute_script('document.getElementsByClassName(\'submit EdgeButton EdgeButton--primary EdgeButtom--medium\')[0].click()')
    
    print('scraping ' + twitter_url)

    count = scrolls
    while count !=0:
        w.execute_script("window.scrollBy(0,100000)")
        sleep(0.5)
        count = count-1

    x = w.find_elements_by_class_name('ProfileCard')

    print('extracting data')

    accounts_d = pd.DataFrame({'name':[],'screen_name':[],'bio':[],'protected':[],'emoji':[]})

    for i in range(len(x)):
            
        d = pd.DataFrame({'name':[x[i].find_element_by_class_name('ProfileNameTruncated').text]})
        d['screen_name'] = x[i].find_element_by_class_name('ProfileCard-screenname').text
        d['bio'] = x[i].find_element_by_class_name('ProfileCard-bio').text
        
        if len(x[i].find_elements_by_class_name('Icon--protected')) > 0:
            d['protected'] = 'True'
        else:
            d['protected'] = 'False'

        try:
            emojis = x[i].find_elements_by_class_name('Emoji')
            e_list = []    
            for e in emojis:
                e_list.append(e.get_attribute('title'))
            d['emoji'] = str(e_list)
        except:
            d['emoji'] = 'no emojis'
        
        accounts_d = accounts_d.append(d)

    return accounts_d