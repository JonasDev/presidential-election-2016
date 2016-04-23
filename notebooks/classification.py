import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn import preprocessing
from sklearn import cross_validation

# county facts
from sklearn.linear_model import LinearRegression

cf = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/county_facts.csv')



# 2016 primary results
pr = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/primary_results.csv')

clusters = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/visualization/clustersout.csv')

# only consider the republican party
pr = pr[pr['party'] == 'Republican']

# identify states that have already voted
# statesAlreadyVoted = pr['state_abbreviation'].unique()

pr.drop('state_abbreviation', axis = 1, inplace=True)

# merge county facts with 2016 primary results
data = pd.merge(cf, pr, on='fips', how='left')
# data = pd.merge(cf, pr, on='fips', how='inner')

# encode string as number for regression
le = preprocessing.LabelEncoder()
le.fit(data['state_abbreviation'])
states = le.transform(data['state_abbreviation'])
data['state_number'] = states
data.drop('state_abbreviation', axis = 1, inplace=True)

# removes information aggregated on state level
data = data[data.state_number != 0]

# remove unnecessary data
data.drop('area_name', axis = 1, inplace=True)
data.drop('county', axis = 1, inplace=True)
data.drop('state', axis = 1, inplace=True)
data.drop('party', axis = 1, inplace=True)
data.drop('votes', axis = 1, inplace=True)



# introduce voted column TODO: fill in correctly
data['voted'] = 0

### 10466 rows

# data.loc[data['fips'] == 1001,'voted'] = 1
# data.loc[data['fips'] == 1003,'voted'] = 1

# statesAlreadyVoted = pr['fips'].values
# for county in statesAlreadyVoted:
#     # data[data['fips'] == county].loc
#     data.loc[data['fips'] == county,'voted'] = 1
data.loc[data['candidate'].isnull(), 'voted'] = 0

testDataFrame = data[data['candidate'].isnull()]
# testDataFrame.dropna(axis=1, inplace=True)
testDataFrame.drop('candidate', axis=1, inplace=True)
testDataFrame.fillna(value=0, inplace=True)


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


# TODO fill in county-clusters
# cluster = [1001, 1003, 1005, 1007]
clusters = [clusters[clusters['cluster'] == id]['fips'].values for id in range(4)]
# cluster = clusters[clusters['cluster'] == 0]['fips'].values

clusterPredictions = {}

relevantFeatures = ['SEX255214', 'RHI125214', 'RHI225214', 'RHI625214', 'RHI725214', 'RHI825214', 'POP815213', 'EDU635213', 'LFE305213', 'HSG495213', 'HSD310213', 'INC910213', 'PVY020213', 'SBO415207', 'RTN131207', 'LND110210', 'POP060210']


# predictionResults['fips'] = testDataFrame['fips']

clusterResults = []


# w, h = 20, 4.
# mse = [[0 for x in range(w)] for y in range(h)]
mse = []

# for idx, val in enumerate(ints):
for clusterId, cluster in enumerate(clusters):

    predictions = {}
    predictionResults = pd.DataFrame()

    benchmarks = pd.DataFrame()

    # loop through candidates
    for candidate in candidates:

        trainingData = []
        testData = []

        data = candidateDataMapping[candidate]

        # assign county to training or test set
        for county in cluster:
            # countyData = data[data['fips'] == county]
            # if countyData['voted'].iloc[0] == 1:

            # contained in the candidate's results
            if len(data[data['fips'] == county]) == 1:
                trainingData.append(data[data['fips'] == county])
            else:
                testData.append(testDataFrame[testDataFrame['fips'] == county])


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

        benchmarks[candidate] = (benchmarkRegressors([RandomForestRegressor(n_estimators=100), GradientBoostingRegressor(), AdaBoostRegressor(), LinearRegression()], training, targetClass))

        # if candidate == 'Donald Trump':
        #     mse.append(benchmarkRegressors([RandomForestRegressor(n_estimators=100), GradientBoostingRegressor(), AdaBoostRegressor(), LinearRegression()], training, targetClass))

    mse.append(benchmarks)
    clusterResults.append(predictionResults)
    clusterPredictions[clusterId] = predictions

finished = 1

# print predictionResults

def benchmarkRegressors(regressors, trainingData, targetClass):
    meanMSE = []
    for regressor in regressors:
        meanMSE.append((cross_validation.cross_val_score(regressor, trainingData, targetClass, cv=5, scoring='mean_squared_error')).mean())

    return meanMSE



# TODO
# benchmark different models
# identify best model for every candidate / cluster
# take best if exists, or separate models if it makes a significant difference

# remove states (fips = 2000 etc) from test set
