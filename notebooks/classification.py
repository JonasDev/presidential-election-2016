import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

# county facts
cf = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/county_facts.csv')

# 2016 primary results
pr = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/primary_results.csv')

# only consider the republican party
pr = pr[pr['party'] == 'Republican']

# identify states that have already voted
statesAlreadyVoted = pr['state_abbreviation'].unique()

pr.drop('state_abbreviation', axis = 1, inplace=True)

# merge county facts with 2016 primary results
data = pd.merge(cf, pr, on='fips', how='left')

# remove unnecessary data
data.drop('area_name', axis = 1, inplace=True)
data.drop('county', axis = 1, inplace=True)
data.drop('state', axis = 1, inplace=True)
data.drop('party', axis = 1, inplace=True)

# encode string as number for regression
le = preprocessing.LabelEncoder()
le.fit(data['state_abbreviation'])
states = le.transform(data['state_abbreviation'])
data['state_number'] = states
data.drop('state_abbreviation', axis = 1, inplace=True)

# introduce voted column TODO: fill in correctly
data['voted'] = 0
data.loc[data['fips'] == 1001,'voted'] = 1
data.loc[data['fips'] == 1003,'voted'] = 1

# GOP candidates
candidates = ['Donald Trump', 'Ted Cruz', 'John Kasich']

# split up data for every candidate
trumpData = data[data['candidate'] == 'Donald Trump']
trumpData.drop('candidate', axis=1, inplace=True)

cruzData = data[data['candidate'] == 'Ted Cruz']
cruzData.drop('candidate', axis=1, inplace=True)

kasichData = data[data['candidate'] == 'John Kasich']
kasichData.drop('candidate', axis=1, inplace=True)

candidateDataMapping = {'Donald Trump' : trumpData, 'Ted Cruz' : cruzData, 'John Kasich' : kasichData}


# TODO fill in county-clusters
cluster = [1001, 1003, 1005, 1007]


predictions = {}

# loop through candidates
for candidate in candidates:

    trainingData = []
    testData = []

    data = candidateDataMapping[candidate]

    # assign county to training or test set
    for county in cluster:
        countyData = data[data['fips'] == county]
        if countyData['voted'].iloc[0] == 1:
            trainingData.append(countyData)
        else:
            testData.append(countyData)


    training = pd.concat(trainingData)
    test = pd.concat(testData)

    targetClass = training['fraction_votes']
    # targetClass = np.array(targetClass).astype(float)

    # build regression model
    regressor = RandomForestRegressor(n_estimators = 100)
    regressor = regressor.fit(training, targetClass)
    output = regressor.predict(test)
    accuracy = regressor.score(training, targetClass)

    # save predictions
    d = {'fips' : test['fips'], 'fraction_votes' : test['fraction_votes'], 'predictions' : output}
    predictions[candidate] = pd.DataFrame(data = d)
