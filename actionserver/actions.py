from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import AllSlotsReset, SlotSet
import pandas as pd
from rasa.core.slots import Slot
import json
from actionserver.utils import utilities as util
from actionserver.controllers.faqs.faq import FAQ
dataset = pd.read_csv('./actionserver/dishes.csv')
dataset = dataset.set_index('dish').T.to_dict('list')
dish_list = []
quant_list = [] #takes quantity from user
restaurant_dataset = pd.read_csv('./actionserver/restaurant.csv')
restaurant_dataset = restaurant_dataset.set_index('restaurant').T.to_dict('list')



with open(r'.\actionserver\custom_payload.json') as f:
    restaurant_menu = json.load(f)

# Code snippet for global back
# return [Restarted(), UserUttered(text="/get_started", parse_data={
                    #   "intent": {"confidence": 1.0, "name": "get_started"}, 
                    #   "entities": []
                    #  }), FollowupAction(name="utter_greet")]

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
            "confirm"
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

    def validate_confirm(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() not in self.msg():
            return {"phone_number": value}
        else:
            return {"phone_number": None,"confirm": None}


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

class ActionShowMenu(Action):
    def name(self) -> Text:
        return "action_show_menu"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        x = open('./actionserver/custom_payload.json',"r")
        data = json.load(x)
        data_restaurant = data['restaurant']
        for i in data['restaurant']['menu_imgs']:
                url = str(i)
                dispatcher.utter_message("Menu of that restaurant is ")
                dispatcher.utter_message(image = url)
        return []

class ActionAskDishCategory(Action):
    def name(self) -> Text:
        return "action_ask_dish_category"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        data=[
			{"label":"starters1","value":"/inform{'dish_category':'starters'}"},
			{"label":"meals1","value":"/inform{'dish_category':'meals'}"}
			]

        message={"payload":"dropDown","data":data}
  
        dispatcher.utter_message(text="Please select a option",json_message=message)
        return []



class OrderForm(FormAction):

    def name(self):
        return "order_form"
    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("quantity"):
            return [
                "proceed"
                ]
        else:
            return [
                "dish_category",
                "dish_name",
                "quantity",
                "proceed"
            ]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"dish_category": self.from_intent("inform"),"dish_name": self.from_entity("any_thing"),"quantity": self.from_entity("quantity"),"proceed": self.from_intent("inform")}
    
    # def request_next_slot(
    #     self,
    #     dispatcher: "CollectingDispatcher",
    #     tracker: "Tracker",
    #     domain: Dict[Text, Any],
    #     ):

    #     for slot in self.required_slots(tracker):
    #         if self._should_request_slot(tracker, slot):
    #             kwargs = {}
    #             if slot == 'dish_category':
    #                 kwargs.update({"action_ask_dish_category": "some_value"})

    #                 dispatcher.utter_template("utter_ask_{}".format(slot), tracker, **kwargs)

    #                 return [SlotSet("requested_slot", slot)]

    def validate_dish_category(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        data = []
        category = tracker.get_slot("dish_category")

        # for keys in restaurant_menu['restaurant']['menu'].keys():

        #     if category in keys:
        #         temp = restaurant_menu['restaurant']['menu'][category]
        #         for j in temp:


        #             dic = {
        #                 "title":j['dish'],
        #                    "price":j['price'],
        #                    "image" : j['image']
        #                }
                    
        #             data.append(dic)
        try:
            if restaurant_menu['restaurant']['menu'][category]:
                temp = restaurant_menu['restaurant']['menu'][category]
                for j in temp:


                    dic = {
                        "title" : j['dish'],
                        "price" : j['price'],
                        "image" : j['image']
                    }
                    
                    data.append(dic)
            
            message={"payload":"cartCarousels","data":data}
  
            dispatcher.utter_message(text="Please type the dish name",json_message=message)

            return {"dish_category": category}
        
        except :
            dispatcher.utter_message(text="No such Category Found")
            return {"dish_category":None}        

        			
        # message={"payload":"cartCarousels","data":data}
  
        # dispatcher.utter_message(text="Please type the dish name",json_message=message)

        # return {"dish_category": category}

    def validate_dish_name(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        category = tracker.get_slot("dish_category")

        # to debug whether the slot is present
        print(category)

        dish_name = value
        menu = restaurant_menu['restaurant']['menu']
        if menu[category]:
            temp = menu[category]
            for j in temp:
                if dish_name.lower() == j['dish'].lower():
                    dispatcher.utter_message("it costs {}".format(j['price']))
                    return {"dish_name": dish_name}
                else:
                    continue
                    # dispatcher.utter_template("utter_not_serving",tracker)
                    # return {"dish_name":None}
            dispatcher.utter_template("utter_not_serving",tracker)
            return {"dish_name":None}
        else:
            dispatcher.utter_message(text="No such category found")

    


        # if dish_name in dataset.keys():
        #     dispatcher.utter_message("it costs {}".format(dataset[dish_name][0]))
        #     return {"dish_name": dish_name}
        # else:
        #     dispatcher.utter_template("utter_not_serving",tracker)
        #     return {"dish_name":None}
    def validate_quantity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        dish_name = tracker.get_slot("dish_name")
        quantity=0
        try:
            quantity = int(value)
            return {"dish_name":dish_name,"quantity":quantity}
        except:
            dispatcher.utter_message(text="Please Enter Valid Number")
            return {"dish_name":dish_name,"quantity":None}


    def validate_proceed(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        dish_name = tracker.get_slot("dish_name")
        proceed = tracker.get_slot("proceed")
        quant = int(tracker.get_slot("quantity"))
        if proceed =="Add to Cart":
            dish_list.append(dish_name)
            quant_list.append(quant)
            print("quantity")
            return {"proceed":None,"dish_name":None,"quantity":None}

        elif proceed == "Buy Now":
            dish_list.append(dish_name)
            quant_list.append(quant)
            return {"proceed":proceed}

        else:
            return {"dish_name":None,"proceed":None,"quantity":None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        amount = 0
        for x in range(len(dish_list)):
            dispatcher.utter_message("{} : {} : {}".format(dish_list[x],quant_list[x],dataset[dish_list[x]][0]))
            z = int(dataset[dish_list[x]][0])
            amount += z
        dispatcher.utter_message("Total Amount : {}".format(amount))
        dispatcher.utter_message("Thanks for ordering")
        return [AllSlotsReset()]

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

class ComplainForm(FormAction):

    def name(self):
        return "complain_form"

    @staticmethod
    def required_slots(tracker):

            if tracker.get_slot("complain_type"):
                return ["complain_type", "complain_text"]
            else:
                return ["complain_type"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        return {"complain_type": self.from_entity("complain_type"),"complain_text": [self.from_entity(entity="navigation"),self.from_text()]}

        #return {"complain_type": self.from_entity("complain_type"),"complain_text": self.from_entity(entity="any_thing")}

    def validate_complain_type(
        self,
        value:Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if value=="back1":
            return {"complain_type":"-1","complain_text":"-1"}
        else:
            return {"complain_type":value}
    def validate_complain_text(
        self,
        value:Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if value=="back2":
            return {"complain_type":None,"complain_text":None}
        else:
            return {"complain_text":value}
        

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        if tracker.get_slot("complain_type")!="-1":
        # saving 
            with open("./actionserver/customer_queries.json", "r") as queriesRef:
                comp_type=tracker.get_slot("complain_type")
                comp = tracker.get_slot("complain_text")
                compObj = json.load(queriesRef)
                compObj["complaints"].append({
                    "createdOn":util.timestamp(),
                    "complaint_area":comp_type,
                    "complaint":comp
                })
                with open("./actionserver/customer_queries.json", "w") as queriesRefWrite:
                    json.dump(compObj, queriesRefWrite, indent = 4)

            dispatcher.utter_message("Your Complaint :\n Complaint Area:{comp_type}\n Complaint: '{comp}' \n has been registered!".format(comp_type=comp_type,comp = comp))
        else:
            dispatcher.utter_message("Complaints Form is closed")


        return [SlotSet("complain_type",None), SlotSet("complain_text",None)]


class FeedbackForm(FormAction):

    def name(self):
        return "feedback_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("rating"):
            return ["rating","feedback_text"]
        else :
            return ["rating"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {"rating": self.from_entity("rating"),"feedback_text": [self.from_entity(entity="any_thing"),self.from_entity(entity="navigation")]}

    def validate_rating(
    self,
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value=="back1":
            return {"rating":"-1", "feedback_text":"-1"}
        else:
            return {"rating":value}

    def validate_feedback_text(
    self,
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value=="back2":
            return {"rating":None, "feedback_text":None}
        else:
            return {"feedback_text":value}


    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("rating")!="-1":
            with open("./actionserver/customer_queries.json", "r") as queriesRef:
                rating=tracker.get_slot("rating")
                feedback = tracker.get_slot("feedback_text")
                feedbackObj = json.load(queriesRef)
                feedbackObj["feedback"].append({
                    "createdOn":util.timestamp(),
                    "complaint_area":rating,
                    "complaint":feedback
                })
            with open("./actionserver/customer_queries.json", "w") as queriesRefWrite:
                json.dump(feedbackObj, queriesRefWrite, indent = 4)

            dispatcher.utter_message("Your Response :\n Rating :'{rate}' star \n Feedback: '{feedbk}' \n Submitted!Thank You!".format(rate=rating,feedbk=feedback))
        else:
            dispatcher.utter_message("Feedback form closed")

        return [SlotSet("rating", None), SlotSet("feedback_text", None)]
    

        
              

class FaqForm(FormAction):

    def name(self):
        return "faq_form"

    @staticmethod
    def required_slots(tracker):
        return ["faq_choice","faq_text"]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        #return { "faq_choice": self.from_entity("faq_choice"),"faq_question": self.from_entity("faq_question"), "faq_text": [self.from_text()]}

        return {"faq_choice": self.from_entity("faq_choice"), "faq_text": [self.from_entity(entity="any_thing"),self.from_entity(entity="navigation")] }

        # return {"faq_choice": self.from_entity("choice"),"faq_question": self.from_entity("choice"), "faq_text": self.from_entity(entity="any_thing")}

    def validate_faq_choice(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        faq_choice = tracker.get_slot("faq_choice")
        print(faq_choice)

        if faq_choice == "back2":
            return {"faq_choice": "-1","faq_text":"-1"}
        elif faq_choice == "1":
            useNlp = False
            faq_data = pd.read_csv("./actionserver/controllers/faqs/test_faq.csv")

            button_resp = [
                {
                    "title":"Choose from our set of FAQs",
                    "payload": "/faq_choice{\"faq_choice\": \"1\"}"
                },
                {
                    "payload": "/faq_choice{\"faq_choice\": \"2\" }",
                    "title": "Type your own question."
                },{
                        "payload": "/faq_choice{\"faq_choice\": \"back2\"}",
                        "title": "Back"
                }
            ]
            dispatcher.utter_message(text="How should we get your FAQ?", buttons=button_resp)
            qa = []
            for i in range(len(faq_data)):
                obj = {
                "title":faq_data["Question"][i],
                "description":faq_data["Answer"][i]
                    }
                qa.append(obj)
            message={ "payload": "collapsible", "data": qa }
            dispatcher.utter_message(text="Faq's",json_message=message)

            return {"faq_choice":None}
        else:
            return {"faq_choice":value}

    def validate_faq_text(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        faq_choice = tracker.get_slot("faq_choice")
        try:
            navigation = tracker.get_slot("navigation")
        except:
            navigation = "NOBACK"
        print(value)


        if navigation == "back3":
            return {"faq_text": None,"faq_choice": None,"navigation":None}
        else:
            # dispatcher.utter_template("utter_not_serving",tracker)
            print(faq_choice)
            if faq_choice!="-1":
                ques= value
                useNlp = True

                f = FAQ("./actionserver/controllers/faqs/test_faq.csv")
                # NLP disabled coz morethan 100 sec
                ans = f.ask_faq(ques, NLP = False)
                if ans:
                    dispatcher.utter_message("Your Question :{}\n Answer:{}".format(ques, ans))
                else:
                    dispatcher.utter_message("Query not found !")               
                return {"faq_choice":faq_choice,"faq_text":None}
            else:
                {"faq_choice":faq_choice,"faq_text":"filled"}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
            # handle back2 logic here
            dispatcher.utter_message("Faq is closed")
            return [SlotSet("faq_choice", None),SlotSet("faq_text", None) ]



