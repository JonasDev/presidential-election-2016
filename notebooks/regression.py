import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression


class RegressionModel():

    def __init__(self, data, candidateDataMapping, testDataFrame):

        self.clusters = pd.read_csv('../visualization/clustersout.csv')
        # self.clusters = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/visualization/clustersout.csv')
        self.data = data
        self.candidateDataMapping = candidateDataMapping
        self.candidates = candidateDataMapping.keys()
        self.testDataFrame = testDataFrame

    def performRegression(self):

    # TODO extra class
    # def buildRegressionModel(self, data, candidateDataMapping):
        # TODO fill in county-clusters
        # cluster = [1001, 1003, 1005, 1007]
        self.clusters = [self.clusters[self.clusters['cluster'] == id]['fips'].values for id in range(4)]
        # cluster = self.clusters[clusters['cluster'] == 0]['fips'].values

        self.clusterPredictions = {}

        relevantFeatures = ['SEX255214', 'RHI125214', 'RHI225214', 'RHI625214', 'RHI725214', 'RHI825214', 'POP815213', 'EDU635213', 'LFE305213', 'HSG495213', 'HSD310213', 'INC910213', 'PVY020213', 'SBO415207', 'RTN131207', 'LND110210', 'POP060210']


        # predictionResults['fips'] = testDataFrame['fips']

        self.clusterResults = []


        # w, h = 20, 4.
        # mse = [[0 for x in range(w)] for y in range(h)]
        self.mse = []

        for clusterId, cluster in enumerate(self.clusters):

            predictions = {}
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

                if test.empty:
                    print "Empty test set"
                    continue

                targetClass = training['fraction_votes']
                # targetClass = np.array(targetClass).astype(float)


                training = training[relevantFeatures]
                test = test[relevantFeatures]


                # build regression model
                # regressor = RandomForestRegressor(n_estimators = 100)
                # regressor = GradientBoostingRegressor()
                regressor = AdaBoostRegressor()
                # regressor = LinearRegression(normalize=True)

                # regressor = \
                regressor.fit(training, targetClass)
                # output = regressor.predict(test)
                # TODO remove
                # test = training
                output = regressor.predict(test)
                # accuracy = regressor.score(training, targetClass)

                # save predictions
                # d = {'fips' : test['fips'], 'fraction_votes' : test['fraction_votes'], 'predictions' : output}
                d = {'predictions' : output}
                predictions[candidate] = pd.DataFrame(data = d)

                # columnName = str(clusterId) + '_' + candidate
                predictionResults[candidate] = output

                # TODO add flag to disable benchmark
                # regressors = [RandomForestRegressor(n_estimators=100), GradientBoostingRegressor(), AdaBoostRegressor(), LinearRegression()]
                # benchmarks[candidate] = (self.benchmarkRegressors(regressors, training, targetClass))
                benchmarks[candidate] = -1

                # if candidate == 'Donald Trump':
                #     mse.append(benchmarkRegressors([RandomForestRegressor(n_estimators=100), GradientBoostingRegressor(), AdaBoostRegressor(), LinearRegression()], training, targetClass))

            self.mse.append(benchmarks)
            self.clusterResults.append(predictionResults)
            self.clusterPredictions[clusterId] = predictions

    # finished = 1

    # print predictionResults

    def benchmarkRegressors(self, regressors, trainingData, targetClass):
        meanMSE = []
        for regressor in regressors:
            meanMSE.append((cross_validation.cross_val_score(regressor, trainingData, targetClass, cv=5, scoring='mean_squared_error')).mean())

        return meanMSE