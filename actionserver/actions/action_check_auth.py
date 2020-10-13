# from typing import Any, Text, Dict, List, Union
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
# from rasa_sdk.events import UserUtteranceReverted, UserUttered,  FollowupAction
# # from rasa_core.events import (UserUtteranceReverted, UserUttered,
# #                               ActionExecuted, Event)
# from rasa_sdk.events import AllSlotsReset, SlotSet
# from rasa.core.constants import REQUESTED_SLOT
# from rasa.core.slots import Slot
# import pandas as pd
# import json
# from actionserver.utils import utilities as util
# from actionserver.controllers.faqs.faq import FAQ
# from actionserver.controllers.constants.orderForm import *
# import logging
# from actionserver.utils.utilities import INVALID_VALUE
# from actionserver.utils.get_metadata import get_latest_metadata

# product_list = []
# quant_list = []  # takes quantity from user


# # with open(r'./actionserver/custom_payload.json') as f:
# #     frendy_product_menu = json.load(f)

# # Code snippet for global back
# # return [Restarted(), UserUttered(text="/get_started", parse_data={
# #   "intent": {"confidence": 1.0, "name": "get_started"},
# #   "entities": []
# #  }), FollowupAction(name="utter_greet")]


# def query_back(dispatcher):
#     dispatcher.utter_message("Going back to queries!!!")
#     greet_utter = UserUttered(text="/greet", parse_data={
#         "intent": {"confidence": 1.0, "name": "greet"},
#         "entities": []
#     })

#     query_utter = UserUttered(text="/query_init", parse_data={
#         "intent": {"confidence": 1.0, "name": "query_init"},
#         "entities": []
#     })

#     return [
#         greet_utter,
#         FollowupAction(name="utter_greet"),
#         query_utter,
#         FollowupAction(name="utter_query_type")
#     ]


# class ActionCheckAuth(Action):
#     def name(self) -> Text:
#         return "action_check_auth"

#     def run(
#         self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         meta = get_latest_metadata(tracker)

#         if meta.user.auth:
#             return [
#                 SlotSet("username", INVALID_VALUE),
#                 SlotSet("mailid", INVALID_VALUE),
#                 SlotSet("phone_number", INVALID_VALUE),
#                 SlotSet("state", INVALID_VALUE),
#                 SlotSet("locality", INVALID_VALUE),
#                 SlotSet("pincode", INVALID_VALUE)
#             ]
