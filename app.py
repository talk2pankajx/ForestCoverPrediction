from fastapi import FastAPI
import sys
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.requests import Request
from forest_cover.pipeline.training_pipeline import TrainingPipeline
from forest_cover.pipeline.prediction_pipeline import PredictionPipeline
from forest_cover.exception import ForestException


app = FastAPI()
TEMPLATES = Jinja2Templates(directory="templates")

orgins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=200)
@app.post("/",)
async def index(request: Request):
    return TEMPLATES.TemplateResponse(name='index.html',context={"request":request})

@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        return Response("<h1> Training Sucessfully Completed !</h1>")
    except Exception as e:
        raise ForestException(e,sys)

@app.get("/predict")

async def predictRouteClient():
    try:
        predict_pipeline = PredictionPipeline()
        predict_pipeline.initiate_prediction()
        return Response("<h1> Prediction Sucessfully Completed and stored in s3 bucket !</h1>")
    except Exception as e:
        raise ForestException(e,sys)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)