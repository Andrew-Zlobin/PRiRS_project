import random
import uuid

from math import trunc


def generate_random_scores(scores_counter=6, score_range=(0,100)):
    random.seed(42)
    return [trunc(random.random() * (score_range[1] - score_range[0]) + score_range[0]) for _ in range(scores_counter)]


def generate_uniq_strings(temlplates : list):
    return [f"{temlplate}_{uuid.uuid1()}" for tamplate in temlplates]

class User ():
    def __init__(name=None,\
                email=None,\
                password=None,\
                age=None,\
                user_score_grammar=None,\
                user_score_listenning=None,\
                user_score_reading_insertion=None,\
                user_score_reading_skipping=None,\
                user_score_reading_phoneme=None,\
                user_score_reading_accent=None,\
                user_group_id=None,\
                created_at=None):
        if name == None:
            name = 