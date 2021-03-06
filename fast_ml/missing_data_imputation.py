import pandas as pd
import numpy as np

from IPython.display import Markdown, display




class MissingDataImputer_Numerical:
    '''
    
    Various imputation methods available in this module are:
    Mean, Median, Mode, User define value, Random Sample distribution
    
    Parameters:
    -----------
        Allowed values for
        method : 'mean', 'median', 'mode', 'custom_value', 'random'
        value : if method ='custom_value' then user can pass on the imputation value in this parameter
        add_indicator : True / False. If True then a new binary variable will be created of the name "var_nan" 
                        which will take value 1 if there's a missing value in var or 
                        0 if there's no missing value in var
    '''
    def __init__ (self, method, add_indicator = True, value=None, random_state =1):
        
        '''
        
        Parameters:
        -----------
        
            method : strategy for imputation like 'mean', 'median', 'mode', 'custom_value', 'random'
            value : if method ='custom_value' then user can pass on the imputation value in this parameter
            add_indicator : True / False. If True then a new binary variable will be created of the name "var_nan" 
                        which will take value 1 if there's a missing value in var or 
              
              
         '''
        
        self.method = method
        self.value = value
        self.random_state = random_state
        self.add_indicator = add_indicator
        self.variables = variables

 
        
 

        
    def fit (self, df, variables):


        '''
        
        The fit function imputes the dataset for the missing values based on the strateghy or method used and stores it into a
        dictionary 'param_dict_' variable 
      
        Parameters:
        ----------
        
            df : df defines the dataset
            
            variables : set of categorical columns to be imputed
            
        Returns : 
        --------
        
            returns all the imputed values
        
        '''

        
        self.variables = variables
        
        if self.method =='mean':
            self.param_dict_ = df[self.variables].mean().to_dict()
        
        if self.method =='median':
            self.param_dict_ = df[self.variables].median().to_dict()
        
        if self.method =='mode':
            self.param_dict_ = df[self.variables].mode().to_dict()
            
        if self.method =='UB' or self.method =='ub' or self.method =='upper_bound':
            self.param_dict_ = df[self.variables].mode().to_dict()
        
        if self.method =='custom_value':
            if value==None:
                raise ValueError("for 'custom_value' method provide a valid value in the 'value' parameter")
            else:
                self.param_dict_ = {var:self.value for var in variables}
        
        if self.method =='random':
            None
            
        return self
    
    def transform(self, df):
        
        '''
        
        The transform function applies the changes to the data after the fit function imputation is made in a dictionary variable
        
        
        Parameters:
        -----------
        
            df : df defines the dataset
            
        Return : 
        ------- 
        
            returns the dataset after apply of imputed values

        '''

        if self.add_indicator == True:
            df[var + '_nan'] = np.where(df[var].isnull(), 1, 0)
        
        if self.method == 'random':
            df = self.__random_imputer__(df)
        
        else:
            for var in self.param_dict_:
                df[var].fillna(self.param_dict_[var] , inplace=True)
        
        return df
    
    def __random_imputer__(self, df):
        
        '''
        
        This function is for random imputation of the missing values
        
        Parameters:
        ----------
        
            df : df defines the dataset

        Return:
        ------
        
            This function returns the dataset after the ramdom imputation.
            
        '''

    
        for var in self.variables:
        
            if df[var].isnull().sum()>0:
                
                # number of data point to extract at random
                n_samples = df[var].isnull().sum()

                #extract values
                random_sample = df[var].dropna().sample(n_samples, random_state=self.random_state)

                # re-index for pandas so that missing values are filled in the correct observations
                random_sample.index = df[df[var].isnull()].index

                # replace na
                df.loc[df[var].isnull(), var] = random_sample

        return df
    
    
    
    
    def __get_upper_bound__(self, df):
        
        '''
        
        This function is to obtain the upper bound or threshold values
        
        Parameters:
        ----------
        
            df : df defines the dataset

        Return:
        ------
        
            This function does not return any value
            
        '''
        
        for var in self.variables:
            None
        
        return None
            




class MissingDataImputer_Categorical:
    '''
    
    Various imputation methods available in this module are:
    Mean, Median, Mode, User define value, Random Sample distribution
    
    Parameters:
    ----------
        Allowed values for
        method : 'frequent', 'custom_value', 'random'
        value : if method ='custom_value' then user can pass on the imputation value in this parameter
        add_indicator : True / False. If True then a new binary variable will be created of the name "var_nan" 
                        which will take value 1 if there's a missing value in var or 
                        0 if there's no missing value in var
                        
    '''
    
    def __init__ (self, method, add_indicator = True, value='Missing', random_state =1):
        self.method = method
        self.value = value
        self.random_state = random_state
        self.add_indicator = add_indicator
        
    def fit (self, df, variables):
        
        '''
        The fit function imputes the dataset for the missing values based on the strategy or method used and stores it into a
        dictionary 'param_dict_' variable
        
        
        Parameters:
        -----------
        
            df : df defines the dataset
            variables : list of variables to be imputed
            
        Return : 
        ------- 
        
            returns the self variables after imputing the values

        '''
        
        
        if self.method =='frequent':
            self.param_dict_ = {}
            
            for var in variables:
                value = df[var].mode()
                
                # Careful : because some variable can have multiple modes
                if len(value) ==1:
                    self.param_dict_[var] = value[0]
                else:
                    raise ValueError(f'Variable {var} contains multiple frequent categories')

        if self.method =='custom_value':
            #if value==None:
             #   raise ValueError("for 'custom_value' method provide a valid value in the 'value' parameter")
            #else:
            self.param_dict_ = {var:self.value for var in variables}

        if self.method =='random':
            None
            
        return self
    
    def transform(self, df):
        
        '''
        
        The transform function applies the changes to the data after the fit function imputation is made in a dictionary variable
        
        
        Parameters:
        -----------
        
            df : df defines the dataset
            
        Return : 
        ------- 
        
            returns the dataset after apply of imputed values

        '''
        
        if self.method == 'random':
            df = self.__random_imputer__(df)
        
        else:
            for var in self.param_dict_:
                # Add indicator
                if self.add_indicator == True:
                    df[var + '_nan'] = np.where(df[var].isnull(), 1, 0)
                # impute missing values
                df[var].fillna(self.param_dict_[var] , inplace=True)
        
        
        return df
    
    def __random_imputer__(self, df):
        
        '''
        
        This function is for random imputation of the missing values
        
        Parameters:
        ----------
        
            df : df defines the dataset

        Return:
        ------
        
            This function returns the dataset after the ramdom imputation.
            
        '''
        
        
        for var in self.variables:
            
            if df[var].isnull().sum()>0:
                
                # number of data point to extract at random
                n_samples = df[var].isnull().sum()

                #extract values
                random_sample = df[var].dropna().sample(n_samples, random_state=self.random_state)

                # re-index for pandas so that missing values are filled in the correct observations
                random_sample.index = df[df[var].isnull()].index

                # add missing indicator
                if self.add_indicator == True:
                    df[var + '_nan'] = np.where(df[var].isnull(), 1, 0)
                # replace na
                df.loc[df[var].isnull(), var] = random_sample

        return df