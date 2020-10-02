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

def greet_back(dispatcher):
    dispatcher.utter_message("Going back!!!")
    return [UserUttered(text="/greet", parse_data={
        "intent": {"confidence": 1.0, "name": "greet"},
        "entities": []
    }), FollowupAction(name="utter_greet")]

class CartDisplay(FormAction):

    def name(self):
        return "order_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("quantity"):
            return [
                "proceed"
            ]
        elif tracker.get_slot("dish_name"):
            return [
                "quantity"
            ]
        elif tracker.get_slot("dish_category"):
            return [
                "dish_name"
            ]
        else:
            return [
                "dish_category",
                # "dish_name",
                # "quantity",
                # "proceed"
            ]
     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        # return {"dish_category": self.from_intent("inform"),"dish_name": self.from_entity("any_thing"),"quantity": self.from_entity("quantity"),"proceed": self.from_intent("inform")}
        # return {"dish_category": [self.from_intent("inform"),self.from_text()], "dish_name": self.from_text(), "quantity": self.from_entity("quantity"), "proceed": self.from_intent("inform")}
        return {
            
            "dish_name": [
                self.from_entity("dish_name"),
                self.from_text()
            ],
            "quantity": [self.from_entity("quantity"), self.from_text()],
            "proceed": [self.from_entity("proceed"), self.from_text()]
        }
    def showCart(self, dispatcher, tracker):
        data = []
        for x in dish_list:
            image = util.dish_info(x['dish'], x['category'])['image']
            price = util.dish_info(x['dish'], x['category'])['price']
            cart = {
                "title": x['dish'],
                "image": image,
                "quantity": x['quantity'],
                "price": price
            }

            data.append(cart)

        message = {"payload": "cartCarousels", "data": data}

        dispatcher.utter_message(text="Your Order", json_message=message)
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("dish_category") == INVALID_VALUE:
            li = [
                SlotSet("dish_category", None),
                SlotSet("dish_name", None),
                SlotSet("quantity", None),
                SlotSet("proceed", None)
            ]
            li.extend(greet_back(dispatcher))
            return li

        else:

            amount = 0
            dish_cat = tracker.get_slot("dish_category")
            total = 0
            price = 0

            for x in dish_list:
                prize = util.dish_info(x['dish'], x['category'])['price']
                total = float(prize)*int(x['quantity'])
                # amount += total
                 dispatcher.utter_message("{} : {} : {}".format(x['dish'],x["quantity"],total))
                 amount += total
            self.showCart(dispatcher, tracker)
            dispatcher.utter_message("Total Amount : {}".format(amount))
            dispatcher.utter_message("Thanks for ordering")
            return [AllSlotsReset()]


