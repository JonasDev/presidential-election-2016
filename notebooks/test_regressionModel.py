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

    def test_performRegression(self):
        e = Election2016()
        e.init()

        r = RegressionModel(e.data, e.candidateDataMapping, e.testDataFrame)
        r.performRegression()
        self.assertTrue(len(r.mse) > 0)

        print "Regressor benchmark performed"

    def test_modelForEveryClusterBuilt(self):
        e = Election2016()
        e.init()

        r = RegressionModel(e.data, e.candidateDataMapping, e.testDataFrame)
        r.performRegression()
        self.assertTrue(len(r.clusterResults) == 4)

        print "Regressor model for every cluster has been built"

