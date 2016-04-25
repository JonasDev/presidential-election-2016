import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn import preprocessing
from sklearn import cross_validation

from regression import RegressionModel

class Election2016:

    def __init__(self):
        test = 1

    def run(self):
        self.loadDataSets()
        self.preprocessDataSets()
        self.candidateDataMapping = self.setupCandidates(self.data)

        self.regressor = RegressionModel(self.data, self.candidateDataMapping, self.testDataFrame)
        self.regressor.performRegression()


    def loadDataSets(self):
        # self.cf = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/county_facts.csv')
        self.cf = pd.read_csv('../2016_presidential_election_v5/county_facts.csv')

        # 2016 primary results
        self.pr = pd.read_csv('../2016_presidential_election_v5/primary_results.csv')
        # self.pr = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/primary_results.csv')

        # self.clusters = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/visualization/clustersout.csv')

    def encodeStrings(self, data):
        # encode string as number for regression
        le = preprocessing.LabelEncoder()
        le.fit(data['state_abbreviation'])
        states = le.transform(data['state_abbreviation'])
        data['state_number'] = states
        data.drop('state_abbreviation', axis = 1, inplace=True)
        return data

    def setupTestSet(self, data):
        testDataFrame = data[data['candidate'].isnull()]
        # testDataFrame.dropna(axis=1, inplace=True)
        testDataFrame.drop('candidate', axis=1, inplace=True)
        testDataFrame.fillna(value=0, inplace=True)
        return testDataFrame

    def preprocessDataSets(self):
        # only consider the republican party
        self.pr = self.pr[self.pr['party'] == 'Republican']

        # identify states that have already voted
        # statesAlreadyVoted = pr['state_abbreviation'].unique()

        self.pr.drop('state_abbreviation', axis = 1, inplace=True)

        # merge county facts with 2016 primary results
        self.data = pd.merge(self.cf, self.pr, on='fips', how='left')
        # data = pd.merge(cf, pr, on='fips', how='inner')

        self.data = self.encodeStrings(self.data)

         # removes information aggregated on state level
        self.data = self.data[self.data.state_number != 0]

        self.data = self.removeUnnecessaryFeatures(self.data)

        # TODO check voted
        # self.data['voted'] = 0
        self.data['voted'] = 1

        self.data.loc[self.data['candidate'].isnull(), 'voted'] = 0

        self.testDataFrame = self.setupTestSet(self.data)



    def removeUnnecessaryFeatures(self, data):
        # remove unnecessary data
        data.drop('area_name', axis = 1, inplace=True)
        data.drop('county', axis = 1, inplace=True)
        data.drop('state', axis = 1, inplace=True)
        data.drop('party', axis = 1, inplace=True)
        data.drop('votes', axis = 1, inplace=True)
        return data

    def setupCandidates(self, data):
        # GOP candidates
        candidates = ['Donald Trump', 'Ted Cruz', 'John Kasich']

        # split up data for every candidate
        trumpData = data[data['candidate'] == 'Donald Trump']
        trumpData.drop('candidate', axis=1, inplace=True)
        ### 1881 rows

        cruzData = data[data['candidate'] == 'Ted Cruz']
        cruzData.drop('candidate', axis=1, inplace=True)

        kasichData = data[data['candidate'] == 'John Kasich']
        kasichData.drop('candidate', axis=1, inplace=True)

        candidateDataMapping = {'Donald Trump' : trumpData, 'Ted Cruz' : cruzData, 'John Kasich' : kasichData}
        return candidateDataMapping





    # introduce voted column TODO: fill in correctly
    # self.data['voted'] = 0

    ### 10466 rows

    # data.loc[data['fips'] == 1001,'voted'] = 1
    # data.loc[data['fips'] == 1003,'voted'] = 1

    # statesAlreadyVoted = pr['fips'].values
    # for county in statesAlreadyVoted:
    #     # data[data['fips'] == county].loc
    #     data.loc[data['fips'] == county,'voted'] = 1
    # self.data.loc[self.data['candidate'].isnull(), 'voted'] = 0
    #
    # testDataFrame = data[data['candidate'].isnull()]
    # # testDataFrame.dropna(axis=1, inplace=True)
    # testDataFrame.drop('candidate', axis=1, inplace=True)
    # testDataFrame.fillna(value=0, inplace=True)
