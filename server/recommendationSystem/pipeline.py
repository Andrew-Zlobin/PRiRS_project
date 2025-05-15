from sklearn.cluster import KMeans
from scipy.spatial.distance import cosine
import numpy as np

from collections import Counter
from math import floor


class recommendationModel:
    def __init__(self, database):
        self.database = database
        self.cached_tasks = None
        


    def cluster_users(self, users, n_clusters=4):
        data = np.array(users)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(data)
        return labels

    # типа для каждой группы пользователей посчитать среднее по скорам и выбрать пропорциональном этим скорам число заданий той или иной категории?
    # 

    def update_cached_tasks_list(self):
        self.cached_tasks = self.database.get_all_tasks_types_and_ids()

    # так, здесь мы представляем что мы работаем с группой пользователей как с одним
    # и пытаемся для него (группы) получить список idшников заданий, которые им подходят
    def create_task_query (self, user_group_scores, strategy="balanced", n=10):
        # strategy could be also confidence and challenge

        tasks = self.cached_tasks
        # tasks = [(id, type, difficulty)]
        scored_tasks = []
    
        for task in tasks:
            id = task[0]
            error_type = task[1].strip()
            difficulty = task[2]
            user_error_rate = user_group_scores.get("user_score_reading_" + error_type, 0)

            risk_score = user_error_rate * difficulty
            
            if strategy == "confidence":
                adjusted_score = -risk_score  # Prefer lower risk tasks
            elif strategy == "challenge":
                adjusted_score = risk_score  # Prefer high-risk tasks
            else:  # "balanced"
                adjusted_score = risk_score if difficulty > 2 else risk_score * 0.8
            
            scored_tasks.append((adjusted_score, task))
        # print("before sorting :", scored_tasks)
        scored_tasks.sort()#reverse=(strategy != "confidence"))
        # print("after sorting :", scored_tasks)
        print()
        # task -> (score, (id, type, difficulty))
        return [task for _, task in scored_tasks[:n]]


    def sort_task_query(self, user_group_scores, task_query):
        tasks = task_query
        print(tasks)
        # insertion, skipping, phoneme, accent
        target_vector = [5 * user_group_scores["user_score_reading_insertion"], 
                         5 * user_group_scores["user_score_reading_skipping"], 
                         5 * user_group_scores["user_score_reading_phoneme"], 
                         5 * user_group_scores["user_score_reading_accent"], 
        ]
        # (tasks: List[Dict], user_difficulty_avg: float) -> List[Dict]:
        # print([task[0] if task[1][1] == "insertion" else 0, \
        #                  task[0] if task[1][1] == "skipping" else 0, \
        #                     task[0] if task[1][1] == "phoneme" else 0, \
        #                         task[0] if task[1][1] == "accent" else 0], [target_vector])
        sorted_tasks = sorted(tasks, key=lambda task: float(cosine([task[0] if task[1] == "insertion" else 0, \
                         task[2] if task[1] == "skipping" else 0, \
                            task[2] if task[1] == "phoneme" else 0, \
                                task[2] if task[1] == "accent" else 0], target_vector)))
        return sorted_tasks

    # "scores" : {"user_score_grammar" : data[5],
    #             "user_score_listenning" : data[6],
    #             "user_score_reading_insertion" : data[7],
    #             "user_score_reading_skipping" : data[8],
    #             "user_score_reading_phoneme" : data[9],
    #             "user_score_reading_accent" : data[10],
    #             "user_group_id" : data[11],}
    def update_score_for_user(self, user, sentence : str, errors : dict):
        # print("errors", errors["error_types"])
        errors_counter = Counter(errors["error_types"])
        # print(errors_counter)
        new_scores = {}
        sentence_len = len(sentence.split()) * 5
        if "replace" in errors_counter.keys():
            new_scores["user_score_reading_phoneme"] = floor((
                user["scores"]["user_score_reading_phoneme"] / 100 
                - errors_counter["replace"] / sentence_len) * 100)
        else:
            new_scores["user_score_reading_phoneme"] = \
                user["scores"]["user_score_reading_phoneme"] + 1

        if "delete" in errors_counter.keys():
            new_scores["user_score_reading_skipping"] = floor((
                user["scores"]["user_score_reading_skipping"] / 100 
                - errors_counter["delete"] / sentence_len) * 100)
        else:
            new_scores["user_score_reading_skipping"] = \
                user["scores"]["user_score_reading_skipping"] + 1
            
        if "insert" in errors_counter.keys():
            new_scores["user_score_reading_insertion"] = floor((
                user["scores"]["user_score_reading_insertion"] / 100 
                - errors_counter["insert"] / sentence_len) * 100)
        else:
            new_scores["user_score_reading_insertion"] = \
                user["scores"]["user_score_reading_insertion"] + 1
        print(new_scores)
        self.database.update_metrics_for_user_by_email(email=user["email"], scores=new_scores)
    
    def proccess(self):
        self.update_cached_tasks_list()
        all_users = self.database.get_all_users()
        clusters = self.cluster_users([list(user["scores"].values()) for user in all_users], n_clusters=5)
        for user, cluster in zip(all_users, clusters):
            self.database.update_metrics_for_user_by_email(email=user["email"], user_group_id=int(cluster))
        # for user in users:
        stats_test_parameter = None
        mean_scores = []
        tasks = {}
        sorted_tasks = {}
        for cluster in set(clusters):
            mean_score = {
                "user_score_reading_insertion" : 0,
                "user_score_reading_skipping" : 0,
                "user_score_reading_phoneme" : 0,
                "user_score_reading_accent" : 0,
            }
            counter = 0
            for user, user_cluster in zip(all_users, clusters):
                if user_cluster == cluster:
                    counter += 1
                    for score in mean_score.keys():
                        # print(user["scores"])
                        mean_score[score] += user["scores"][score]
            for score in mean_score.keys():
                # print(user["scores"])
                mean_score[score] /= counter
                
            mean_scores.append(mean_score)
            tasks[cluster] = self.create_task_query(mean_score)
            sorted_tasks[cluster]  = self.sort_task_query(mean_score, tasks[cluster])
            for user, user_cluster in zip(all_users, clusters):
                if user_cluster == cluster:
                    self.database.close_all_tasks_for_user_by_email(user["email"])
                    if user["id"] == 1:
                        stats_test_parameter = mean_score
                    for task in sorted_tasks[cluster]:
                        if not self.database.check_if_task_is_passed_by_user(user["id"], task[0]):
                            self.database.set_task_to_user(user["id"], task[0])
        return stats_test_parameter
        
    def evaluate_errors(self, user, comparation_res):
        # user = self.database.get_user("test@test.com")
        print("evaluatin starts")
        current_task = self.database.get_task_for_user(email=user['email'])[0]
        print("comparation res = ", comparation_res)
        print("task = ", current_task)
        self.database.close_task_for_user(user["id"], current_task["key"])
        print("try to set passed task")
        self.database.set_task_passed_by_user(user["id"], current_task["key"], 1)
        print("successfully set passed task")
        self.update_score_for_user(user, current_task["text"], comparation_res)
        
        mean_scores = self.proccess()
        user = self.database.get_user("test@test.com")
        print("updated user : ", user)


objects = [
    (1, 2, 3, 4, 5, 6),
    (2, 3, 4, 5, 6, 7),
    (10, 12, 14, 16, 18, 20),
    (11, 13, 15, 17, 19, 21),
    (50, 52, 54, 56, 58, 60)
]

    
