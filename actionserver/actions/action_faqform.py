from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted, UserUttered,  FollowupAction
# from rasa_core.events import (UserUtteranceReverted, UserUttered,
#                               ActionExecuted, Event)
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa.core.constants import REQUESTED_SLOT
from rasa.core.slots import Slot
import pandas as pd
import json
from actionserver.utils import utilities as util
from actionserver.controllers.faqs.faq import FAQ
from actionserver.controllers.constants.orderForm import *
import logging
from actionserver.utils.utilities import INVALID_VALUE

dish_list = []
quant_list = []  # takes quantity from user


logger = logging.getLogger(__name__)


with open(r'.\actionserver\custom_payload.json') as f:
    restaurant_menu = json.load(f)


def query_back(dispatcher):
    dispatcher.utter_message("Going back to queries!!!")
    greet_utter = UserUttered(text="/greet", parse_data={
        "intent": {"confidence": 1.0, "name": "greet"},
        "entities": []
    })

    query_utter = UserUttered(text="/query_init", parse_data={
        "intent": {"confidence": 1.0, "name": "query_init"},
        "entities": []
    })

    return [
        greet_utter,
        FollowupAction(name="utter_greet"),
        query_utter,
        FollowupAction(name="utter_query_type")
    ]


def greet_back(dispatcher):
    dispatcher.utter_message("Going back!!!")
    return [UserUttered(text="/greet", parse_data={
        "intent": {"confidence": 1.0, "name": "greet"},
        "entities": []
    }), FollowupAction(name="utter_greet")]


class FaqForm(FormAction):

    def name(self):
        return "faq_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("faq_choice"):
            if tracker.get_slot("faq_choice") == '2':
                return ["faq_text"]
            else:
                return ['faq_choice']
        else:
            return ['faq_choice']
        # return ["faq_choice","faq_text"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        # return { "faq_choice": self.from_entity("faq_choice"),"faq_question": self.from_entity("faq_question"), "faq_text": [self.from_text()]}

        return {"faq_choice": [self.from_entity("faq_choice"), self.from_text()], "faq_text": [self.from_text(), self.from_entity(entity="navigation")]}

    def validate_faq_choice(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
        # faq_choice = tracker.get_slot("faq_choice")
        faq_choice = value
        print(f"Inside validate faq choice {faq_choice}")

        if faq_choice == "back2" or value.lower() == 'back':
            # return {"faq_choice": INVALID_VALUE,"faq_text":INVALID_VALUE}
            return {"faq_choice": INVALID_VALUE, "faq_text": INVALID_VALUE}

        elif faq_choice == "1":
            useNlp = False
            faq_data = pd.read_csv(
                "./actionserver/controllers/faqs/test_faq.csv")

            button_resp = [
                {
                    "title": "Choose from our set of FAQs",
                    "payload": "/faq_choice{\"faq_choice\": \"1\"}"
                },
                {
                    "payload": "/faq_choice{\"faq_choice\": \"2\" }",
                    "title": "Type your own question."
                }, {
                    "payload": "/faq_choice{\"faq_choice\": \"back2\"}",
                    "title": "Back"
                }
            ]
            dispatcher.utter_message(
                text="How should we get your FAQ?", buttons=button_resp)
            qa = []
            for i in range(len(faq_data)):
                obj = {
                    "title": faq_data["Question"][i],
                    "description": faq_data["Answer"][i]
                }
                qa.append(obj)
            message = {"payload": "collapsible", "data": qa}
            dispatcher.utter_message(text="Faq's", json_message=message)

            return {
                "faq_choice": None,
                REQUESTED_SLOT: "faq_choice"
            }

        elif faq_choice == '2':
            return {
                "faq_choice": value,
                REQUESTED_SLOT: "faq_text"
            }

        else:
            dispatcher.utter_message(text="Please type valid option")
            return {
                "faq_choice": None,
                REQUESTED_SLOT: "faq_choice"
            }

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
        print(f'Inside faq_text {value}')

        if navigation == "back3" or value.lower() == "back":
            return {"faq_text": None, "faq_choice": None, "navigation": None}
        else:
            # dispatcher.utter_template("utter_not_serving",tracker)
            print(f'checking navigation {faq_choice}')
            # if faq_choice!=INVALID_VALUE:
            if faq_choice != INVALID_VALUE:
                ques = value
                useNlp = True

                f = FAQ("./actionserver/controllers/faqs/test_faq.csv")
                # NLP disabled coz morethan 100 sec
                ans = f.ask_faq(ques, NLP=False)
                if ans:
                    dispatcher.utter_message(
                        "Your Question :{}\n Answer:{}".format(ques, ans))
                else:
                    dispatcher.utter_message("Query not found !")
                return {"faq_choice": faq_choice, "faq_text": None}
            else:
                {"faq_choice": faq_choice, "faq_text": "filled"}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # handle back2 logic here
        dispatcher.utter_message("Faq is closed")
        # return greet_back(dispatcher)
        li = [SlotSet("faq_choice", None), SlotSet("faq_text", None)]
        li.extend(greet_back(dispatcher))
        return li
