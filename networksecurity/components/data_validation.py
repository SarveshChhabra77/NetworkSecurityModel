from networksecurity.entity.artifact_entity import DataIngestionArtificats,DataValidationArtifacts
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file


class DataValidation:
    def __init__(self,data_ingestion_artifacts:DataIngestionArtificats,data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
     ## becuse we use it only once in data validation   
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f'Required number of columns: {number_of_columns}')
            logging.info(f'Dataframe has columns : {len(dataframe)}')
            
            if len(dataframe.columns==number_of_columns):
                return True 
            else :
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def validate_numeric_columns(self,dataframe)->bool:
        try:
            numeric_columns=self._schema_config['numerical_columns']
            for col in numeric_columns:
                if col not in dataframe.columns:
                    return False
                else:
                    return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def detect_dataset_drift(self,base_df:dict,current_df:dict,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                ## it compares the distribution of 2 samples
                is_sample_dist=ks_2samp(d1,d2)
                
                if threshold<=is_sample_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    'p_value':float(is_sample_dist.pvalue),
                    'drift_status':is_found
                }})
                
            drift_report_filePath=self.data_validation_config.drift_report_file_path
            
            dir_path=os.path.dirname(drift_report_filePath)
            os.makedirs(dir_path,exist_ok=True)
            
            write_yaml_file(file_path=drift_report_filePath,content=report)
            
            return status
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
            
        
    def initiate_data_validation(self)->DataValidationArtifacts:
        try:
            train_file_path=self.data_ingestion_artifacts.trained_file_path
            
            test_file_path=self.data_ingestion_artifacts.tested_file_path
            
            ## read data from train and test
            train_dataframe=self.read_data(train_file_path)
            test_dataframe=self.read_data(test_file_path)
            
            ## validate number of columns
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f'Train dataframe does not containall columns. \n'
            
            status=self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f'Test dataframe does not containall columns. \n'
             ## validate numeric columns
            status=self.validate_numeric_columns(dataframe=train_dataframe)
            if not status:
                error_message=f'Train dataframe does not contain all numeric columns. \n'
            
            status=self.validate_numeric_columns(dataframe=test_dataframe)
            if not status:
                error_message=f'Test dataframe does not contain all numeric columns. \n'
        
        
        
            ## lets check datadrift
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            
            os.makedirs(dir_path,exist_ok=True)
            
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            
            data_validation_artifacts=DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifacts.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifacts.tested_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifacts
            
            
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    



