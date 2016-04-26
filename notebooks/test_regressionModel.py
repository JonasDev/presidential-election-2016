from unittest import TestCase
from regression import RegressionModel
from election import Election2016


class TestRegressionModel(TestCase):
    def test_properInitialization(self):
        e = Election2016()
        e.init()

        r = RegressionModel(e.data, e.candidateDataMapping, e.testDataFrame)

        self.assertFalse(r.clusters.empty)

        self.assertTrue(len(r.clusters) == 2957)

        print 'Regression model properly initialized'

    