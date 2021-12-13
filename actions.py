from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class Learn(Action):

    def name(self) -> Text:
        return "action_learn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject = next(tracker.get_latest_entity_values("subject"), None)
        if(subject is None):
            dispatcher.utter_message(text="I'm sorry, I didn't understand the subject.")
            return []
        else:
            dispatcher.utter_message(text="I'm learning {}".format(subject))
            return []
