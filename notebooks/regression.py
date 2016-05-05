import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
import election
import pickle
import csv


class RegressionModel():

    def __init__(self, data, candidateDataMapping, testDataFrame):

        self.clusters = pd.read_csv('../visualization/clustersout.csv')
        # self.clusters = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/visualization/clustersout.csv')
        self.data = data
        self.candidateDataMapping = candidateDataMapping
        self.candidates = candidateDataMapping.keys()
        self.testDataFrame = testDataFrame
        self.countryWideRegressors = {}
        self.electionData = election.Election2016()

        self.BUILD_MODELS = False
        self.CV_FOLDS = 5

    def run(self):
        self.bestRegressors = {'Donald Trump' : [], 'Ted Cruz' : [], 'John Kasich' : []}
        self.regressors = [RandomForestRegressor(n_estimators=100), GradientBoostingRegressor(), AdaBoostRegressor(), LinearRegression()]
        self.clusters = [self.clusters[self.clusters['cluster'] == id]['fips'].values for id in range(4)]
        self.relevantFeatures = ['SEX255214', 'RHI125214', 'RHI225214', 'RHI625214', 'RHI725214', 'RHI825214', 'POP815213', 'EDU635213', 'LFE305213', 'HSG495213', 'HSD310213', 'INC910213', 'PVY020213', 'SBO415207', 'RTN131207', 'LND110210', 'POP060210']
        self.statesThatHaveVoted = ['AL', 'AZ', 'AR', 'CO', 'FL', 'GA', 'ID', 'IL', 'IA', 'KY', 'LA', 'ME', 'MA', 'MI', 'MS', 'MO', 'NE', 'NV', 'NC', 'OH', 'OK', 'SC', 'TN', 'TX', 'UT', 'VT', 'VA', 'NH']



        ##### Identify best regressor for every candidate and cluster #####

        if self.BUILD_MODELS:
            self.performRegression(identifyBestRegressorMode=True)
            with open('bestRegressors.pickle', 'wb') as handle:
                pickle.dump(self.bestRegressors, handle)
        else:
            with open('bestRegressors.pickle', 'rb') as handle:
                self.bestRegressors = pickle.load(handle)




        self.performRegression(identifyBestRegressorMode=False)





        ##### Clusters #####

        if self.BUILD_MODELS:
            with open('clusterResults.pickle', 'wb') as handle:
                pickle.dump(self.clusterResults, handle)
        else:
            with open('clusterResults.pickle', 'rb') as handle:
                self.clusterResults = pickle.load(handle)

        for id in range(4):
            self.clusterResults[id].to_csv('clusterResults_' + str(id) + '.csv', index=False)




        ##### Cluster regressors #####

        with open('regressors_MSE.csv', 'wb') as myfile:
            string = ""
            for candidate in self.candidates:
                string += candidate
                string += ','
                for id in range(4):
                    string += '"' + str(self.bestRegressors[candidate][id][0]) + '"'
                    string += ','
                    string += str(self.bestRegressors[candidate][id][1])
                    string += ','
                string += '\r\n'
            myfile.write(string)



        ##### Country wide regressors #####

        if self.BUILD_MODELS:
            for candidate in self.candidates:
                self.countryWideRegressors[candidate] = (self.identifyBestRegressor(self.regressors, self.candidateDataMapping[candidate][self.relevantFeatures], self.candidateDataMapping[candidate]['fraction_votes'] ))
                with open('countryWideRegressors.pickle', 'wb') as handle:
                    pickle.dump(self.countryWideRegressors, handle)
        else:
            with open('countryWideRegressors.pickle', 'rb') as handle:
                self.countryWideRegressors = pickle.load(handle)


        with open('countryWideRegressor_MSE.csv', 'wb') as myfile:
            string = ""
            for candidate in self.candidates:
                string += candidate
                string += ','
                string += '"' + str(self.countryWideRegressors[candidate][0]) + '"'
                string += ','
                string += str(self.countryWideRegressors[candidate][1])
                string += '\r\n'
            myfile.write(string)


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

                    # get state for fips
                    # check if state has voted


                    # contained in the candidate's results
                    if len(data[data['fips'] == county]) == 1:
                        trainingData.append(data[data['fips'] == county])
                    else:
                        if self.electionData.getStateForFips(county) not in self.statesThatHaveVoted:
                            testData.append(self.testDataFrame[self.testDataFrame['fips'] == county])
                        else:
                            print '2012 election data is not available for county ' + str(county)


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
                    regressor = self.bestRegressors[candidate][clusterId][0]
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
            meanMSE.append((cross_validation.cross_val_score(regressor, trainingData, targetClass, cv=self.CV_FOLDS, scoring='mean_squared_error')).mean())

        return meanMSE

    def identifyBestRegressor(self, regressors, trainingData, targetClass):
        meanMSE = []
        mse = []
        for regressor in regressors:
            result = cross_validation.cross_val_score(regressor, trainingData, targetClass, cv=self.CV_FOLDS, scoring='mean_squared_error')
            mse.append(result)
            meanMSE.append(result.mean())

        return (regressors[meanMSE.index(max(meanMSE))], max(meanMSE))

        # def identifyBestRegressor(self, regressors, trainingData, targetClass):
        # meanMSE = []
        # for regressor in regressors:
        #     meanMSE.append((cross_validation.cross_val_score(regressor, trainingData, targetClass, cv=5, scoring='mean_squared_error')).mean())
        #
        # return regressors[meanMSE.index(max(meanMSE))]

    # TODO finish evaluation over entire country
    def regressorPerformanceForEntireCountry(self, regressor, data):
        tr = cross_validation.cross_val_score(regressor, data[self.relevantFeatures], data['fraction_votes'], cv=self.CV_FOLDS, scoring='mean_squared_error')
        return tr.mean()


    # TODO also look at non ideal cluster models for comparison