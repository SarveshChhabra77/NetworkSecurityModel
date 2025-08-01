from dataclasses import dataclass


@dataclass
class DataIngestionArtificats:
    trained_file_path:str
    tested_file_path:str

@dataclass
class DataValidationArtifacts:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str
    
    
@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str
    
@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float    
    

@dataclass
class ModelTrainerArtifacts:
    trained_model_file_path:str
    train_metric_artifacts: ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact