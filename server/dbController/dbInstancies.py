import random
import uuid

from math import trunc
import warnings


def generate_random_scores(scores_counter=6, score_range=(0,100)):
    random.seed(42)
    return [trunc(random.random() * (score_range[1] - score_range[0]) + score_range[0]) for _ in range(scores_counter)]


scores_keys_template = ["user_score_grammar", "user_score_listenning", 
        "user_score_reading_insertion", "user_score_reading_skipping", 
        "user_score_reading_phoneme", "user_score_reading_accent"]


class User():
    def __init__(name:str=None, email:str=None, 
    password:str=None, age:int=None, scores : dict=None):
        user_uuid = str(uuid.uuid1())
        if name is None:
            warnings.warn("Name was unset")
            name = "Name_{uid}".format(uid=user_uuid)
        if email is None:
            warnings.warn("Name was unset")
            email = "email_{uid}@mail.com".format(uid=user_uuid)
        if password is None:
            warnings.warn("Name was unset")
            password = "pswd"
        if age == None:
            age = random.randint(20, 60)
        if scores is None:
            scores = dict(zip(scores_keys_template, 
            generate_random_scores(scores_counter=len(scores_keys_template))))

        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.scores = scores
        

task_types = {0 : "reading"}

class Task():
    def __init__(name:str, text:str, type:int, difficulty:int):
        self.name = name
        self.text = text
        self.type = type
        self.difficulty = difficulty
