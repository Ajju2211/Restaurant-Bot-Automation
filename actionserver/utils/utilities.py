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
        
    

    
    
    

