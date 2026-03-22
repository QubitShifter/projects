from fastapi import FastAPI 
from src.models.rules import rule_engine
from src.models.predict import predict_ml
from src.models.decision import decision_engine

app = FastAPI()

@app.post("/predict")
def predict(transaction: dict):
    #step 1
    rules = rule_engine(transaction)

    #step 2: ML (not implemented yet)
    ml_score = predict_ml(transaction)

    result = decision_engine(rules, ml_score)

    #step 3: Decision
    return{
        "rules_triggered": rules,
        "ml_score": ml_score,
        "risk_score": result["risk_score"],
        "decision": result["decision"]
    }
