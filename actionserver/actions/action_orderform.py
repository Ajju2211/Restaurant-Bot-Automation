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


class ActionShowMenu(Action):
    def name(self) -> Text:
        return "action_show_menu"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        x = open('./actionserver/custom_payload.json', "r")
        data = json.load(x)
        data_restaurant = data['restaurant']
        for i in data['restaurant']['menu_imgs']:
            url = str(i)
            dispatcher.utter_message("Menu of that restaurant is ")
            dispatcher.utter_message(image=url)
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
            "dish_category": [
                self.from_entity("dish_category"),
                self.from_text()
            ],
            "dish_name": [
                self.from_entity("dish_name"),
                self.from_text()
            ],
            "quantity": [self.from_entity("quantity"), self.from_text()],
            "proceed": [self.from_entity("proceed"), self.from_text()]
        }

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ):
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                logger.debug(f"Request next slot '{slot}'")
                if slot == "dish_category":
                    dispatcher.utter_message(text="Please select the category")
                    button_resp = [
                        {
                            "title": "back",
                            "payload": '/inform{"dish_category":"back"}'
                        }
                    ]
                    dispatcher.utter_message(
                        text="type back otherwise!",
                        buttons=button_resp)
                    self.askCategories(dispatcher)
                elif slot == 'dish_name':
                    self.showDishes(tracker.get_slot(
                        "dish_category"), dispatcher, tracker)
                else:
                    dispatcher.utter_message(
                        template=f"utter_ask_{slot}", **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return None

    def askCategories(self, dispatcher):
        data = []
        for keys in restaurant_menu['restaurant']['menu'].keys():
            val = '\"{}\"'.format(keys)
            cat = {"label": f"{keys}",
                   "value": '/inform{\"dish_category\":'+val+'}'}
            data.append(cat)

        message = {"payload": "dropDown", "data": data}

        dispatcher.utter_message(
            text="Please select a option", json_message=message)
    # To display dishes of category

    def showDishes(self, category, dispatcher, tracker):
        dic = {}
        data = []
        print(f"cat:{category}")
        try:
            if restaurant_menu['restaurant']['menu'][category]:
                temp = restaurant_menu['restaurant']['menu'][category]
                for j in temp:

                    dic = {
                        "title": j['dish'],
                        "price": j['price'],
                        "image": j['image']
                    }

                    data.append(dic)

            message = {"payload": "cartCarousels", "data": data}
            button_resp = [
                {
                    "title": "back",
                    "payload": '/inform{"dish_name":"back1"}'
                }
            ]

            dispatcher.utter_message(
                text="Please type the dish name", json_message=message, buttons=button_resp)

            # return {"dish_category": category}

        except:
            dispatcher.utter_message(text="No such Category Found")
            raise Exception("No such Category")
            # return {"dish_category":None}

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

    def validate_dish_category(self,
                               value: Text,
                               dispatcher: CollectingDispatcher,
                               tracker: Tracker,
                               domain: Dict[Text, Any],
                               ) -> Dict[Text, Any]:

        data = []
        category = value
        if value:
            if value.lower() == 'back':
                return {
                    "dish_category": INVALID_VALUE,
                    "dish_name": INVALID_VALUE,
                    "quantity": INVALID_VALUE,
                    "proceed": INVALID_VALUE
                }
            else:
                try:
                    self.showDishes(category, dispatcher, tracker)
                    return {"dish_category": category}
                except:
                    return {"dish_category": None}
        else:
            return {"dish_category": None}

        # message={"payload":"cartCarousels","data":data}

        # dispatcher.utter_message(text="Please type the dish name",json_message=message)

        # return {"dish_category": category}

    def validate_dish_name(self,
                           value: Text,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: Dict[Text, Any],
                           ) -> Dict[Text, Any]:
        if value:
            value = value.lower()
            if value == "back" or value == "back1":
                return {
                    "dish_category": None,
                    "dish_name": None,
                    "quantity": None,
                    "proceed": None,
                    REQUESTED_SLOT: "dish_category"
                }
            else:

                category = tracker.get_slot("dish_category")

                # to debug whether the slot is present
                print(category)

                dish_name = value
                menu = restaurant_menu['restaurant']['menu']
                if menu[category]:
                    temp = menu[category]
                    for j in temp:
                        if dish_name.lower() == j['dish'].lower():
                            dispatcher.utter_message(
                                "it costs {}".format(j['price']))
                            return {"dish_name": dish_name}
                        else:
                            continue
                            # dispatcher.utter_template("utter_not_serving",tracker)
                            # return {"dish_name":None}
                    dispatcher.utter_template("utter_not_serving", tracker)
                    return {"dish_name": None}
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
        quantity = 0
        if value.lower() == 'back':
            return {
                "dish_name": None,
                "quantity": None,
                REQUESTED_SLOT: "dish_name"
            }
        try:
            quantity = int(value)
            return {"dish_name": dish_name, "quantity": quantity}
        except:
            dispatcher.utter_message(text="Please Enter Valid Number")
            return {"dish_name": dish_name, "quantity": None}

    def validate_proceed(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        dish_name = tracker.get_slot("dish_name")
        proceed = value
        quant = int(tracker.get_slot("quantity"))
        cat = tracker.get_slot("dish_category")
        if proceed:
            proceed = proceed.lower().strip()

            # check if the value exist in individual list
            if proceed in ADD_TO_CART:
                dish_obj = {"dish": dish_name,
                            "quantity": quant, "category": cat}
                dish_list.append(dish_obj)
                self.showDishes(cat, dispatcher, tracker)
                print("quantity")
                return {"proceed": None, "dish_name": None, "quantity": None, REQUESTED_SLOT: "dish_name"}

            elif proceed in BUY_NOW:
                dish_obj = {"dish": dish_name,
                            "quantity": quant, "category": cat}
                dish_list.append(dish_obj)
                return {"proceed": proceed}

            elif proceed in CHANGE_DISH:
                self.showDishes(cat, dispatcher, tracker)
                return {"dish_name": None, "proceed": None, "quantity": None, REQUESTED_SLOT: "dish_name"}

            elif proceed in CHANGE_QUANTITY:
                return {"quantity": None, "proceed": None, REQUESTED_SLOT: "quantity"}

            elif proceed in SWITCH_CATEGORY:
                return {"dish_category": None, "dish_name": None, "proceed": None, "quantity": None, REQUESTED_SLOT: "dish_category"}

            else:
                # Select other food
                dispatcher.utter_message(text="Please select a valid option")
                # self.showDishes(cat, dispatcher, tracker)
                return {"proceed": None, REQUESTED_SLOT: "proceed"}
        else:
            dispatcher.utter_message(text="Please select valid option")
            return {"proceed": None, REQUESTED_SLOT: "proceed"}

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
                amount += total
                # dispatcher.utter_message("{} : {} : {}".format(x['dish'],x["quantity"],total))
                # amount += total
            self.showCart(dispatcher, tracker)
            dispatcher.utter_message("Total Amount : {}".format(amount))
            dispatcher.utter_message("Thanks for ordering")
            return [AllSlotsReset()]
