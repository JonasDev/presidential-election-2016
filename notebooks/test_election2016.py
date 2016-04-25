from unittest import TestCase
from election import Election2016


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



