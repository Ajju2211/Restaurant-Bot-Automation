from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import AllSlotsReset, SlotSet
import pandas as pd
from rasa.core.slots import Slot
import json
from utils import utilities as util
from test_utils import find_ans
dataset = pd.read_csv('dishes.csv')
dataset = dataset.set_index('dish').T.to_dict('list')
dish_list = []
quant_list = [] #takes quantity from user
restaurant_dataset = pd.read_csv('restaurant.csv')
restaurant_dataset = restaurant_dataset.set_index('restaurant').T.to_dict('list')

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
        x = open('custom_payload.json',"r")
        data = json.load(x)
        data_restaurant = data['restaurant']
        for i in data['restaurant']['menu_imgs']:
                url = str(i)
                dispatcher.utter_message("Menu of that restaurant is ")
                dispatcher.utter_message(image = url)
        return []




class OrderForm(FormAction):

    def name(self):
        return "order_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "dish_name",
            "quantity",
            "proceed"
            ]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"dish_name": self.from_entity("any_thing"),"quantity": self.from_entity("quantity"),"proceed": self.from_intent("inform")}


    def validate_dish_name(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        dish_name = tracker.get_slot("dish_name")

        if dish_name in dataset.keys():
            dispatcher.utter_message("it costs {}".format(dataset[dish_name][0]))
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


        return {"complain_type": self.from_entity("complain_type"),"complain_text": [self.from_text()]}

        #return {"complain_type": self.from_entity("complain_type"),"complain_text": self.from_entity(entity="any_thing")}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:


        # saving
        with open("customer_queries.json", "r") as queriesRef:
            comp_type=tracker.get_slot("complain_type")
            comp = tracker.get_slot("complain_text")
            compObj = json.load(queriesRef)
            compObj["complaints"].append({
                "createdOn":util.timestamp(),
                "complaint_area":comp_type,
                "complaint":comp
            })
            with open("customer_queries.json", "w") as queriesRefWrite:
                json.dump(compObj, queriesRefWrite, indent = 4)

        dispatcher.utter_message("Your Complaint :\n Complaint Area:{comp_type}\n Complaint: '{comp}' \n has been registered!".format(comp_type=comp_type,comp = comp))


        return [SlotSet("complain_type",None), SlotSet("complain_text",None)]


class FeedbackForm(FormAction):

    def name(self):
        return "feedback_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("rating"):
            return ["rating", "feedback_text"]
        else :
            return ["rating"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"rating": self.from_entity("rating"),"feedback_text": self.from_entity(entity="any_thing")}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        with open("customer_queries.json", "r") as queriesRef:
            rating=tracker.get_slot("rating")
            feedback = tracker.get_slot("feedback_text")
            feedbackObj = json.load(queriesRef)
            feedbackObj["feedback"].append({
                "createdOn":util.timestamp(),
                "complaint_area":rating,
                "complaint":feedback
            })
            with open("customer_queries.json", "w") as queriesRefWrite:
                json.dump(feedbackObj, queriesRefWrite, indent = 4)

        dispatcher.utter_message("Your Response :\n Rating :'{rate}' star \n Feedback: '{feedbk}' \n Submitted!Thank You!".format(rate=rating,feedbk=feedback))

        return [SlotSet("rating", None), SlotSet("feedback_text", None)]


class FaqForm(FormAction):

    def name(self):
        return "faq_form"

    @staticmethod
    def required_slots(tracker):

        if (tracker.get_slot("faq_choice")=="1"):
           return["faq_choice", "faq_question"]
        elif (tracker.get_slot("faq_choice")=="2"):
            return ["faq_choice", "faq_text"]
        else:
            return ["faq_choice"]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        #return { "faq_choice": self.from_entity("faq_choice"),"faq_question": self.from_entity("faq_question"), "faq_text": [self.from_text()]}

        return {"faq_choice": self.from_entity("faq_choice"), "faq_question": self.from_entity("faq_question"),"faq_text": self.from_entity(entity="any_thing") }

        # return {"faq_choice": self.from_entity("choice"),"faq_question": self.from_entity("choice"), "faq_text": self.from_entity(entity="any_thing")}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

            # fetching answer

            if (tracker.get_slot("faq_choice")=="1"):
                ques= tracker.get_slot("faq_question")
            elif (tracker.get_slot("faq_choice")=="2"):
                ques= tracker.get_slot("faq_text")
            #ques = "what is naaniz"
            ans = find_ans(ques)

            dispatcher.utter_message("Your Question :{}\n Answer:{}".format(ques, ans))

            return [SlotSet("faq_choice", None),SlotSet("faq_question", None),SlotSet("faq_text", None) ]



