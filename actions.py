from typing import Any, Text, Dict, List,Union
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
    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        username = tracker.get_slot("username")
        mailid = tracker.get_slot("mailid")
        phone_number=tracker.get_slot("phone_number")
        
        
       
        message="ORDER DETAILS:"+"\n\n"+"Name:"+username+"\n"+"Email:"+mailid+"\n"+"Phone Number:"+phone_number+"\n"+"\nThanks for ordering! Your order will be placed soon." 
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
            dispatcher.utter_message("it costs "+ str(dataset[dish_name][0]))
            return {"dish_name": dish_name}
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
            
    



class ComplainForm(FormAction):

    def name(self):
        return "complain_form"

    @staticmethod
    def required_slots(tracker):

        
            return ["complain_type", "complain_text"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
                

            "complain_text": [
                self.from_text(intent="complain"),
            ],



        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

     
     #Writing complin to external file.
        f = open("complaints.txt", "a")
        xp=tracker.get_slot("complain_type")      
        f.write("Complain Area: ")
        f.write(xp)
        f.write(",  Complain Text: ")
        xp=tracker.get_slot("complain_text")   
        f.write(xp)
        f.close()   

        dispatcher.utter_message("Thanks Complain Registered")
        return []
        amount = 0
        for x in dish_list:
            dispatcher.utter_message(x+":"+str(dataset[x][0]))
            amount += dataset[x][0]
        dispatcher.utter_message("Total Amount : "+str(amount))    
        dispatcher.utter_message("Thanks for ordering")
        return []
            
class DefaultFallback(FormAction):
    """Default Fallback Action"""

    def name(self):
        return "action_default_fallback"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any])-> List[Dict[Text, Any]]:
        queryText = tracker.latest_message.get('text')

        dispatcher.utter_message("Fallback Triggered bcoz u've typed something! "+queryText)
        return []



