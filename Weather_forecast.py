from tkinter import *
from tkinter.font import Font
import time, json
from turtle import pen
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
writeAPI = "GNA7DDFVJA5H8SKJ" 
readAPI = "D2BEZ1ITTWV3RFPS"
def getInput(str1):
    s1 = str1.get()
    if s1 == '': 
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Please enter the strings").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()  
    elif not(s1.isalpha()):
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Input should be Strings only.").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    else:
        display(s1.lower())
        

def main():
    baseURL = ('https://api.thingspeak.com/update?api_key=GNA7DDFVJA5H8SKJ')
    data = [(33,16)]
    for d in data:
        f = urlopen(baseURL +"&field1=%s&field2=%s" %d)
        f.close()
        time.sleep(15)

def read():
    baseURL = ("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                        % (1699259,'D2BEZ1ITTWV3RFPS'))
    f = urlopen(baseURL)
    data = json.loads(f.read().decode())
    Temp = []
    Hum = []
    f.close()
    for d in data["field1"]:
        Temp.append(d)
    for d2 in data["field2"]:
        Hum.append(d2)
    return Temp, Hum
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    Temp = soup.select('#wob_tm')[0].getText().strip()
    humidity = soup.select('#wob_hm')[0].getText().strip()
    precipitation = soup.select('#wob_pp')[0].getText().strip()
    wind = soup.select('#wob_ws')[0].getText().strip()
    
    return time,Temp,humidity,info,precipitation,wind

def instructions():
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)
    background.create_text(w/2, h/2 - 375, text = "Team - 13", font = headingFont)
    background.create_text(w/2, h/2 - 325, text = "Weather forecast", font = headingFont)
    background.create_text(w/2, h/2 - 250, text = "Welcome ", font = headingFont)
    background.create_text(w/2 , h/2 - 200, text = "(Please read the following Instructions)", font = textFont)
    Inst = '''
            1. To know your current location weather please Type 'current' in the given box and press Enter.
            2. To know the weather of a specific location please type the location name in the box and press Enter.
            3. To Predict the weather of the location please re enter the location and  click on the predict.
            4. Click on the Next to go the weather forecast window.
            5. If you want to QUit click on the Quit button which is on the to right corner
            '''
    background.create_text(w/2- 630 , h/2 -75, text = "Instructions:", font = headingFont)
    background.create_text(w/2- 300 , h/2 + 25, text = Inst, font = textFont)
    b =  Button(background, text = "Next", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:inputScreen())
    background.create_window(w/2 , h/2 + 200, window = b, width = w/8)

def inputScreen():
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.update()
    background.grid(row=0, column=0)
    background.create_text(w/2, h/2 - 375, text = "Team - 13", font = headingFont)
    background.create_text(w/2, h/2 - 300, text = "Weather forecast", font = headingFont)
    
    background.create_text(w/2 - 310, h/2 - 100, text = "Enter your Location: ", font = textFont)
    str1 =Entry(background)
    background.create_window(w/2 , h/2 - 100, window = str1, width = w/4)
    
    b1 = Button(background, text = "Enter", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:getInput(str1))
    background.create_window(w/2 + 300  , h/2 - 100, window = b1, width = w/8)
    b2 = Button(background, text = "QUIT", bg = '#FF0000', activebackground = '#FFE5CC', command=lambda:root.destroy())
    background.create_window(w/2 + 650, h/2 -400, window = b2, width = w/8)
    b3 = Button(background, text = "Predict", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:prediction(str1))
    background.create_window(w/2 , h/2 +200, window = b3, width = w/8)
    return background

def display(string):
    background = inputScreen()
    if string == "current":
        background.create_text(w/2 , h/2 - 30, text = "The weather of your  " + string  + " Location is:", font = textFont)
        main()
        Temp, Hum = read()
        background.create_text(w/2 , h/2 , text = ["Temperature is "] + Temp + ["°C"], font = smallTextFont)
        background.create_text(w/2 , h/2 + 25 , text = ["Humidity is "] + Hum + ["%"], font = smallTextFont)
    else:
        background.create_text(w/2 , h/2 - 30, text = "The Weather of " + string  + " is:", font = textFont)
        string = string+" weather"
        time,Temp,humidity,info,precipitation,wind, = weather(string)
    background.create_text(w/2 , h/2 , text = "The Time is "+ time , font = smallTextFont)
    background.create_text(w/2 , h/2 + 25 , text = "Temperature is "+Temp +"°C" , font = smallTextFont)
    background.create_text(w/2 , h/2 + 50, text = "humidity is "+humidity , font = smallTextFont)
    background.create_text(w/2 , h/2 + 75, text = "The Sky is " + info , font = smallTextFont)
    background.create_text(w/2 , h/2 + 100, text = "The precipitation is " + precipitation , font = smallTextFont)
    background.create_text(w/2 , h/2 + 125, text = "Wind speed is " + wind , font = smallTextFont)
    if Temp > '35':
        background.create_text(w/2 + 450 , h/2 +50 , text = "The Temperature is high Take care if you planned to go out" , font = smallTextFont)
    if Temp < '35' and humidity < '60%' and info == 'Clear':
        background.create_text(w/2 + 450 , h/2 +50 , text = "This is the best weather to plan a trip" , font = smallTextFont)

def prediction(string):
    background = inputScreen()
    dataset = pd.read_csv("weather.csv")
    dataset.loc[dataset['RainToday']=='Yes','RainToday']=1
    dataset.loc[dataset['RainToday']=='No','RainToday']=0
    dataset['RainToday'] = dataset['RainToday'].astype(int, errors = 'raise')
    Y1 = dataset.MaxTemp.values
    X1 = dataset.drop(['MaxTemp','RainToday'], axis = 1)
    print(X1)
    X1_train, X1_test, Y1_train, Y1_test = train_test_split( X1, Y1, test_size = 0.2, random_state = 0 )
    regressor = LinearRegression()
    regressor.fit(X1_train, Y1_train)
    string = string.get()
    string = string+" weather"
    time,Temp1,humidity1,info,precipitation1,wind1, = weather(string)
    temp = int(Temp1)
    prep = int(precipitation1[:-1])
    windspeed = int(wind1[:-4])
    hum = int(humidity1[:-1])
    custom_data=np.array([[temp,prep,windspeed,hum]])
    print(custom_data)
    max_temp = regressor.predict(custom_data)
    
    Y2 = dataset.RainToday.values
    X2 = dataset.drop(['RainToday'], axis = 1)
    print(X2)
    X2_train, X2_test, Y2_train, Y2_test = train_test_split( X2, Y2, test_size = 0.2, random_state = 0 )
    regressor = LinearRegression()
    regressor.fit(X2_train, Y2_train) 
    rain_data = np.array([[temp,max_temp,prep,windspeed,hum]]) 
    y1_pred = regressor.predict(rain_data)
    if y1_pred >0.5:
        statement = "Rain fall may occur"
    else:
        statement = "There are no chances of rain"
    background.create_text(w/2 + 450 , h/2 + 75, text = "The prediction of " +  string + " is:" , font = smallTextFont)
    background.create_text(w/2 + 450 , h/2 + 125, text = "The max temperature will be " +  str( max_temp) + "°C" , font = smallTextFont)
    background.create_text(w/2 + 450 , h/2 + 175, text = statement , font = smallTextFont)



if __name__ == "__main__":
    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    root.title("Weather forecast")
    smallTextFont = Font(family = 'Bookman Old Style', size = '12')
    textFont = Font(family = 'Bookman Old Style', size = '15')
    headingFont = Font(family = 'Bookman Old Style', size = '30')
    instructions()
    root.mainloop()
