from sklearn.preprocessing import StandardScaler
import numpy as np


class PcaAnalyzer:
    def __init__(self, dataframe, features, labels):
        self.df = dataframe
        self.features = features
        self.labels = labels
        self.scaler = StandardScaler()

    def perform_pca_analysis(self):
        # Map categories and countries to number values
        print(self.features)
        features_scaled = self.scaler.fit_transform(self.features)
        covariance_matrix = np.cov(features_scaled.T)
        eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix)
        print(f'Eigen values:\n{eigen_values}')

        # Project data onto Eigen vector
        projected = features_scaled.dot(eigen_vectors.T[0])
        print(projected)
