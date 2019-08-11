import unittest
from model import prediction_with_model
import pandas as pd
import numpy as np

class PredictionWithModel(unittest.TestCase):
    def test_prediction(self):
        d = pd.read_csv(r"C:\Users\Toan\Documents\GitHub\colossi\static\temp\cc7deed8140745d89f2f42f716f6fd1b\out_imac_atlas_expression_v7.1.tsv", " ")

        result = np.array([d['Freq'].to_list() + [0, 1800]])
        print(prediction_with_model(result))


if __name__ == '__main__':
    unittest.main()
