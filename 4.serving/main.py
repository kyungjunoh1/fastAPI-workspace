from fastapi import FastAPI, APIRouter
import uvicorn
from model.user import Titanic
import joblib

app = FastAPI()
router = APIRouter()
# 서버 시작 시 모델 로드
model = joblib.load("ml_model/rfc_model.joblib")
@router.get("/")  # 변경됨
def root():
    return {"message": "Titanic Prediction API is running"}

@router.post("/predict")
def predict(data: Titanic) -> dict:
    print("data : ", data)
    print( "data.dict().values() : ", data.dict().values() ) # data.model_dump().values()
    input_data = [[ list(data.model_dump().values()) ]]

    print("input_data", input_data)
    
    prediction = model.predict( input_data )
    print("prediction : ", prediction )
    return {"prediction": int(prediction[0])}

app.include_router( router )
if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)