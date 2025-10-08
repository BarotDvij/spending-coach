def generate_insights(summary_data, budgets):
    insights = []
    for b in budgets:
        cat_total = next((c["total"] for c in summary_data["by_category"] if c["category"] == b.category), 0)
        pct = (cat_total / b.amount * 100) if b.amount else 0

        if pct > 80:
            insights.append({
                "type": "Budget nearly exceeded",
                "severity": "high",
                "payload": {"category": b.category, "amount": b.amount, "spent": float(cat_total), "budget": b.amount}, "percent_used": round(pct, 2)
            })
        elif pct >= 50:
            insights.append({
                "type": "Midway through budget",
                "severity": "medium",
                "payload": {"category": b.category, "percent_used": round(pct, 2)},
            })
        return insights