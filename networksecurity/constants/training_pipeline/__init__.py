import os
import numpy as np

'''
Defining common constants variable for training pipeline
'''
TARGET_COLUMN='Result'
PIPELINE_NAME:str='NetworkSecurity'
ARTIFACT_DIR:str='Artifacts'
FILE_NAME:str='phisingData.csv'
TRAIN_FILE_NAME:str='train.csv'
TEST_FILE_NAME:str='test.csv'
SCHEMA_FILE_PATH=os.path.join('data_schema','schema.yaml')
SAVED_MODEL_DIR:str=os.path.join('saved_models')
MODEL_FILE_NAME:str='model.pkl'
'''
Data Ingestion related constants starts with Data_Ingestion var name
'''

DATA_INGESTION_COLLECTION_NAME:str='NetworkData'
DATA_INGESTION_DATABASE_NAME:str='sarvespoker'
DATA_INGESTION_DIR_NAME:str='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str='feature_store'
DATA_INGESTION_INGESTED_DIR:str='ingested' 
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2


'''Data Validation related constants start with Data_Validation var name '''

DATA_VALIDATION_DIR_NAME:str='data_validation'
DATA_VALIDATION_VALID_DIR:str='validated'
DATA_VALIDATION_INVALID_DIR:str='invalid'
DATA_INGESTION_DRIFT_REPORT_DIR:str='drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str='report.yaml'

'''Data Transformation related constants start with Data_Transformation var name '''

DATA_TRANSFORMATION_DIR_NAME:str='data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str='transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str='transformed_object'

#  KNN imputer to replace nan value
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
    'missing_values':np.nan,
    'n_neighbors':3,
    'weights':'uniform' # Corrected typo here
}
PREPROCESSING_OBJECT_FILE_NAME:str='preprocessing.pkl'

MODEL_TRANSFORMATION_TRAIN_FILE_PATH:str='train.npy'
MODEL_TRANSFORMATION_TEST_FILE_PATH:str='test.npy'


'''Model Trainer related constants start with Model_trainer var name '''
MODEL_TRAINER_DIR_NAME:str='model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR:str='trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME:str='model.pkl'
# MODEL_TRAINER_MODEL_CONFIG_FILE_PATH:str=''
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float=0.05
