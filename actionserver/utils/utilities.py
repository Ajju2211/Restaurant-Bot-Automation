from datetime import datetime
import json
def timestamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestampStr
def getJsonFileAsDict(filePath):
    with open(filePath,"r") as f:
        return json.load(f)
def saveDictAsJsonFile(dictData,filePath):
    with open("./../"+filePath,"w") as f:
        json.dump(dictData,f,indent = 4)
        return True

        
def dish_info(dish_name, category):
    with open(r'.\actionserver\custom_payload.json') as f:
        restaurant_menu =   json.load(f)
    
    menu = restaurant_menu['restaurant']['menu']
    if menu[category]:
        temp = menu[category]
        for j in temp:
            if dish_name.lower() == j['dish'].lower():
                return {"dish":j['dish'],"price":j['price'],"image":j['image']}
        return {"none":-1}
    return {"none":-1}
    

    
    
    

