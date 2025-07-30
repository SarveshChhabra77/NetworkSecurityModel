import os
import sys
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
    )
from networksecurity.entity.artifact_entity import (
    DataIngestionArtificats,
    DataValidationArtifacts,
    DataTransformationArtifacts,
    ModelTrainerArtifacts
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            
            logging.info("Start Data Ingestion")
            
            self.data_ingestion = DataIngestion(self.data_ingestion_config)
            
            data_ingestion_artifacts=self.data_ingestion.initiate_data_ingestion()
            
            logging.info(f'Data ingestion completed : {data_ingestion_artifacts}')
            
            return data_ingestion_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifacts:DataIngestionArtificats):
        
        try:
            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
        
            logging.info('Start Data validation ')
            
            self.data_validation=DataValidation(data_ingestion_artifacts=data_ingestion_artifacts,data_validation_config=self.data_validation_config)
            
            data_validation_artifacts=self.data_validation.initiate_data_validation()
            
            logging.info(f'Data Validation completed : {data_validation_artifacts}')
            
            return data_validation_artifacts
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifacts:DataValidationArtifacts):
        
        try:
            self.data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            
            logging.info('Data Transformation Started')

            self.data_transformation=DataTransformation(data_validation_artifact=data_validation_artifacts,data_transformation_config=self.data_transformation_config)
            
            data_transformation_artifacts=self.data_transformation.initiate_data_tranformation()
            
            logging.info(f'Data Transformation Completed : {data_transformation_artifacts}')
            
            return data_transformation_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifacts:DataTransformationArtifacts):
            try:
                self.model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
                
                logging.info('Model Training Started')

                self.model_trainer=ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifacts=data_transformation_artifacts)
                
                model_trainer_artifacts=self.model_trainer.initiate_model_trainer()
                
                logging.info(f'Model Training is completed : {model_trainer_artifacts}')

                return model_trainer_artifacts
            
            except Exception as e :
                return NetworkSecurityException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifacts=self.start_data_ingestion()
            data_validation_artifacts=self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifacts=self.start_data_transformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts=self.start_model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            
            return model_trainer_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
                
        
        