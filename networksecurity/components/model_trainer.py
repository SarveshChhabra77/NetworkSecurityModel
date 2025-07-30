import os
import sys

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifacts,DataTransformationArtifacts,ClassificationMetricArtifact


from networksecurity.utils.main_utils.utils import save_obj,load_numpy_array_data,evaluate_models,load_object
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

## All machine learning models
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier)
import mlflow

# import dagshub
# dagshub.init(repo_owner='SarveshChhabra77', repo_name='NetworkSecurityModel', mlflow=True)
## it will create mlrun folder into this remote repo



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifacts:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifacts=data_transformation_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classification_metric:ClassificationMetricArtifact):
        with mlflow.start_run():
            f1_score=classification_metric.f1_score
            precision_score=classification_metric.precision_score
            recall_score=classification_metric.recall_score
            
            mlflow.log_metric('f1_score',f1_score)
            mlflow.log_metric('precision_score',precision_score)
            mlflow.log_metric('recall_score',recall_score)
            mlflow.sklearn.log_model(best_model,'model')
        
    def model_train(self,x_train,y_train,x_test,y_test):
        try:
            models={
                'Random-Forest':RandomForestClassifier(verbose=1),
                'Decision-Tree':DecisionTreeClassifier(),
                'Gradient-Boosting':GradientBoostingClassifier(),
                'Logistic-Regression': LogisticRegression(),
                'Ada-Boost':AdaBoostClassifier()
            }
            
            params={
                'Random-Forest':{
                    'n_estimators':[8,16,32,64,128,256]
                },
                'Decision-Tree':{
                    'criterion':['gini','entropy','log_loss'],
                },
                'Gradient-Boosting':{
                    'learning_rate': [.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'n_estimators':[8,16,32,128,256]
                },
                'Logistic-Regression':{},
                'Ada-Boost':{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators':[8,16,32,128,256]
                }    
            }
            model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,params=params)
            
            best_model_score=max(model_report.values())
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]
            
            
            y_train_pred=best_model.predict(x_train)
            
            classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
            
            
            ##track the experiments with mlflow
            
            self.track_mlflow(best_model,classification_train_metric)
            
        
            
            y_test_pred=best_model.predict(x_test)
            
            classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)
            
            self.track_mlflow(best_model,classification_test_metric)
            
            preprocessor=load_object(file_path=self.data_transformation_artifacts.transformed_object_file_path)
            
            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            
            Network_model=NetworkModel(processor=preprocessor,model=best_model)
            
            save_obj(self.model_trainer_config.trained_model_file_path,Network_model)
            
            save_obj('final_model/model.pkl',best_model)
            
            ## model trainer artifacts
            model_trainer_artifacts=ModelTrainerArtifacts(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifacts=classification_train_metric,
                test_metric_artifact=classification_test_metric
                )
            logging.info(f'Model Trainer Artifacts : {model_trainer_artifacts}')
            
            return model_trainer_artifacts
            
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifacts:
        
        try:
            train_file_path=self.data_transformation_artifacts.transformed_train_file_path
            test_file_path=self.data_transformation_artifacts.transformed_test_file_path
            
            ## loading training array and testing array
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)
            
            X_train,X_test,y_train,y_test=(
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )
            model_trainer_artifacts=self.model_train(X_train,y_train,X_test,y_test)
            
            
            return model_trainer_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)