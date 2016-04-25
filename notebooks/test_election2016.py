from unittest import TestCase
from election import Election2016


class TestElection2016(TestCase):
    def test_loadDataSets(self):
        election = Election2016()
        election.loadDataSets()
        self.assertFalse(election.cf.empty, "Loading county facts")
        self.assertFalse(election.pr.empty, "Loading prediction results")



