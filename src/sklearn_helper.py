from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class CoordinatesImputer(BaseEstimator, TransformerMixin):
    '''
    Original code author: Eryk Lewinson. Modified to work with our latitude and longitude column
    
    Class used for imputing (latitude,longitude) of (2e-08,0)
    
    Parameters
    ----------    
    group_cols : list
        List of columns used for calculating the aggregated value 
    groupByTarget : str
        The name of the column to impute
    metric : str
        The metric to be used for remplacement, can be one of ['mean', 'median']
    Returns
    -------
    X : array-like
        The array with imputed values in the target column
    '''
    def __init__(self, group_cols=['latitude','longitude'], groupByTarget='region', metric='median'):
        
        assert type(group_cols) == list, 'which columns to groupy by for mean/median'
        assert metric in ['mean', 'median'], 'Unrecognized value for metric, should be mean/median'
        assert type(groupByTarget) == str, 'groupByTarget should be a string'
        
        self.group_cols = group_cols
        self.groupByTarget = groupByTarget
        self.metric = metric
        

    def fit(self, X, y=None):
        
        impute_map = X.groupby(self.groupByTarget)[self.group_cols].agg(self.metric)
        
        self.impute_map_ = impute_map
        
        return self 
    
    def transform(self, X, y=None):
        
        # make sure that the imputer was fitted
        check_is_fitted(self, 'impute_map_')
        
        X = X.copy()
        
        #Generates T/F flags for records with bad coords
        index_locs = (X[self.group_cols]==[-2e-08,0]).all(axis=1)
        
        #Filters out only true records. Creates a series of just those indexes
        index_locs = index_locs[index_locs].reset_index()['index']
        
        for ind in index_locs:
            
            #grabbing region for current location to cross reference with impute map
            X.loc[ind, self.group_cols] = self.impute_map_.loc[X.loc[ind, self.groupByTarget]]
        
        return X.drop(self.groupByTarget, axis = 1) #dropping the group by target column
    

    
    

    
