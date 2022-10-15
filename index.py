from flask import Response, Flask, request, current_app as app, jsonify
import requests
import json
import re
import os
import urllib
import socket
from threading import Thread
import sys
import os




import os
dirname, filename = os.path.split(os.path.abspath(__file__))
#print(dirname)
#exit()
errorText="Error In Parsing"
gCityID="1275339"
gAppID="15373f8c0b06b6e66e6372db065c4e46"
filename=os.path.join(dirname,'temp.json')
deviceConfigFileName=os.path.join(dirname,"remoteDeviceConfig.json")
deviceConFigJSON=None
pingPongDeviceName='ping-pong'


app = Flask(__name__,  static_url_path='/static')


#print($apiResponse);

@app.route("/")
def indexPage():       	
        return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)




	

@app.route("/humidity")
def getHumidity():       
        
        requestURL="http://api.openweathermap.org/data/2.5/weather?id="+gCityID+"&appid="+gAppID        

       
        try:        
                response = download_file(requestURL, filename)
                return getData("main.humidity")
        except:
                return errorText
    
@app.route("/temperature")
def getTemperature():        

        requestURL="http://api.openweathermap.org/data/2.5/weather?id="+gCityID+"&appid="+gAppID        

       
        try:        
                response = download_file(requestURL, filename)
                temperatureK=getData("main.temp")                
                temperatureC=int(round(float(temperatureK)-273.15,0))
                
                return str(temperatureC)
                
        except:
                return errorText

@app.route("/weatherDescription")
def getWeatherDescription():
                
        requestURL="http://api.openweathermap.org/data/2.5/weather?id="+gCityID+"&appid="+gAppID        

       
        try:        
                response = download_file(requestURL, filename)
                return getData("weather.main")
        except:
                return errorText
				
@app.route("/forecast")
def getForecast():
        requestURL="http://api.openweathermap.org/data/2.5/forecast/daily?id="+gCityID+"&appid="+gAppID
        #try:
        #response = download_file(requestURL, filename)
        #return getData("")
        #except:
        #       return errorText

        r = requests.get(requestURL, stream=True)
        return r.content


@app.route("/news")
def getRSSNews():
        requestURL="http://www.macmillandictionary.com/potw/potwrss.xml"
        headers = {'user-agent': 'my-app/0.0.1'}
        r = requests.get(requestURL, stream=True,headers=headers)
        return r.content

""" @app.route("/hasPingPongEnumerated")
def hasPingPongEnumerated():
        ipinJSON, portinJSON,foundAtIndex=getDeviceIPandPort(pingPongDeviceName)
        requestURL="http://"+ipinJSON
        successJsonString={"connection":"true", "ip":ipinJSON, "port":portinJSON}
        failureJsonString={"connection":"false", "ip":"0.0.0.0", "port":"80"}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
                r = requests.get(requestURL,timeout=2) # set timeout to 2 seconds
                return jsonify(successJsonString) 
        except requests.exceptions.RequestException as e:  # This is the correct syntax
                return jsonify(failureJsonString)   """
        

        
                
        
def getData(jsontree):
    with open(filename) as data_file:    
        data = json.load(data_file)
    splittree=jsontree.split(".")    
    lastLeafIndex = len(splittree) - 1
    #jsontree="main.temp"
    
    for i, leaf in enumerate(splittree):
        if i == lastLeafIndex:
            continue
        else:
           leafDataIndex=0
           result =  re.findall(r'\[([^]]*)\]', leaf)
           if result:
              leafDataIndex=result[0]
              leaf=leaf.replace("["+leafDataIndex+"]","")
              leafDataIndex=int(leafDataIndex)
        
        try:        
            data=data[leaf][leafDataIndex]
        except(KeyError):
           try: 
               data=data[leaf]
           except (KeyError):
               return "Error"
               exit()

    leaf=splittree[lastLeafIndex]
    leafDataIndex=0
    result =  re.findall(r'\[([^]]*)\]', leaf)
    if result:
        leafDataIndex=result[0]
        leaf=leaf.replace("["+leafDataIndex+"]","")
        leafDataIndex=int(leafDataIndex)
        return (data[leaf][leafDataIndex])
    else:
       return str(data[leaf])  

        
def getDataList(jsontree):    
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data 

        

  
def download_file(url,filename):
    local_filename = filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)                
    return True

def getDeviceConfigJSON():
        with open(deviceConfigFileName, 'r') as infile:
                deviceConFigJSON = json.load(infile)
        return deviceConFigJSON

def saveDeviceConfigJSON(JSONObject):
        with open(deviceConfigFileName, "w") as outfile:
            json.dump(JSONObject,outfile)

def getDeviceIPandPort(deviceName):
        deviceJSON=getDeviceConfigJSON()
        index=0
        for device in deviceJSON["remoteDeviceConfig"]:
                #print(device)
                
                nameFound=device.get("name", None)
                #print(nameFound)
                if (nameFound is not None and nameFound==deviceName):
                        return device.get("ip"), device.get("port", None), index
                index=index+1
        return None,None,-1

def saveDeviceJSON(deviceJSONObject):
        deviceJSONFromFile=getDeviceConfigJSON()
        
        deviceName=deviceJSONObject.get("name","Default")
        deviceIP=deviceJSONObject.get("ip","127.0.0.1")
        devicePort=deviceJSONObject.get("port",80)
        
        ipinJSON, portinJSON,foundAtIndex=getDeviceIPandPort(deviceName)
        #print("ipinJSON: " +ipinJSON)
        #print("portinJSON: " +portinJSON)
        #print("foundAtIndex: " +str(foundAtIndex))
        if(foundAtIndex>-1): # remove the old config
            #print("Removing Old Config")
            #print (deviceJSONFromFile["remoteDeviceConfig"][foundAtIndex])
            del deviceJSONFromFile["remoteDeviceConfig"][foundAtIndex]
            print(deviceJSONFromFile)
        if(deviceJSONFromFile is not None):
                   deviceJSONFromFile["remoteDeviceConfig"].append(deviceJSONObject)
        saveDeviceConfigJSON(deviceJSONFromFile)           
        print("saved")
        
def recieveUDPForPingPong():
        print("Starting Thread")
        UDP_PORT = 8000
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('',UDP_PORT))
        
        while True:
            data, (ip,port) = sock.recvfrom(1024) # buffer size is 1024 bytes
            print ("received from:", ip)
            try:
                    jsonResponse=json.loads(data)                   
                    print ("received message:", jsonResponse)
                    print ("received from:", ip)
                    saveDeviceJSON(jsonResponse)
            except:        
                 print("Malformed JSON")   
            sys.exit()

if __name__ == "__main__":    
        #deviceConFigJSON=getDeviceConfigJSON()
       

        #recieveUDPForPingPong()
        port = int(os.environ.get("PORT", 8080))
        app.run(host='0.0.0.0', port=port, debug=True)
