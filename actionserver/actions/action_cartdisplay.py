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


logger = logging.getLogger(__name__)




# Code snippet for global back
# return [Restarted(), UserUttered(text="/get_started", parse_data={
    #   "intent": {"confidence": 1.0, "name": "get_started"},
    #   "entities": []
    #  }), FollowupAction(name="utter_greet")]

class ActionCartDisplay(Action):

    def name(self) -> Text:
        return "action_cartDisplay"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        data = []
        with open(r'./actionserver/order_cart.json') as f:
            cart = json.load(f)["cart"]
        total = 0
        for x in cart:
            cart = {
                "title": x['dish_name'],
                "image": x['dish_image'],
                "quantity": x['dish_quantity'],
                "price": x['dish_price']
            }
            total += x['dish_price']*x['dish_quantity']

            data.append(cart)

        message = {"payload": "cartCarousels", "data": data}

        dispatcher.utter_message(text= f'Your Order total is {total}', json_message=message)
        return []
        

