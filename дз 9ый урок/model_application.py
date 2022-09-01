from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

import pickle

app = FastAPI()


def load_model(model_name: str):
    with open(f'model/{model_name}.pkl', 'rb') as file:
        model = pickle.load(file)

    return model

MODEL_NAME = 'ramdom_forest_v2'
model = load_model(MODEL_NAME)


class Data(BaseModel):
    x_vector: List[float]


@app.post("/data/")
async def create_item(data: Data):
    prediction = int(model.predict([data.x_vector])[0])

    return {'prediction of condition': prediction}