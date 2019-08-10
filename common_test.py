import unittest
import pandas as pd
import common

class CommonTest(unittest.TestCase):
    def test_pca(self):
        df = pd.read_csv(r"C:\Users\localadmin\PycharmProjects\colossi\static\temp\6c3656b1aeb94c86b04f3e77ac11731e\imac_atlas_expression_v7.1.tsv", sep="\t", index_col=0)
        points = common.pcaTransform(df, 50)
        print(points)

if __name__ == '__main__':
    unittest.main()
