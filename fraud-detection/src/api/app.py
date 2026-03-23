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
    ml_score, top_features = predict_ml(transaction)

    result = decision_engine(rules, ml_score)
    
    # reason
    rule_names = [r["rule"] for r in rules]
    reason_parts = []

    if rule_names:
        reason_parts.append("rules: " + ", ".join(rule_names))
    if ml_score > 0.8:
        reason_parts.append("ML: high fraud probability")
    elif ml_score > 0.3:
        reason_parts.append("ML: moderate risk")

    reason = " | ".join(reason_parts) if reason_parts else "low risk"

    #step 3: Decision
    return {
        "decision": result["decision"],
        "ml_score": float(round(ml_score, 3)),
        "risk_score": float(result["risk_score"]),
        "rules_triggered": rules,
        "top_features": top_features,
        "reason": reason
    }
