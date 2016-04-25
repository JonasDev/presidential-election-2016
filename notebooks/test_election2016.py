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

        print 'Srings have been encoded as numbers for regression model'




