from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataValidationArtifacts
import sys


if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        
        data_ingestion=DataIngestion(dataingestionconfig)
        
        logging.info('Initiate the data ingestion')
        
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        
        logging.info('Data Ingestion Completed')
        
        print(dataingestionartifact)

        
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
            
        logging.info('Initiate the Data Validation')
        
        data_validation_artifacts=data_validation.initiate_data_validation()
        
        logging.info('Data Validation Completed')
        
        print(data_validation_artifacts)
        
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        
        data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config)
        
        logging.info('Initiate data transformation')
        
        data_transformation_articats=data_transformation.initiate_data_tranformation()
        
        logging.info('Data transformation complted')
        
        print(data_transformation_articats)
        
        logging.info('Model Training Started')
        
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifacts=data_transformation_articats)
        
        model_trainer_artifacts=model_trainer.initiate_model_trainer()
        
        logging.info('Model Training artifacts created')
        
        
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)