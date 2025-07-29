from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifacts,DataValidationArtifacts
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_obj,save_numpy_array_data


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifacts,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    #3 do not need class instance of self    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
         
    def get_data_transformer_object(cls)->Pipeline:
        
        '''it initialises a KNN imputer object with the parameters specified in the training_pipeline.py file and return a pipeline object with the KNN imputer object ass the first object 
        Args :
            cls: DataTransformation
            
        Returns :
            A pipeline object
            
        '''
        
        logging.info('Entered get_data_transformer_object method of transformation class')
         
        try:
            # ** means it will take params as key value pair
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            
            logging.info(f'Initialise KNN imputer with params {DATA_TRANSFORMATION_IMPUTER_PARAMS}')
            
            processor:Pipeline=Pipeline(
                steps=[('imputer',imputer)]
            )
            
            return processor
        
        except Exception as e :
            raise NetworkSecurityException(e,sys)
         
    
    def initiate_data_tranformation(self)->DataTransformationArtifacts:
        logging.info('Enter initaite_data_tranformation method of Datatransformation class')
        try:
            logging.info('Starting data tranformation')
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            #training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_columns=train_df[TARGET_COLUMN]
            target_feature_train_columns=target_feature_train_columns.replace( -1 , 0 )
            
            #testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_columns=test_df[TARGET_COLUMN]
            target_feature_test_columns=target_feature_test_columns.replace( -1 , 0 )
            
            preprocessor=self.get_data_transformer_object()
            preprocessor_obj=preprocessor.fit(input_feature_train_df)
            
            transformed_input_train_feature=preprocessor.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor.transform(input_feature_test_df)
            
            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_columns)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_columns)]
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            
            save_obj(self.data_transformation_config.transformed_object_file_path,preprocessor_obj,)
            
            ## Preparing DataTransformation Artifacts
            
            data_transformation_artifact=DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            return data_transformation_artifact
            
                     
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    