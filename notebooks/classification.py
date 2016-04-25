import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn import preprocessing
from sklearn import cross_validation

import classification
# from classification import Election2016
from classification import RegressionModel

# county facts
from sklearn.linear_model import LinearRegression


def main():
    # election = Election2016()
    # election.run()

if __name__ == "__main__": main()








# TODO
# benchmark different models
# identify best model for every candidate / cluster
# take best if exists, or separate models if it makes a significant difference

# remove states (fips = 2000 etc) from test set
