#Group 12: Niranjan Naik, Anurag Patil, Dhaval Metre
#3.1 & 3.2 Code for scrapping the data and storing in dataframe.
from bs4 import BeautifulSoup
import pandas
import json
import os
import datetime
from lxml import html
#path

folder = r'C:\Users\anura\Desktop\DS\Project 2\data'
#dictionaries to store results to be stored in a json file finally
final=dict()
android_final=dict()
ios_final= dict()
ios_main = dict()
ios_sub = dict()
android_main = dict()
android_sub = dict()


android_final_Jsondump=dict()
ios_final_jsondump=dict()
final_jsondump=dict()
#lists to store data for visualizaiton

size=None
rating_5=None
rating_4=None
rating_3=None
rating_2=None
rating_1=None

outfile = open('data.json', 'w')

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

#looping through every folder, directory and file
for dirName, dirs, files in os.walk(folder):
    print("directory name---->>>>",dirName)

    for fileName in files:

        #filename_without_extension, extension = os.path.splitext(filename)
        if 'android' in fileName :
            print("inside android---->>>>",fileName)


            try:
                soup = BeautifulSoup (open(dirName + '/' + fileName),'lxml')
                metaInfo = soup.find_all("div", class_="meta-info")
                avg_Rating= soup.find("div", class_="score")
                avg_Rating=str(avg_Rating).split()[-1].split(r'>')[1].split(r'<')[0]
                total_Rating= soup.find("span", class_="reviews-num")
                total_Rating= str(total_Rating).split()[-1].split(r'>')[1].split(r'<')[0]
            except:
                if avg_Rating==None or avg_Rating<=0:
                    avg_Rating=0
                if total_Rating==None or total_Rating<=0:
                    total_Rating=0
                continue

            try:
                rating_five= soup.find_all("div", class_="rating-bar-container five")
                rating_four= soup.find_all("div", class_="rating-bar-container four")
                rating_three= soup.find_all("div", class_="rating-bar-container three")
                rating_two= soup.find_all("div", class_="rating-bar-container two")
                rating_one= soup.find_all("div", class_="rating-bar-container one")

                try:
                    for i in metaInfo:
                        m= i.find("div",class_="content",itemprop="fileSize")
                        mlable=i.find("div", class_="title")
                        mlable=str(mlable.get_text())

                        if mlable=="Size":
                           print("inside")
                           if m!=None:

                              size=(str(m)).split(r'>')[1].split(r'<')[0].strip()
                              size=size[:-1]
                              print(size)
                              break
                        else:
                            size=0

                except:
                      if size==None or size<0:
                         size=0
                         continue

                for i in rating_five:
                    rating_5= i.find("span",class_="bar-number")
                    if rating_5!=None:
                       rating_5=(str(rating_5)).split(r'>')[1].split(r'<')[0].strip()

                for i in rating_four:
                    rating_4= i.find("span",class_="bar-number")
                    if rating_4!=None:
                       rating_4=(str(rating_4)).split(r'>')[1].split(r'<')[0].strip()

                for i in rating_three:
                    rating_3= i.find("span", class_="bar-number")
                    if rating_3!=None:
                       rating_3=(str(rating_3)).split(r'>')[1].split(r'<')[0].strip()

                for i in rating_two:
                    rating_2= i.find("span", class_="bar-number")
                    if rating_2!=None:
                       rating_2=(str(rating_2)).split(r'>')[1].split(r'<')[0].strip()

                for i in rating_one:
                    rating_1= i.find("span", class_="bar-number")
                    if rating_1!=None:
                       rating_1=(str(rating_1)).split(r'>')[1].split(r'<')[0].strip()

            except:
                if rating_5==None or rating_5<=0:
                   rating_5=0
                if rating_4==None or rating_4<=0:
                    rating_4=0
                if rating_3==None or rating_3<=0:
                   rating_3=0
                if rating_2==None or rating_2<=1:
                    rating_2=0
                if rating_1==None or rating_1<=1:
                    rating_1=0
                continue

            android_sub = {'Android_Total_rating': total_Rating,\
                   'Android_Average_rating': avg_Rating,\
                   'Android_Rating_1': rating_1,\
                   'Android_Rating_2': rating_2,\
                   'Android_Rating_3': rating_3,\
                   'Android_Rating_4': rating_4,\
                   'Android_Rating_5': rating_5,\
                   'Android_File_size' : size}

            year=int(dirName.split("\\")[-1].split("-")[0])
            month=int(dirName.split("\\")[-1].split("-")[1])
            day=int(dirName.split("\\")[-1].split("-")[2] )
            hour=int(fileName.split('_')[0])
            Min=int(fileName.split('_')[1])
            sec=00
            dateTime=datetime.datetime(year,month,day,hour,Min,sec)

            #converting date to nanoseconds
            android_main = {unix_time_millis(dateTime): android_sub}
            android_final.update(android_main)

        if 'ios' in fileName:
            print("inside ios---->>>>",fileName)
            #creating a beautifule soup object for ios
            soup = BeautifulSoup(open(dirName + '/' + fileName), 'lxml')
            try:

                lableSize=soup.find_all('span',class_="label")
                lableSize= str (lableSize[3].get_text()).strip()

                if lableSize=='Size:':
                    size = soup.find_all('li')
                    ios_size=str(size[21].get_text()).split(" ")[1]
                else:
                    ios_size=0

                custr_rating = soup.find_all('span', {'class' : 'rating-count'})
                curr_ver_rating= str(custr_rating[0]).split(r'>')[1].split(r'<')[0][:-7]
                all_ver_rating= str(custr_rating[1]).split(r'>')[1].split(r'<')[0][:-7]


            except:
                if all_ver_rating==None or all_ver_rating<=0:
                    all_ver_rating=0

                if curr_ver_rating==None or curr_ver_rating<=0:
                   curr_ver_rating=0
                if ios_size==None or ios_size<=0:
                    ios_size=0
                continue
            #creating an intermediate dictionary
            ios_sub = {'ios_all_rating': all_ver_rating,\
                       'ios_current_rating': curr_ver_rating,\
                       'ios_File_size' : ios_size }

            year=int(dirName.split("\\")[-1].split("-")[0])
            month=int(dirName.split("\\")[-1].split("-")[1])
            day=int(dirName.split("\\")[-1].split("-")[2] )
            hour=int(fileName.split('_')[0])
            Min=int(fileName.split('_')[1])
            sec=00
            #dateTime=year+ "," +month +"," +day + ","+hour+","+min+","+sec
            dateTime=datetime.datetime(year,month,day,hour,Min,sec)
            print unix_time_millis(dateTime)
            ios_main = {unix_time_millis(dateTime): ios_sub}
            ios_final.update(ios_main)






#merging two child dictioneries based on the parent key
def mergDictionaries(android_final,ios_final):
    for i in android_final:
        for j in ios_final:
             if i==j:
                final[i]={}
                for idItemA in android_final[i]:
                     final[i][idItemA]=android_final[i][idItemA]

                for idItemB in ios_final[j]:
                   final[i][idItemB]=ios_final[j][idItemB]

    return final


final=mergDictionaries(android_final,ios_final)




from pandas import ExcelWriter
df =pandas.DataFrame.from_dict(final, orient='index')
df.to_csv('data.csv', header=True, index=True, index_label='datetime', encoding='utf-8')
writer = ExcelWriter('data.xlsx')
df.to_excel(writer, sheet_name='PokemonGoAnalysisData',header=True, index=True, index_label='datetime')
writer.save()

#dumping the dictionary in the json file
json.dump(final, outfile)
