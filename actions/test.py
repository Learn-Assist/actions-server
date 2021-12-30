from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from requests import get
import api.api1 as api
import json


class ActionAskSubjectTestForm(Action):
    def name(self) -> Text:
        return "action_ask_subject_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("\nAsk subject Action\n")
        
        message = "In which subject do you want to take thetest? The available subjects are:"
        subjects = api.getSubjects()
        for subject in subjects:
            print("Subject: {}".format(subject))
            message = message + " " + subject

        print("message: {}".format(message))
        dispatcher.utter_message(text=message)
        return []

class ActionAskLessonTestForm(Action):
    def name(self) -> Text:
        return "action_ask_lesson_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("\nAsk lesson Action\n")
        subject = tracker.get_slot("subject_test")
        message = "I which lesson in {} do you want to take the test? There are {} lessons in {}:".format(subject,api.getLessons(subject),subject)
        dispatcher.utter_message(text=message)
        return []

class ActionAskTopicTestForm(Action):
    def name(self) -> Text:
        return "action_ask_topic_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("\nAsk topic Action\n")
        subject = tracker.get_slot("subject_test")
        message = "In which topic do you want to take the test? The available topics are: " 
        grade = tracker.get_slot("grade_test")
        lesson = tracker.get_slot("lesson_test")
        if not grade: 
            grade = 1
        topics = api.getTopics(subject,grade,lesson)
        for topic in topics:
            message = message + "  " + topic
        dispatcher.utter_message(text=message)
        return []



class ActionSubmitTestForm(Action):
    def name(self) -> Text:
        return "action_submit_test_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject = tracker.get_slot("subject_test")
        lesson = tracker.get_slot("lesson_test")
        topic_slot = tracker.get_slot("topic_test")
        message = ""
        topic = api.getTopic(subject, lesson, 1, topic_slot)
        print("Topic submit: {}".format(topic))
        contents = topic["contents"]
        for content in contents:
            if(content["type"]=="text"):
                message = message + "\n" + content["content"]
        dispatcher.utter_message(text=message)
        return []