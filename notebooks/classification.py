import pandas as pd
from sklearn.ensemble import RandomForestClassifier


cf = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/county_facts.csv')
pr = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/primary_results.csv')

pr = pr[pr['party'] == 'Republican']
pr.drop('state_abbreviation', axis = 1, inplace=True)

data = pd.merge(cf, pr, on='fips')

stateCluster = ['AL', 'NH']

# add cf, merge on fips


trainingData = []
for state in stateCluster:
    trainingData.append(data[data['state_abbreviation'] == state])




targetClass =








classifier = RandomForestClassifier(n_estimators = 100)
classifier = classifier.fit(X, targetClass)
output = classifier.predict(test_data)
