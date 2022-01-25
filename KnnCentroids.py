import math
import random as rand

class Point:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

    def get_distance(self, point):
        return math.sqrt(
            math.pow(self.x - point.x, 2) + math.pow(self.y - point.y, 2)
        )

class KnnBase:
    def __init__(self, df):
        self.df = df
        self.count = df['state'].count()
        self.items_objects = self.create_startups_objects(df)

    def create_startups_objects(self, df, clear_state=False):
        count = df['state'].count()
        objects = []
        for i in range(0, count):
            obj = Point(df.iloc[i])
            if clear_state:
                obj.state = None
            objects.append(obj)
        return objects

class KnnCentroids(KnnBase):
    def __init__(self, df):
        super().__init__(df)
        self.create_startups_objects(df, True)
        self.clusters = []
        self.generate_random_clusters()
        self.train()

    def train(self):
        print('====== Training ======')
        for cluster in self.clusters:
            print(cluster.to_string())

        points_changed = self.match_point_to_clusters()
        counter = 0
        while points_changed and counter < 1000000:
            counter += 1
            self.reposition_clusters()
            points_changed = self.match_point_to_clusters()
            print(f'\n   {counter} iteration points changed: {points_changed}')
            for cluster in self.clusters:
                print(f'   {cluster.to_string()}')

    def generate_random_clusters(self):
        clusters =  []
        for i in [0, 1]:
            x = rand.randint(0, 10)
            state = i
            backers = rand.randint(0, 10)
            clusters.append(
                Point()
            )

        self.clusters = clusters

    def reposition_clusters(self):
        for cluster in self.clusters:
            pledged_sum = 0
            backers_sum = 0
            pledged_ratio_sum = 0
            count = 0

            for item in self.items_objects:
                if item.state == cluster.state:
                    pledged_sum += item.pledged
                    backers_sum += item.backers
                    pledged_ratio_sum += item.pledged_ratio
                    count += 1

            if count > 0:
                cluster.pledged = pledged_sum
                cluster.backers = backers_sum
                cluster.pledged_ratio = pledged_ratio_sum

    def match_point_to_clusters(self):
        changed = 0
        for item in self.items_objects:
            current_distance = None
            current_state = item.state
            new_state = None

            for cluster in self.clusters:
                new_state = cluster.state
                new_distance = item.get_distance_from(cluster)
                if current_distance is None:
                    current_distance = new_distance + 1

                # print(f'{new_distance}___{current_distance}')
                if new_distance < current_distance:
                    item.state = new_state

            if current_state != new_state:
                changed += 1

        return changed

    def classify(self, item, print_result=True):
        distance = None
        item_class = None
        for cluster in self.clusters:
            new_distance = item.get_distance_from(cluster)
            new_item_class = cluster.state

            if distance is None:
                distance = new_distance
            if item_class is None:
                item_class = new_item_class
            if distance is not None and distance < new_distance:
                item_class = new_item_class
        if print_result:
            print(f'Item classified as {item_class}')

        return item_class