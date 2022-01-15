import numpy as np
from Startup import Startup

class KnnKMeans:
    def __init__(self, df):
        self.df = df
        self.count = df['state'].count()
        self.startups_objects = self.create_startups_objects(df)
        for i in range(0, 5):
            self.startups_objects[i].to_string()

    def create_startups_objects(self, df):
        count = df['state'].count()
        objects = []
        for i in range(0, count):
            objects.append(Startup(df.loc[i]))
        return objects

    def get_k_closest(self, k):
        print(k)

    def get_distance(self, startup1, startup2):
        return np.sqrt(
            np.pow(startup2.main_category - startup1.main_category, 2)
            + np.pow(startup2.currency - startup1.currency, 2)
            + np.pow(startup2.deadline - startup1.deadline, 2)
            + np.pow(startup2.goal - startup1.goal, 2)
            + np.pow(startup2.launched - startup1.launched, 2)
            + np.pow(startup2.pledged - startup1.pledged, 2)
            + np.pow(startup2.backers - startup1.backers, 2)
            + np.pow(startup2.country - startup1.country, 2)
            + np.pow(startup2.usd_pledged - startup1.usd_pledged, 2)
            + np.pow(startup2.pledged_ratio - startup1.pledged_ratio, 2)
        )


