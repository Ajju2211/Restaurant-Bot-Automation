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


with open(r'./actionserver/custom_payload.json') as f:
    restaurant_menu = json.load(f)

# Code snippet for global back
# return [Restarted(), UserUttered(text="/get_started", parse_data={
    #   "intent": {"confidence": 1.0, "name": "get_started"},
    #   "entities": []
    #  }), FollowupAction(name="utter_greet")]


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


class FeedbackForm(FormAction):

    def name(self):
        return "feedback_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("rating"):
            return ["rating", "feedback_text"]
        else:
            return ["rating"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        # return {"rating": [self.from_entity("rating"),self.from_entity("any_thing")],"feedback_text": [self.from_entity(entity="any_thing"),self.from_entity(entity="navigation")]}
        return {"rating": [self.from_entity("rating"), self.from_text()], "feedback_text": [self.from_text(), self.from_entity(entity="navigation")]}

    def validate_rating(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        ratings = ['1', '2', '3', '4', '5']
        try:
            value = value.strip()
            if value == "back1" or value.lower() == "back":
                return {"rating": INVALID_VALUE, "feedback_text": INVALID_VALUE}
                # 1-5 it integer otherwise rating:None
            elif value in ratings:
                return {"rating": value, "feedback_text": None}
            else:
                dispatcher.utter_message("Please enter valid option.")
                return {"rating": None, "feedback_text": None}
        except Exception as e:
            print(e)
            dispatcher.utter_message("Please enter valid option.")
            return {"rating": None, "feedback_text": None}

    def validate_feedback_text(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value == "back2" or value.lower() == "back":
            return {"rating": None, "feedback_text": None}
        else:
            return {"feedback_text": value}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("rating") != INVALID_VALUE:
            with open("./actionserver/customer_queries.json", "r") as queriesRef:
                rating = tracker.get_slot("rating")
                feedback = tracker.get_slot("feedback_text")
                feedbackObj = json.load(queriesRef)
                feedbackObj["feedback"].append({
                    "createdOn": util.timestamp(),
                    "complaint_area": rating,
                    "complaint": feedback
                })
            with open("./actionserver/customer_queries.json", "w") as queriesRefWrite:
                json.dump(feedbackObj, queriesRefWrite, indent=4)

            dispatcher.utter_message("Your Response :\n Rating :'{rate}' star \n Feedback: '{feedbk}' \n Submitted!Thank You!".format(
                rate=rating, feedbk=feedback))
        else:
            dispatcher.utter_message("Feedback form closed")
            li = [SlotSet("rating", None), SlotSet("feedback_text", None)]
            li.extend(query_back(dispatcher))
            return li
        return [SlotSet("rating", None), SlotSet("feedback_text", None)]
