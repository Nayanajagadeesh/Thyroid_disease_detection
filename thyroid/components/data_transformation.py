from thyroid.entity import artifact_entity,config_entity
from thyroid.exception import ThyroidException
from thyroid.logger import logging
from typing import Optional
import os,sys 
from sklearn.pipeline import Pipeline
import pandas as pd
from thyroid import utils
import numpy as np
import sklearn
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from thyroid.config import TARGET_COLUMN
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline,make_pipeline
from sklearn.preprocessing import MinMaxScaler
class DataTransformation:


    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                    data_validation_artifact:artifact_entity.DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise ThyroidException(e, sys)


    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:      
            trf1 = ColumnTransformer(transformers=[

                    ('oe',OrdinalEncoder(),['on_thyroxine',
                        'query_on_thyroxine',
                        'on_antithyroid_medication',
                        'sick',
                        'pregnant',
                        'thyroid_surgery',
                        'I131_treatment',
                        'query_hypothyroid',
                        'query_hyperthyroid',
                        'lithium',
                        'goitre',
                        'tumor',
                        'hypopituitary',
                        'psych']),
        
                    ('onehot', OneHotEncoder(), ['sex']),
                    ('imputer_scaler', make_pipeline(KNNImputer(), MinMaxScaler()), ['age', 'TSH', 'T3', 'TT4', 'T4U', 'FTI'])
                    ],remainder='passthrough')

            return trf1
        except Exception as e:
            raise ThyroidException(e, sys)



    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            train_df = pd.read_csv(self.data_validation_artifact.train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            
            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)



            transformer=DataTransformation.get_data_transformer_object()
          
            
            input_feature_train_arr=transformer.fit_transform(input_feature_train_df)
            # input_feature_train_arr = transformer.transform(input_feature_train_df)
            input_feature_test_arr = transformer.transform(input_feature_test_df)



            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            #target encoder
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]


            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)


            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformer)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)
            logging.info(f"sklearn version: {sklearn.__version__}")


            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path

            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise ThyroidException(e,sys)
