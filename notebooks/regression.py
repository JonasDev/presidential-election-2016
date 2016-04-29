import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
import pickle

# TODO


class RegressionModel():

    def __init__(self, data, candidateDataMapping, testDataFrame):

        self.clusters = pd.read_csv('../visualization/clustersout.csv')
        # self.clusters = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/visualization/clustersout.csv')
        self.data = data
        self.candidateDataMapping = candidateDataMapping
        self.candidates = candidateDataMapping.keys()
        self.testDataFrame = testDataFrame

    def run(self):
        self.bestRegressors = {'Donald Trump' : [], 'Ted Cruz' : [], 'John Kasich' : []}
        self.regressors = [RandomForestRegressor(n_estimators=100), GradientBoostingRegressor(), AdaBoostRegressor(), LinearRegression()]
        self.clusters = [self.clusters[self.clusters['cluster'] == id]['fips'].values for id in range(4)]
        self.relevantFeatures = ['SEX255214', 'RHI125214', 'RHI225214', 'RHI625214', 'RHI725214', 'RHI825214', 'POP815213', 'EDU635213', 'LFE305213', 'HSG495213', 'HSD310213', 'INC910213', 'PVY020213', 'SBO415207', 'RTN131207', 'LND110210', 'POP060210']

        # flag to load from file instead of benchmark every time
        with open('bestRegressors.pickle', 'rb') as handle:
            self.bestRegressors = pickle.load(handle)
        # self.performRegression(identifyBestRegressorMode=True)
        # with open('bestRegressors.pickle', 'wb') as handle:
        #     pickle.dump(self.bestRegressors, handle)

        self.performRegression(identifyBestRegressorMode=False)


        # for id in range(4):
        #     self.clusterResults[id]['fips'] = self.clusters[id]

        with open('clusterResults.pickle', 'wb') as handle:
            pickle.dump(self.clusterResults, handle)

        for id in range(4):
            self.clusterResults[id].to_csv('clusterResults_' + str(id) + '.csv', index=False)


    def performRegression(self, identifyBestRegressorMode = False):

        self.clusterPredictions = {}



        # predictionResults['fips'] = testDataFrame['fips']

        self.clusterResults = []



        # w, h = 20, 4.
        # mse = [[0 for x in range(w)] for y in range(h)]
        self.mse = []

        for clusterId, cluster in enumerate(self.clusters):

            predictions = {}
            testFips = []
            predictionResults = pd.DataFrame()

            benchmarks = pd.DataFrame()

            # loop through candidates
            for candidate in self.candidates:

                trainingData = []
                testData = []

                data = self.candidateDataMapping[candidate]

                # assign county to training or test set
                for county in cluster:
                    # countyData = data[data['fips'] == county]
                    # if countyData['voted'].iloc[0] == 1:

                    # contained in the candidate's results
                    if len(data[data['fips'] == county]) == 1:
                        trainingData.append(data[data['fips'] == county])
                    else:
                        testData.append(self.testDataFrame[self.testDataFrame['fips'] == county])


                training = pd.concat(trainingData)
                test = pd.concat(testData)

                testFips = test['fips']

                if test.empty:
                    print "Empty test set"
                    continue

                targetClass = training['fraction_votes']
                # targetClass = np.array(targetClass).astype(float)


                training = training[self.relevantFeatures]
                test = test[self.relevantFeatures]

                if identifyBestRegressorMode:
                    self.bestRegressors[candidate].append(self.identifyBestRegressor(self.regressors, training, targetClass))
                else:
                    regressor = self.bestRegressors[candidate][clusterId]
                    regressor.fit(training, targetClass)
                    output = regressor.predict(test)
                    d = {'predictions' : output}
                    predictions[candidate] = pd.DataFrame(data = d)
                    predictionResults[candidate] = output


                # if candidate == 'Donald Trump':
                #     mse.append(benchmarkRegressors([RandomForestRegressor(n_estimators=100), GradientBoostingRegressor(), AdaBoostRegressor(), LinearRegression()], training, targetClass))
            predictionResults['fips'] = testFips.values
            self.mse.append(benchmarks)
            self.clusterResults.append(predictionResults)
            self.clusterPredictions[clusterId] = predictions
        finished = 1

        # if identifyBestRegressorMode:
        #     return

    # finished = 1

    # print predictionResults

    def benchmarkRegressors(self, regressors, trainingData, targetClass):
        meanMSE = []
        for regressor in regressors:
            meanMSE.append((cross_validation.cross_val_score(regressor, trainingData, targetClass, cv=5, scoring='mean_squared_error')).mean())

        return meanMSE

    def identifyBestRegressor(self, regressors, trainingData, targetClass):
        meanMSE = []
        for regressor in regressors:
            meanMSE.append((cross_validation.cross_val_score(regressor, trainingData, targetClass, cv=5, scoring='mean_squared_error')).mean())

        return regressors[meanMSE.index(max(meanMSE))]

    # TODO finish evaluation over entire country
    # def regressorPerformanceForEntireCountry(self, regressor, data):
    #     tr = cross_validation.cross_val_score(regressor, data[self.relevantFeatures], data['fraction_votes'], cv=5, scoring='mean_squared_error')
    #     return tr.mean()