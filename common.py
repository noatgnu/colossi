from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

def pcaTransform(input, retain):
    """
    Args:
        input (DataFrame): input points to be PCA transformed
            columns are dimensions to be reduced
        retain (int): number of dimensions to reduce to
    Returns:
        DataFrame of PCA transformed points
    """
    # store columns of input data frame
    cols = [i for i in input.columns]
    # Z score normalize so no one feature stands out over the others
    input = StandardScaler().fit_transform(input)
    input = pd.DataFrame(input, columns=cols)
    # create pca object to analyze n dimensions (number of columns)
    pca = PCA(n_components=len(input.columns))

    # feed input in to be analyzed
    pca.fit(input)

    # transform points according to PCA to minimize variances
    points = pca.transform(input)
    # add back column labels to points
    points = pd.DataFrame(points, columns=cols)

    # proportion of variance explained by each dimension
    var = pca.explained_variance_ / sum(pca.explained_variance_)
    # make sure matrix is horizontal 1x3
    var = pd.DataFrame(var)
    # label this column variance explained
    var.columns = ['variance explained']
    # add column labels on top of 1x3 matrix
    var.insert(1, 'col variable', cols)
    # reduce dimension to number specified by retain
    pcaReduce = PCA(n_components=retain)
    points = pd.DataFrame(pcaReduce.fit_transform(points))

    # tidy table has all graph variables as columns, rows are just IDs


    return points