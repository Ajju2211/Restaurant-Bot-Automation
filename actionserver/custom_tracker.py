import contextlib
import itertools
import json
import logging
import os
import pickle
from datetime import datetime, timezone
# Import custom module made for firebase credentials
# from actionserver.db_firebase.db_cred import *

from time import sleep
from typing import (
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Text,
    Union,
    TYPE_CHECKING,
)

from boto3.dynamodb.conditions import Key
import rasa.core.utils as core_utils
from rasa.core.actions.action import ACTION_LISTEN_NAME
from rasa.core.brokers.broker import EventBroker
from rasa.core.constants import (
    POSTGRESQL_SCHEMA,
    POSTGRESQL_MAX_OVERFLOW,
    POSTGRESQL_POOL_SIZE,
)
from rasa.core.conversation import Dialogue
from rasa.core.domain import Domain
from rasa.core.events import SessionStarted
from rasa.core.trackers import ActionExecuted, DialogueStateTracker, EventVerbosity
import rasa.cli.utils as rasa_cli_utils
from rasa.utils.common import class_from_module_path, raise_warning, arguments_of
from rasa.utils.endpoints import EndpointConfig
import sqlalchemy as sa

from actionserver.db.dbConfig import db

COLLECTION = "restaurant-bot-tracker"



class FirebaseTrackerStore(TrackerStore):
    """Stores conversation history in memory"""

    def __init__(
        self, domain: Domain, event_broker: Optional[EventBroker] = None
    ) -> None:
        self.store = {}
        logger.debug("using custom tracker")
        super().__init__(domain, event_broker)

    def save(self, tracker: DialogueStateTracker) -> None:
        """Updates and saves the current conversation state"""
        if self.event_broker:
            self.stream_events(tracker)
        serialised = self.serialiseTracker(sender_id, tracker, COLLECTION)

        # added print
        print(f"{self.event_broker} EventBroker ")

        self.store[tracker.sender_id] = serialised

        # added print bellow
        print(f"Store {self.store}, Serialize {serialised}")

    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """
        Args:
            sender_id: the message owner ID

        Returns:
            DialogueStateTracker
        """
        if sender_id in self.store:
            logger.debug(f"Recreating tracker for id '{sender_id}'")

            # added code bellow
            val = self.deserialiseTracker(sender_id, self.store[sender_id], COLLECTION, db)

            # added print
            print(val)

            return self.deserialiseTracker(sender_id, self.store[sender_id], COLLECTION, db)
        else:
            logger.debug(f"Creating a new tracker for id '{sender_id}'.")
            return None

    def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the Tracker Store in memory"""
        
        # added print
        print(f"Store Keys {self.store.keys()}")

        return self.store.keys()
    def serialiseTracker(self, sender_id, tracker, collection):
        """User defined serialisation"""
        dialogue = tracker.as_dialogue()
        dialogue = json.dumps(dialogue)
        dialogue = json.loads(dialogue)
        ref = db.reference(f'{collection}/{sender_id}')
        ref.set(dialogue)
        return dialogue

    def deserialiseTracker(self, sender_id, collection, db):
        """User defined deserialisation"""
        # dialogue = pickle.loads(_json)
        try:
            ref = db.reference(f'{collection}/{sender_id}')
            dialogue = ref.get()
            tracker = self.init_tracker(sender_id)
            tracker.recreate_from_dialogue(dialogue)
            return tracker
        except Exception as e:
            logging.error('Sender Id is not found')
            return None



