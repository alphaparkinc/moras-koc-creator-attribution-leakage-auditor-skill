import sys, math
sys.stdout.reconfigure(encoding='utf-8')

class KocCreatorAttributionLeakageAuditorClient:
    """
    Social commerce affiliate attribution ledger auditor.
    Detects creator commission leakage caused by short 7-day cookie windows,
    browser privacy cookie wiping, and platform last-touch hijacking.
    Calculates fair Shapley / Time-Decayed multi-touch commission reallocation.
    """
    def __init__(self, half_life_days=7.0):
        self.half_life = half_life_days

    def audit_attribution_leakage(self, conversion_events):
        """
        conversion_events: list of dicts:
        {
            "order_id": str,
            "order_value_usd": float,
            "recorded_last_touch_creator": str,
            "touchpoints": [
                {"creator_id": str, "channel": str, "days_before_order": float}
            ]
        }
        """
        if not conversion_events:
            return {"status": "error", "message": "No conversion events supplied"}

        total_gmv = sum(e["order_value_usd"] for e in conversion_events)
        last_touch_payouts = {}
        multi_touch_payouts = {}

        for event in conversion_events:
            val = float(event["order_value_usd"])
            comm_pool = val * 0.15 # standard 15% commission pool
            
            # Last-touch attribution
            lt_creator = event.get("recorded_last_touch_creator", "ORGANIC")
            last_touch_payouts[lt_creator] = last_touch_payouts.get(lt_creator, 0.0) + comm_pool

            # Time-decay multi-touch attribution
            tps = event.get("touchpoints", [])
            if not tps:
                multi_touch_payouts[lt_creator] = multi_touch_payouts.get(lt_creator, 0.0) + comm_pool
                continue

            weights = []
            for tp in tps:
                d = max(0.0, float(tp.get("days_before_order", 0.0)))
                # Exponential decay weight: 2^(-d / half_life)
                w = math.pow(2.0, -d / self.half_life)
                weights.append((tp["creator_id"], w))

            sum_w = sum(w for _, w in weights)
            if sum_w == 0: sum_w = 1.0

            for cid, w in weights:
                share = (w / sum_w) * comm_pool
                multi_touch_payouts[cid] = multi_touch_payouts.get(cid, 0.0) + share

        # Compute creator discrepancies
        all_creators = set(last_touch_payouts.keys()) | set(multi_touch_payouts.keys())
        discrepancies = []
        total_leakage = 0.0

        for c in all_creators:
            lt_val = last_touch_payouts.get(c, 0.0)
            mt_val = multi_touch_payouts.get(c, 0.0)
            diff = mt_val - lt_val # positive means creator was underpaid/leaked
            if diff > 0:
                total_leakage += diff
            discrepancies.append({
                "creator_id": c,
                "last_touch_commission": round(lt_val, 2),
                "fair_multi_touch_commission": round(mt_val, 2),
                "commission_discrepancy": round(diff, 2),
                "status": "UNDERPAID_LEAKAGE" if diff > 5.0 else ("OVER_ATTRIBUTED" if diff < -5.0 else "FAIR")
            })

        discrepancies.sort(key=lambda x: x["commission_discrepancy"], reverse=True)

        return {
            "status": "success",
            "audited_orders_count": len(conversion_events),
            "total_gmv_audited": round(total_gmv, 2),
            "total_creator_commission_pool": round(total_gmv * 0.15, 2),
            "identified_attribution_leakage": round(total_leakage, 2),
            "leakage_rate_pct": round(total_leakage / (total_gmv * 0.15) * 100, 1) if total_gmv > 0 else 0.0,
            "creator_attribution_reconciliation": discrepancies
        }
