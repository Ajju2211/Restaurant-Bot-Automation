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


# with open(r'./actionserver/custom_payload.json') as f:
#     frendy_product_menu = json.load(f)

# # Code snippet for global back
# # return [Restarted(), UserUttered(text="/get_started", parse_data={
#     #   "intent": {"confidence": 1.0, "name": "get_started"},
#     #   "entities": []
#     #  }), FollowupAction(name="utter_greet")]


# class UserInfoForm(FormAction):
#     """Default Fallback Action"""

#     def name(self) -> Text:
#         return "user_info_form"

#     @staticmethod
#     def required_slots(tracker):
#         if tracker.get_slot("locality"):
#             return [
#                 "pincode"
#             ]
#         elif tracker.get_slot("state"):
#             return [
#                 "locality"
#             ]
#         elif tracker.get_slot("phone_number"):
#             return [
#                 "state"
#             ]
#         elif tracker.get_slot("mailid"):
#             return [
#                 "phone_number"
#             ]
#         elif tracker.get_slot("username"):
#             return [
#                 "mailid"
#             ]        
#         else:
#             return [
#                 "username"
#             ]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         return {
#             "username": self.from_text(),
#             "mailid": self.from_text(),
#             "phone_number": self.from_text(),
#             "state": self.from_text(),
#             "locality": self.from_text(),
#             "pincode": self.from_text()
#         }
