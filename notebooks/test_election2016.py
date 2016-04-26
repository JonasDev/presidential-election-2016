from unittest import TestCase
from election import Election2016
import numpy as np


class TestElection2016(TestCase):
    def test_loadDataSets(self):
        election = Election2016()
        election.loadDataSets()
        self.assertFalse(election.cf.empty)
        self.assertFalse(election.pr.empty)

        self.assertTrue(len(election.cf.columns) == 54)
        self.assertTrue(len(election.pr.columns) == 8)
        print 'Data sets have been loaded correctly'

    def test_preprocessingRemoveDemocrats(self):
        e = Election2016()
        e.loadDataSets()

        self.assertTrue(len(e.pr[e.pr['party'] == 'Democrat']) > 0)

        e.preprocessDataSets()

        self.assertTrue(len(e.pr[e.pr['party'] == 'Democrat']) == 0)

        print 'Democrats have successfully been removed from the data-set'

    def test_preprocessingStringEncoding(self):
        e = Election2016()
        e.loadDataSets()

        self.assertTrue(type(e.pr['state_abbreviation'].iloc[0]) is str)

        e.preprocessDataSets()

        self.assertFalse('state_abbreviation' in e.data.columns)
        self.assertTrue('state_number' in e.data.columns)

        self.assertTrue(type(e.data['state_number'].iloc[0]) is np.int64)

        print 'Strings have been encoded as numbers for regression model'

    def test_preprocessingRemoveUnnecessaryFeatures(self):
        e = Election2016()
        e.loadDataSets()

        e.preprocessDataSets()

        self.assertFalse('area_name' in e.data.columns)
        self.assertFalse('county' in e.data.columns)
        self.assertFalse('state' in e.data.columns)
        self.assertFalse('party' in e.data.columns)
        self.assertFalse('votes' in e.data.columns)

        print 'Unnecessary features have been removed'

    def test_preprocessingNoVotesInTestSet(self):
        e = Election2016()
        e.loadDataSets()

        e.preprocessDataSets()

        self.assertTrue(len(e.testDataFrame['voted'].unique()) == 1)
        self.assertTrue(e.testDataFrame['voted'].unique()[0] == 0)

        print 'Test set includes only counties that have not voted so far'

    def test_candidates(self):
        e = Election2016()
        e.loadDataSets()
        e.preprocessDataSets()
        candidates = ['Donald Trump', 'Ted Cruz', 'John Kasich']

        candidateDataMapping = e.setupCandidates(e.data)

        mapping = [can in candidates for can in candidateDataMapping.keys()]
        self.assertEqual(mapping, [True, True, True])

        print 'Data for all candidates has been mapped'



