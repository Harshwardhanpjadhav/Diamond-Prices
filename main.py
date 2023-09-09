from src.diamond.configuration.mongo_conn import MongodbClient
from src.diamond.exception import CustomException
from src.diamond.logger import logging
from src.diamond.pipeline.training_pipeline import TrainingPipeline
from fastapi import FastAPI
from src.diamond.ml.estimator import ModelResolver
from src.diamond.utils.main_util import load_object
from src.diamond.constants.trainingpipeline import SAVED_MODEL_DIR
from uvicorn import run as app_run
import pandas as pd
from starlette .responses import RedirectResponse
from fastapi.responses import Response
from fastapi import FastAPI, File, UploadFile,Request


import os
import sys

app = FastAPI()
origins = ["*"]

# app.add_middleware(
#     # CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    


@app.get("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        #get data from user csv file
        #conver csv file to dataframe
        df = pd.read_csv(file.file)
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        return df.to_html()
        #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")


if __name__ == '__main__':
    app_run(app)
