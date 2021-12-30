from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from requests import get
import api.api1 as api
import json

class ActionInitConversation(Action):
    def name(self) -> Text:
        return "action_init_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Sender_ID: ", tracker.sender_id)
        uid = tracker.sender_id
        name = "Guest"
        grade = "1"
        try:
            if uid == None or uid == "" or not uid or uid == "default":
                SlotSet("name", "Guest")
                SlotSet("grade",grade)
            else:
                user = get("http://localhost:6001/user/{}".format(uid))
                user = json.loads(user.content)
                name = user["name"]
                SlotSet("name", user["name"])
                SlotSet("grade", user["grade"])
        except Exception as err:
            print("Error {}".format(err))
        dispatcher.utter_message(text="Hello {}! ".format(name))
        return []

class ActionAskSubjectLearnForm(Action):
    def name(self) -> Text:
        return "action_ask_subject_learn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("\nAsk subject Action\n")
        
        message = "What subject do you want to learn? The available subjects are:"
        subjects = api.getSubjects()
        for subject in subjects:
            print("Subject: {}".format(subject))
            message = message + " " + subject

        print("message: {}".format(message))
        dispatcher.utter_message(text=message)
        return []

class ActionAskLessonLearnForm(Action):
    def name(self) -> Text:
        return "action_ask_lesson_learn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("\nAsk lesson Action\n")
        subject = tracker.get_slot("subject_learn")
        message = "Which lesson in {} do you want to learn? There are {} lessons in {}:".format(subject,api.getLessons(subject),subject)
        dispatcher.utter_message(text=message)
        return []

class ActionAskTopicLearnForm(Action):
    def name(self) -> Text:
        return "action_ask_topic_learn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("\nAsk topic Action\n")
        subject = tracker.get_slot("subject_learn")
        message = "What topic do you want to learn? The available topics are: " 
        grade = tracker.get_slot("grade")
        lesson = tracker.get_slot("lesson_learn")
        if not grade: 
            grade = 1
        topics = api.getTopics(subject,grade,lesson)
        for topic in topics:
            message = message + "  " + topic
        dispatcher.utter_message(text=message)
        return []



class ActionSubmitLearnForm(Action):
    def name(self) -> Text:
        return "action_submit_learn_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject = tracker.get_slot("subject_learn")
        lesson = tracker.get_slot("lesson_learn")
        topic_slot = tracker.get_slot("topic_learn")
        message = ""
        topic = api.getTopic(subject, lesson, 1, topic_slot)
        print("Topic submit: {}".format(topic))
        contents = topic["contents"]
        for content in contents:
            if(content["type"]=="text"):
                message = message + "\n" + content["content"]
        dispatcher.utter_message(text=message)
        return []

