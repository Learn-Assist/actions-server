from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import api.api1 as api

class ValidateLearnForm(ValidationAction):

    def name(self) -> Text:
        return "validate_learn_form"

    def validate_subject_learn(
        self,
        slot_value:Any,
        dispatcher: CollectingDispatcher,
        tracker:Tracker,
        domain :  DomainDict
    ) -> Dict[Text,Any]:

        print("\nValidate subject Action\n")
        try:
            if slot_value in api.getSubjects():
                print("validate_subject: {}".format(slot_value))
                return {"subject_learn": slot_value}
            else:
                print("validate_subject else: {}".format(slot_value))
                dispatcher.utter_message(text="I'm sorry, I didn't understand the subject.")
                return {"subject_learn": None}
        except Exception as e:
            print("Error: {}".format(e))
            dispatcher.utter_message(text="I'm sorry, I didn't understand the subject.")
            return {"subject_learn": None}

    def validate_lesson_learn(
        self,
        slot_value:Any,
        dispatcher: CollectingDispatcher,
        tracker:Tracker,
        domain :  DomainDict
    ) -> Dict[Text,Any]:

        print("\nValidate lesson Action\n")
        subject = tracker.get_slot("subject_learn")
        if(int(slot_value)<=api.getLessons(subject)):
            print("validate_lesson: {}".format(slot_value))
            return {"lesson_learn": slot_value}

        else:
            dispatcher.utter_message(text="There are only {} lessons in {}".format(api.getLessons(subject),subject))
            return {"lesson_learn": None}

    def validate_topic_learn(
        self,
        slot_value:Any,
        dispatcher: CollectingDispatcher,
        tracker:Tracker,
        domain :  DomainDict
    ) -> Dict[Text,Any]:

        print("\nValidate topic Action\n")
        subject = tracker.get_slot("subject_learn")
        lesson = tracker.get_slot("lesson_learn")
        grade = tracker.get_slot("grade")
        topics = []
        for topic in api.getTopics(subject,grade,lesson):
            topic = topic.lower()
            topics.append(topic)
        
        if str(slot_value).lower() in topics:
            print("validate_topic: {}".format(slot_value))
            return {"topic_learn": slot_value}
        else:
            topics = ""
            for t in api.getTopics(subject,grade,lesson):
                topics = topics + " " + t
            dispatcher.utter_message(text="I did not get that. Please try again.".format(topics))
            return {"topic_learn": None}


class ValidateTestForm(ValidationAction):

    def name(self) -> Text:
        return "validate_test_form"

    def validate_subject_test(
        self,
        slot_value:Any,
        dispatcher: CollectingDispatcher,
        tracker:Tracker,
        domain :  DomainDict
    ) -> Dict[Text,Any]:

        print("\nValidate subject Action\n")
        try:
            if slot_value in api.getSubjects():
                print("validate_subject: {}".format(slot_value))
                return {"subject_test": slot_value}
            else:
                print("validate_subject else: {}".format(slot_value))
                dispatcher.utter_message(text="I'm sorry, I didn't understand the subject.")
                return {"subject_test": None}
        except Exception as e:
            print("Error: {}".format(e))
            dispatcher.utter_message(text="I'm sorry, I didn't understand the subject.")
            return {"subject_test": 'None'}

    def validate_lesson_test(
        self,
        slot_value:Any,
        dispatcher: CollectingDispatcher,
        tracker:Tracker,
        domain :  DomainDict
    ) -> Dict[Text,Any]:

        print("\nValidate lesson Action\n")
        subject = tracker.get_slot("subject_test")
        if(int(slot_value)<=api.getLessons(subject)):
            print("validate_lesson: {}".format(slot_value))
            return {"lesson_test": slot_value}

        else:
            dispatcher.utter_message(text="There are only {} lessons in {}".format(api.getLessons(subject),subject))
            return {"lesson_test": None}

    def validate_topic_test(
        self,
        slot_value:Any,
        dispatcher: CollectingDispatcher,
        tracker:Tracker,
        domain :  DomainDict
    ) -> Dict[Text,Any]:

        print("\nValidate topic Action\n")
        subject = tracker.get_slot("subject_test")
        lesson = tracker.get_slot("lesson_test")
        grade = tracker.get_slot("grade")
        topics = []
        for topic in api.getTopics(subject,grade,lesson):
            topic = topic.lower()
            topics.append(topic)
        
        if str(slot_value).lower() in topics:
            print("validate_topic: {}".format(slot_value))
            return {"topic_test": slot_value}
        else:
            topics = ""
            for t in api.getTopics(subject,grade,lesson):
                topics = topics + " " + t
            dispatcher.utter_message(text="I did not get that. Please try again.".format(topics))
            return {"topic_test": None}