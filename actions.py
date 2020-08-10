from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import AllSlotsReset, SlotSet
import pandas as pd
from rasa.core.slots import Slot
dataset= pd.read_csv('dishes.csv')
dataset=dataset.set_index('dish').T.to_dict('list')

class InfoForm(FormAction):
    """Collects order information"""

    def name(self):
        return "info_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "username",
            "mailid",
            "phone_number",

            ]

    @staticmethod
    def msg() -> List[Text]:
        return ["back1","back2","back3"]

    def validate_mailid(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() not in self.msg():
            return {"mailid": value}
        else:
            return {"mailid": None, "username": None}

    def validate_phone_number(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() not in self.msg():
            return {"phone_number": value}
        else:
            return {"phone_number": None,"mailid": None}

    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        username = tracker.get_slot("username")
        mailid = tracker.get_slot("mailid")
        phone_number=tracker.get_slot("phone_number")
        
        
       
        message="DETAILS:"+"\n\n"+"Name:"+username+"\n"+"Email:"+mailid+"\n"+"Phone Number:"+phone_number+"\n"+"\nThanks! for sharing information." 
        saveFile = open("some.txt", 'a')
        saveFile.write(message)
        saveFile.close()
        dispatcher.utter_message(message)
        return []
        
class OrderForm(FormAction):

    def name(self):
        return "order_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "dish_name",
            "proceed",
            ]
    def validate_dish_name(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        dish_name=tracker.get_slot("dish_name")
        
        if dish_name in dataset.keys(): 
            
            return {"dish_name":value}
        else:
            dispatcher.utter_template("utter_not_serving",tracker)
            return {"dish_name":None}
    
    def validate_proceed(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        dish_list=[]
        dish_name=[]
        dish_name= tracker.get_slot("dish_name")
        proceed=tracker.get_slot("proceed")
        if proceed=="No":
            dish_list.append(dish_name)
            return {"proceed":value,"dish_name":value}
        else:
            dish_list.append(tracker.get_slot("dish_name"))
            return {"dish_name":None,"proceed":None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
    
        dish_name=(tracker.get_slot("dish_name"))
        proceed=tracker.get_slot("proceed")
    
        dispatcher.utter_message("Thanks for ordering")
        return []
            
    
