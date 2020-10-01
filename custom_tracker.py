import traceback
import contextlib
import itertools
import json
import logging
import os
import pickle
from datetime import datetime, timezone
# Import custom module made for firebase credentials
from actionserver.db.dbConfig import db

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
from rasa.core.tracker_store import TrackerStore

logger = logging.getLogger(__name__)



class FirebaseTrackerStore(TrackerStore):
    """Stores conversation history in memory"""

    # def __init__(
    #     self, domain: Domain, event_broker: Optional[EventBroker] = None
    # ):
    def __init__(
        self,
        domain: Domain,
<<<<<<< HEAD
        collection: Optional[Text] = "tracker",
=======
>>>>>>> 2ef12546cd268709be6fdf654b962ea9093d5152
        host: Optional[Text] = "localhost",
        event_broker: Optional[EventBroker] = None
    ):
        self.store = {}
        self.COLLECTION = collection
        super().__init__(domain, event_broker)

    def save(self, tracker: DialogueStateTracker) -> None:
<<<<<<< HEAD
        """Updates and saves the current conversation state

        Args:
            tracker: DialogueStateTracker from TrackerStore Class 

        Returns:
            None

        Stores data in Firebase and creates tracker            
        """

        try:
            if self.event_broker:
                self.stream_events(tracker)
            serialised = self.serialiseTracker(tracker)

            ref = db.collection(self.COLLECTION).document(tracker.sender_id)
            ref.set(serialised)

=======
        """Updates and saves the current conversation state"""

        try:
            if self.event_broker:
                self.stream_events(tracker)
            serialised = self.serialiseTracker(tracker)


            # self.store[tracker.sender_id] = serialised
            # store to Firestore
            ref = db.collection(COLLECTION).document(tracker.sender_id)
            ref.set(serialised)

>>>>>>> 2ef12546cd268709be6fdf654b962ea9093d5152
        except Exception as e:
            traceback.print_exc()

    def checkSenderId(self, sender_id):
        """
        Checks if sender Id exists in database (firebase)

        Args:
            sender_id : takes the sender_id as input 

        Returns: 
            Boolean (if the id exists or not) 
        """

        check = db.collection(self.COLLECTION).document(sender_id).get().exists
        return check

    
    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """
        Args:
            sender_id: the message owner ID

        Returns:
            DialogueStateTracker
        """

        if self.checkSenderId(sender_id):
            logger.debug(f"Recreating tracker for id '{sender_id}'")

            deserialised_tracker = self.deserialiseTracker(sender_id)
            return deserialised_tracker
        else:
            logger.debug(f"Creating a new tracker for id '{sender_id}'.")
            return None

    def keys(self) -> Iterable[Text]:
<<<<<<< HEAD
        """
        Returns: 
            sender_ids of the Tracker Store in Firebase
        """

        docs = db.collection(self.COLLECTION).stream()
=======
        """Returns sender_ids of the Tracker Store in Firebase"""
        
        docs = db.collection(COLLECTION).stream()
>>>>>>> 2ef12546cd268709be6fdf654b962ea9093d5152
        keys = []
        for doc in docs:
            keys.append(doc.id)
        return keys
<<<<<<< HEAD

    def serialiseTracker(self, tracker:DialogueStateTracker):
        """
        User defined serialisation
        
        Args:
            tracker : takes tracker object as input
        Returns:
            dialogue    
        """
        try:
            dialogue = tracker.as_dialogue().as_dict()
=======
    def serialiseTracker(self, tracker):
        """User defined serialisation"""
        try:
            dialogue = tracker.as_dialogue().as_dict()
            print(f'dialoggue: {dialogue}')
>>>>>>> 2ef12546cd268709be6fdf654b962ea9093d5152
            dialogue = json.dumps(dialogue)
            dialogue = json.loads(dialogue)
            return dialogue
        except Exception as e:
            traceback.print_exc()
            return None

    def deserialiseTracker(self, sender_id):
<<<<<<< HEAD
        """User defined deserialisation
        Args:
            sender_id : Takes sender_id as input
        
        Returns:
            returns tracker
        """
        
=======
        """User defined deserialisation"""
        # dialogue = pickle.loads(_json)
        # try:
        #     ref = db.collection(COLLECTION).document(sender_id)
        #     dialogue = ref.get().to_dict()
        #     tracker = self.init_tracker(sender_id)
        #     tracker.recreate_from_dialogue(dialogue)
        #     return tracker
        # except Exception as e:
        #     logger.error('Sender Id is not found')
        #     return None
        # tracker = self.init_tracker(sender_id)
        # if not tracker:
        #     return None
>>>>>>> 2ef12546cd268709be6fdf654b962ea9093d5152
        tracker = self.init_tracker(sender_id)
        try:
            if not tracker:
                return None
<<<<<<< HEAD
            ref = db.collection(self.COLLECTION).document(sender_id)
            dialogue = ref.get().to_dict()
            # serialiseTracker(dialogue) no need to pass
            dialogue = Dialogue.from_parameters(
                json.loads(json.dumps(dialogue)))
=======
            ref = db.collection(COLLECTION).document(sender_id)
            dialogue = ref.get().to_dict()
            # serialiseTracker(dialogue) no need to pass
            dialogue = Dialogue.from_parameters(json.loads(json.dumps(dialogue)))
>>>>>>> 2ef12546cd268709be6fdf654b962ea9093d5152
        except Exception as e:
            traceback.print_exc()
        tracker.recreate_from_dialogue(dialogue)

        return tracker




