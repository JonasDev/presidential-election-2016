import pandas as pd


cf = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/county_facts.csv')

columnDescriptions= pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/county_facts_dictionary.csv')
primaryResults = pd.read_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2016_presidential_election_v5/primary_results.csv')
primaries2012 = pd.ExcelFile(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/2012_primaries/2012_primaries.xlsx')

states = []
for i in range(len(primaries2012.sheet_names)):
    states.append(primaries2012.parse(i))

primariesMerged = pd.concat(states)

relevantCandidates = primariesMerged[['Paul', 'Romney', 'Gingrich', 'Santorum', 'fips']]
relevantCandidates['fips'].fillna(11001, inplace=True)
relevantCandidates['winner'] = relevantCandidates[['Paul', 'Romney', 'Gingrich', 'Santorum']].idxmax(axis=1)

result = pd.merge(cf, relevantCandidates, on='fips')
result.to_pickle(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/notebooks/county_facts_with_2012_winner')
result.to_csv(r'/Users/Jonas/OneDrive/Google Drive/Uni/UCB16/Machine Learning and Analytics/final_project/presidential-election-2016/notebooks/county_facts_with_2012_winner.csv', index=False)
