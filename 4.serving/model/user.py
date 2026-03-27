#[ 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare']
#Survived : 0 사망, 1 생존
from pydantic import BaseModel
class Titanic(BaseModel):
    pclass : int
    sex : int
    age : float
    sibsp : int
    parch : int
    fare : float