def decision_color(decision):
    colors = {
        "ALLOW": "#16a34a",
        "REVIEW": "#f59e0b",
        "BLOCK": "#dc2626",
        "HARD BLOCK": "#7f1d1d"
    }

    return colors.get(decision, "#64748b")