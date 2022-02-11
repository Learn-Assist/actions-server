from requests import get
import json
#URL = "https://learn-assist-database-amnjutsbkq-el.a.run.app"
URL = "http://localhost:8080"


def getSubjects():
    subjects = get(URL+"/subject?grade=1")
    subjects = json.loads(subjects.content)
    result = []
    for subject in subjects:
        result.append(subject["name"])
    return result


def getLessons(subject) -> int:
    subject = str(subject).lower()
    if subject == "english":
        return 5
    elif subject == "social":
        return 5
    elif subject == "science":
        return 5
    else:
        return 0


def getTopics(subject, grade, lesson):
    topics = get(URL+"/topic?subject="+subject+"&grade=" +
                 str(grade)+"&lesson="+str(lesson))
    topics = json.loads(topics.content)
    result = []
    for topic in topics:
        result.append(topic["name"])
    return result


def getTopic(subject, lesson, grade, name):
    topics = get(URL+"/topic?subject="+str(subject) +
                 "&grade="+str(grade)+"&lesson="+str(lesson))
    topics = json.loads(topics.content)
    for topic in topics:
        if str(topic["subject"]).lower() == str(subject).lower() and str(topic["lesson"]) == str(lesson) and str(topic["name"]).lower() == str(name.lower()):
            return topic
