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

        return {"complain_type": [self.from_entity("complain_type"), self.from_text()], "complain_text": [self.from_entity(entity="navigation"), self.from_text()]}

        # return {"complain_type": self.from_entity("complain_type"),"complain_text": self.from_entity(entity="any_thing")}

    def validate_complain_type(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        complaints = ["food quality", "delivery", "naaniz app", "other"]
        value = value.strip().lower()
        if value == "back1" or value == "back":
            return {"complain_type": INVALID_VALUE, "complain_text": INVALID_VALUE}
        elif value in complaints:
            return {"complain_type": value}
        else:
            dispatcher.utter_message("please type valid option.")
            return {"complain_type": None}

    def validate_complain_text(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if value == "back2" or value.lower() == "back":
            return {"complain_type": None, "complain_text": None}
        else:
            return {"complain_text": value}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        if tracker.get_slot("complain_type") != INVALID_VALUE:
            # saving
            with open("./actionserver/customer_queries.json", "r") as queriesRef:
                comp_type = tracker.get_slot("complain_type")
                comp = tracker.get_slot("complain_text")
                compObj = json.load(queriesRef)
                compObj["complaints"].append({
                    "createdOn": util.timestamp(),
                    "complaint_area": comp_type,
                    "complaint": comp
                })
                with open("./actionserver/customer_queries.json", "w") as queriesRefWrite:
                    json.dump(compObj, queriesRefWrite, indent=4)

            dispatcher.utter_message("Your Complaint :\n Complaint Area:{comp_type}\n Complaint: '{comp}' \n has been registered!".format(
                comp_type=comp_type, comp=comp))
        else:
            dispatcher.utter_message("Complaints Form is closed")
            li = [SlotSet("complain_type", None),
                  SlotSet("complain_text", None)]
            li.extend(query_back(dispatcher))
            return li
        return [SlotSet("complain_type", None), SlotSet("complain_text", None)]
