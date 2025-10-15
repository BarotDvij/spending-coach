from datetime import timedelta, date
from decimal import Decimal
from django.db.models import Sum, Count
from core.models import Transaction, Subscription

def _normalize_merchant(description: str) -> str:
    # crude normalization for recurring merchants
    return (description or "").strip().lower().split(" ")[0][:48]  # e.g., "netflix", "spotify"

def detect_subscriptions_for_month(user, year, month,
                                   min_occurrences=3,
                                   interval_days=30,
                                   amount_tolerance=Decimal("3.00")):
    """
    Heuristic: same normalized merchant, similar amount (+/- amount_tolerance),
    repeating roughly every ~30 days at least min_occurrences in history.
    """
    # look back 6 months for pattern
    from datetime import date
    start = date(year, month, 1) - timedelta(days=180)
    tx = (Transaction.objects
          .filter(user=user, date__gte=start)
          .values("description", "amount", "date"))

    # group by merchant
    buckets = {}
    for t in tx:
        m = _normalize_merchant(t["description"])
        if not m:
            continue
        buckets.setdefault(m, []).append((t["date"], t["amount"]))

    today = date.today()
    detected = []
    for merchant, rows in buckets.items():
        rows.sort(key=lambda x: x[0])
        if len(rows) < min_occurrences:
            continue

        # check approximate monthly cadence and stable amounts
        deltas = []
        amounts = []
        for i in range(1, len(rows)):
            deltas.append((rows[i][0] - rows[i-1][0]).days)
            amounts.append(rows[i][1])

        if not deltas:
            continue

        avg_delta = sum(deltas)/len(deltas)
        stable_amount = _amount_stable([r[1] for r in rows], amount_tolerance)

        if 20 <= avg_delta <= 40 and stable_amount is not None:
            last_date = rows[-1][0]
            next_est = last_date + timedelta(days=interval_days)
            confidence = min(0.99, 0.6 + 0.05*len(rows))
            occ = len(rows)
            detected.append({
                "merchant": merchant,
                "avg_amount": stable_amount,
                "last_seen": last_date,
                "next_estimated_date": next_est,
                "confidence": float(confidence),
                "occurrences": occ
            })

    # upsert into Subscription
    for d in detected:
        sub, _ = Subscription.objects.update_or_create(
            user=user, merchant=d["merchant"],
            defaults={
                "avg_amount": d["avg_amount"],
                "last_seen": d["last_seen"],
                "next_estimated_date": d["next_estimated_date"],
                "confidence": d["confidence"],
                "occurrences": d["occurrences"],
            }
        )
    return detected

def _amount_stable(amounts, tol: Decimal):
    # returns representative amount if within tolerance window
    if not amounts:
        return None
    baseline = Decimal(str(amounts[0]))
    for a in amounts[1:]:
        if abs(Decimal(str(a)) - baseline) > tol:
            return None
    return baseline.quantize(Decimal("0.01"))
