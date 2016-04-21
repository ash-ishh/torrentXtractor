#!/usr/bin/python3
# Author: Ash-Ishh..
# <mr.akc@outlook.com>
# Modules Required:
# requests
# pip install requests
# beautifulSoup4: https://pypi.python.org/pypi/beautifulsoup4/4.3.2
# pip install BeautifulSoup4


import requests
from bs4 import BeautifulSoup
import re
import sys,os
import webbrowser
#import sl4a

try:
    os.system("color 0A")
except:
    pass
   
   
print("torrentXtractor V2.0".center(50, '-'))
print("\n\nRequirments : You need to install torrent client (e.g : uTorrent , BitTorrent etc) If it is already installed you are good to go.\n\n")


options = "* Enter the Token Number to download.\n* Enter 'N' to navigate to another page.\n* Enter 'S' to change torrent site. \n* Enter 'Yo' to search Another Torrent.\n* Enter 'Q' to exit.\n>> "
#droid = sl4a.Android()
 
def printAvailableTorrents(functionPageNo,functionTitles,functionSeeders,functionLeechers,functionSizes):
    print("Page Number : ",str(functionPageNo))
    for i,(title,seeder,leecher,size) in enumerate(zip(functionTitles,functionSeeders,functionLeechers,functionSizes)):          
        print('\n'+ "x."*30)         
        print("Token Number : " + str(i+1))
        print( (title.encode('ascii','replace')).decode())
        print("Seeders : " + seeder)
        print("Leechers : " + leecher)
        print("Size :" + size)
        print("x."*30 + '\n')
   
def performAction(functionActionVar):
    if functionActionVar == 'Q': #quit
        sys.exit()        
    elif functionActionVar == 'S':
        selectService()
        print('\n'*30)   
    elif functionActionVar == 'YO': #take new query
        print('\n'*30)
        start()


def performNewAction():
    newAction = input("\n\n* Successfully Added to your Downloads :) (Check out your torrent client)\n\n* To Search Another Torrent Enter 'Yo'.\n* To quit enter 'Q'.\n\n>> ").upper()
    if newAction == 'YO':
        start()
    elif newAction == 'Q':
         sys.exit() 
    else:
         start()                   
            	         

def start():
    global query
    query = input("Enter Your Query :\n>> ")
    selectService()
    
def selectService():
    #Options : 1-1337x 2-KickAss
    service = input("\nSelect Torrent Site :\nEnter 1 for - 1337x\nEnter 2 for - Kick Ass Torrent\n>> ")
    if service == '1':
        start1337x(query,1) #second argument = initial page number 1.
    elif service == '2':
        startKat(query,1)
    else:
        print(".\n.\n.\nEnter Vaild Option :(\n")
        selectService()




#### 1337x ####
def start1337x(query0,pageNo):
    print("1337x\n")
    url = 'http://1337x.to'
    query0 = query0.replace(' ','+').lower()
    finalUrl = url + '/search/' + query0 + '/'+str(pageNo)+'/'
    #if query = game of thrones
    #than finalUrl = http://1337x.to/search/game+of+thrones/1/
    
    try:
        req = requests.get(finalUrl)
        soup = BeautifulSoup(req.content,'html.parser')
        #Beautifulsoup object of the whole html page in variable soup.
        
        div1 = soup.find_all('div',{'class':'coll-1'})
        #Div1 contains Title And Magnet Link in it
        
        titles = [t.get_text() for t in div1]
        links = [k['href'] for i in div1 for j in i.find_all('strong') for k in j.find_all('a')]
        #Links are in <div1> --> <strong> --> <a href='..'>
        
        seeders = [s.get_text() for s in soup.find_all('div',{'class':'coll-2'})]
        leechers = [l.get_text() for l in soup.find_all('div',{'class':'coll-3'})]
        sizes = [size.get_text() for size in soup.find_all('div',{'class':'coll-4'})]        
        # seederd are in <div class=coll-2>
        # leechers are in <div class=coll-2>
        # size is in <div class=coll-2>

        if len(titles) == 0:
            print("No Result Found :(\nTry Again!\n")
            start()
  
        printAvailableTorrents(pageNo,titles,seeders,leechers,sizes)   
        action = input(options).upper()     
        performAction(action)
        
        if action == 'N': #navigate
            pageNo = input("Enter Page Number: \n>> ")
            print('\n'*30)
            start1337x(query0,pageNo)                        
        
        else: #download part
            try:
               action = int(action)
            except:
               print('\n'*30)
               print("Enter Vaild Option!!!!")
               start1337x(query,pageNo)
     
            selectedTorrent = url + links[action-1]
            dwnldReq = requests.get(selectedTorrent)
            dwnldSoup = BeautifulSoup(dwnldReq.content,'html.parser')
            magnet = [i['href'] for i in dwnldSoup.find_all('a',{'class':'magnet'})]
            webbrowser.open(magnet[0])
            #droid.setClipboard(magnet[0])     
           
            performNewAction()          
    except Exception as e:
        print("Error! !_!")
        print(str(e))
        print("Try Again..")
        start()
        
                     
        
        
### kat.cr ###    
def startKat(query0,pageNo):
    print("KICK-ASS-T0RRENTS\n")
    url = 'http://kat.cr/usearch/' 
   # query0 = query0.replace(' ','%20')
    finalUrl = url + query0 + '/' + str(pageNo) + '/'

    
    try:
        req = requests.get(finalUrl)
        soup = BeautifulSoup(req.content,"html.parser")

        magnetRegex = re.compile(r"'magnet': '(magnet:\?.*?)'",re.DOTALL)
        magnet = magnetRegex.findall(str(soup.prettify))
        titles = [ti.get_text() for ti in soup.find_all('a', {'class':'cellMainLink'})]
        centerClass = [s.get_text() for s in soup.find_all('td', {'class':'center'})]
        sizes = [t.get_text() for t in soup.find_all('td', {'class':'nobr'}) ]
        seeders = centerClass[3::5]
        leechers = centerClass[4::5]
        
        if len(titles) == 0:
            print("No Result Found :(\nTry Again!\n")
            start()
        
        printAvailableTorrents(pageNo,titles,seeders,leechers,sizes)

        action = input(options).upper()
     
        performAction(action)
       
        if action == 'N': #navigate
            pageNo = input("Enter Page Number: \n>> ")
            print('\n'*30)
            startKat(query,pageNo)           
        
        else: #download part
            try:
               action = int(action)
            except:
               print('\n'*30)
               print("Enter Vaild Option!!!!")
               startKat(query0,pageNo)
            webbrowser.open(magnet[action-1])
            #droid.setClipboard(magnet[action])       
         
            performNewAction()
     
    except Exception as e:
        print("Error! !_!")
        print(str(e))
        print("Try Again..")
        start()
        

if __name__ == '__main__':
    start()
