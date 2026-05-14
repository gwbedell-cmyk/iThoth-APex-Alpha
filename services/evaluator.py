def evaluate_action(action):
    risk = 0
    explanations = []
    triggered_policies = []

    if action["bank_changed_days"] <= 7:
        risk += 30
        explanations.append("Vendor banking details changed recently")
        triggered_policies.append("P-12 Vendor Change Risk")

    if action["duplicate_similarity"] > 0.8:
        risk += 35
        explanations.append("Potential duplicate invoice detected")
        triggered_policies.append("P-27 Duplicate Detection")

    if not action["approval_complete"]:
        risk += 20
        explanations.append("Approval chain incomplete")
        triggered_policies.append("P-19 Approval Completeness")

    if action["po_amount"] > 0:
        po_variance = (action["amount"] - action["po_amount"]) / action["po_amount"]

        if po_variance > 0.10:
            risk += 15
            explanations.append("Invoice exceeds approved PO threshold")
            triggered_policies.append("P-31 Threshold Variance")

    if action["vendor_risk_score"] > 0.5:
        risk += 10
        explanations.append("Elevated vendor risk profile")
        triggered_policies.append("P-42 Vendor Risk Escalation")

    if risk >= 90:
        decision = "HARD BLOCK"
    elif risk >= 70:
        decision = "BLOCK"
    elif risk >= 40:
        decision = "REVIEW"
    else:
        decision = "ALLOW"

    return {
        "risk_score": risk,
        "decision": decision,
        "explanations": explanations,
        "triggered_policies": triggered_policies
    }