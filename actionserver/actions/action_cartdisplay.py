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


with open(r'.\actionserver\order_cart.json') as f:
    restaurant_menu = json.load(f)

# Code snippet for global back
# return [Restarted(), UserUttered(text="/get_started", parse_data={
    #   "intent": {"confidence": 1.0, "name": "get_started"},
    #   "entities": []
    #  }), FollowupAction(name="utter_greet")]

class CartDisplay(Action):

    def name(self) -> Text:
        return "action_cartdisplay"
    def required_slots(tracker):
        return [
            "dish_catergory",
            "disg_name",
            "quantity",
            "confirm"
        ]

    def cartdisplay(self, dispatcher, tracker):
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

        
    #     self,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> List[Dict]:
    #     if tracker.get_slot("dish_category") == INVALID_VALUE:
    #         li = [
    #             SlotSet("dish_category", None),
    #             SlotSet("dish_name", None),
    #             SlotSet("quantity", None),
    #             SlotSet("proceed", None)
    #         ]
    #         li.extend(greet_back(dispatcher))
    #         return li

    #     else:

    #         amount = 0
    #         dish_cat = tracker.get_slot("dish_category")
    #         total = 0
    #         price = 0

    #         for x in dish_list:
    #             prize = util.dish_info(x['dish'], x['category'])['price']
    #             image = util.dish_info(x['dish'],x['category'])['image']
    #             total = float(prize)*int(x['quantity'])
    #             amount += total
                
    #             order_data = {
    #                 "dish_category" : x['category'],
    #                 "dish_name" : x['dish'],
    #                 "dish_price" : prize,
    #                 "dish_quantity" : x['quantity'],
    #                 "dish_image" : image
    #             }

    #             # amount += total
    #             dispatcher.utter_message("{} : {} : {}".format(
    #                 x['dish'], x["quantity"], total))
    #             amount += total
    #         self.showCart(dispatcher, tracker)
    #         dispatcher.utter_message("Total Amount : {}".format(amount))
    #         #dispatcher.utter_message("Thanks for ordering")
    #         return [AllSlotsReset()]
