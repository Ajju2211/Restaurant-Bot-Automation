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
        return ["back1", "back2", "back3"]

    def validate_mailid(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
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
            return {"phone_number": None, "mailid": None}

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
            return {"phone_number": None, "confirm": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        username = tracker.get_slot("username")
        mailid = tracker.get_slot("mailid")
        phone_number = tracker.get_slot("phone_number")

        message = "DETAILS:"+"\n\n"+"Name:"+username+"\n"+"Email:"+mailid+"\n" + \
            "Phone Number:"+phone_number+"\n"+"\nThanks! for sharing information."
        saveFile = open("some.txt", 'a')
        saveFile.write(message)
        saveFile.close()
        dispatcher.utter_message(message)
        return []
