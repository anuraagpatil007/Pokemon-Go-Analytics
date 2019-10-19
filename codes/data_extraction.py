import os
from datetime import datetime
from bs4 import BeautifulSoup # web scraping
import urllib
import pickle # for serialization and desearlization 
import json


data = {}

folders = os.listdir('C:\UTA\Data Science\Project2\pokemon_5378\data')
error_a_avg_rating = []
error_a_total_ratings = []
error_a_3_rating = []
error_a_2_rating = []
error_a_1_rating = []
error_a_size = []
error_android_read =[]

error_ios_crate =[]
error_ios_trate = []
error_ios_size = []
error_ios_read = []


ios_crate =0    
ios_trate =0
ios_size=0
a_avg_rating =0
a_total_ratings =0 
a_1_rating =0
a_2_rating =0
a_3_rating =0
a_size = 0

for folder in folders:
    print '{} - Start'.format(folder)    
    filenames = os.listdir('C:\UTA\Data Science\Project2\pokemon_5378\data\{}'.format(folder))
    year = int(folder.split('-')[0])
    month = int(folder.split('-')[1])
    day = int(folder.split('-')[2])
#    print year, month, date
    
    for files in filenames:
        hour = int(files[:6].split('_')[0])
        mins = int(files[:6].split('_')[1])
        
        if files.endswith('android.html'):
            try:            
                r = urllib.urlopen('file:///C:/UTA/Data%20Science/Project2/pokemon_5378/data/{}/{}'.format(folder,files)).read()
                soup = BeautifulSoup(r, "lxml")
                try:
                    a_avg_rate = soup.find("div", {"class": "score"})
                    a_avg_rating =  float(a_avg_rate.get_text())
                except:
                    error_a_avg_rating.append('{}/{}'.format(folder,files))
                    a_avg_rating= 0
                try:
                    a_total_rate = soup.find("span", {"class": "reviews-num"})
                    if a_total_rate == None:
                        a_total_rate = soup.find("div", {"class": "stars-count"})
                        a_total_ratings = int(a_total_rate.get_text()[2:-2].replace(',' , ''))
                    else:
                        a_total_ratings = int(a_total_rate.get_text().replace(',' , ''))
                except:
                    error_a_total_ratings.append('{}/{}'.format(folder,files))
                    a_total_ratings =0
                
                try:
                    a_3_rate = soup.find("div",{"class" : "rating-bar-container three"})
                    a_3_rating =int(a_3_rate.get_text().split()[1].replace(',',''))
                except:
                    error_a_3_rating.append('{}/{}'.format(folder,files))
                    a_3_rating = 0
                try:
                    a_2_rate = soup.find("div",{"class" : "rating-bar-container two"})
                    a_2_rating =int(a_2_rate.get_text().split()[1].replace(',',''))
                except:
                    error_a_2_rating.append('{}/{}'.format(folder,files))
                    a_2_rating = 0
                try:
                    a_1_rate = soup.find("div",{"class" : "rating-bar-container one"})
                    a_1_rating =int(a_1_rate.get_text().split()[1].replace(',',''))
                except:
                    error_a_1_rating.append('{}/{}'.format(folder,files))
                    a_1_rating =0
                try:
                    a_filesize = soup.find("div", {"class":"content","itemprop":"fileSize"})
                    a_size = float(a_filesize.get_text().strip()[:-1])
                except:
                error_a_size.append('{}/{}'.format(folder,files))
                    a_size=0
            except:
                error_android_read.append('{}/{}'.format(folder,files))
                print "Error in file {}/{} #{}".format(folder,files,len(error_android_read))                
            
          if files.endswith('ios.html'): 
            try:
                s = urllib.urlopen('file:///C:/UTA/Data%20Science/Project2/pokemon_5378/data/{}/{}'.format(folder,files)).read()
                soup1 = BeautifulSoup(s, "lxml")
                
                try:
                    ios_rate = soup1.find_all("span",{"class":"rating-count"})
    
                    if len(ios_rate) ==1:
                        ios_crate =0
                        error_ios_crate.append('{}/{}'.format(folder,files))
                        ios_trate = int(ios_rate[0].get_text().split()[0])
                    else:
                        ios_crate = int(ios_rate[0].get_text().split()[0])
                        ios_trate = int(ios_rate[1].get_text().split()[0])
                except:
                    error_ios_crate.append('{}/{}'.format(folder,files))
                    error_ios_trate.append('{}/{}'.format(folder,files))
                try:  
                    ios_filesize = soup1.find("ul", {"class":"list"})
                    ios_size = float(ios_filesize.find_all("li")[4].get_text().split()[1])
                except:
                    error_ios_size.append('{}/{}'.format(folder,files))
                    ios_size = 0
            except:
                error_ios_read.append('{}/{}'.format(folder,files))
                print "Error in file {}/{} #{}".format(folder,files,len(error_ios_read))                  
        
        data[datetime(year,month,day,hour,mins,0)] = {
                        'ios_current_ratings': ios_crate , 
                        'ios_all_ratings':ios_trate, 
                        'ios_file_size': ios_size, 
                        'android_avg_rating':a_avg_rating, 
                        'android_total_ratings': a_total_ratings, 
                        'android_rating_1': a_1_rating, 
                        'android_rating_2': a_2_rating, 
                        'android_rating_3': a_3_rating, 
                        'android_rating_4': a_4_rating, 
                        'android_rating_5': a_5_rating, 
                        'android_file_size': a_size
                        }
                        
    print '{} - End'.format(folder)  

               
error_list = {
'error_a_avg_rating' :error_a_avg_rating,
'error_a_total_ratings':error_a_total_ratings,
'error_a_3_rating':error_a_3_rating,
'error_a_2_rating' :error_a_2_rating,
'error_a_1_rating':error_a_1_rating,
'error_a_size':error_a_size,
'error_android_read':error_android_read,
'error_ios_crate':error_ios_crate,
'error_ios_trate':error_ios_trate,
'error_ios_size' :error_ios_size,
'error_ios_read':error_ios_read,
'Total_error_a_avg_rating' :len(error_a_avg_rating),
'Total_error_a_total_ratings':len(error_a_total_ratings),
'Total_error_a_3_rating':len(error_a_3_rating),
'Total_error_a_2_rating' :len(error_a_2_rating),
'Total_error_a_1_rating':len(error_a_1_rating),
'Total_error_a_size':len(error_a_size),
'Total_error_android_read':len(error_android_read),
'Total_error_ios_crate':len(error_ios_crate),
'Total_error_ios_trate':len(error_ios_trate),
'Total_error_ios_size' :len(error_ios_size),
'Total_error_ios_read':len(error_ios_read)
}
with open('data.pickle','w') as f:
    pickle.dump(data,f)
    
with open('error.json','w') as f:
    json.dump(error_list, f, indent =4)
