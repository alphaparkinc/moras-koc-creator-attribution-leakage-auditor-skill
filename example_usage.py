from client import KocCreatorAttributionLeakageAuditorClient
import sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    auditor = KocCreatorAttributionLeakageAuditorClient(half_life_days=7.0)
    print("=== MORAS KOC ATTRIBUTION LEAKAGE AUDITOR ===")

    events = [
        {
            "order_id": "ORD-1001",
            "order_value_usd": 120.00,
            "recorded_last_touch_creator": "creator_checkout_coupon",
            "touchpoints": [
                {"creator_id": "creator_viral_video_hook", "channel": "tiktok_video", "days_before_order": 5.0},
                {"creator_id": "creator_checkout_coupon",   "channel": "coupon_site",  "days_before_order": 0.2}
            ]
        },
        {
            "order_id": "ORD-1002",
            "order_value_usd": 85.00,
            "recorded_last_touch_creator": "creator_checkout_coupon",
            "touchpoints": [
                {"creator_id": "creator_viral_video_hook", "channel": "tiktok_video", "days_before_order": 2.0},
                {"creator_id": "creator_checkout_coupon",   "channel": "coupon_site",  "days_before_order": 0.1}
            ]
        }
    ]

    res = auditor.audit_attribution_leakage(events)
    print()
    print(f"Audited Orders: {res['audited_orders_count']} | GMV: ${res['total_gmv_audited']} | Comm Pool: ${res['total_creator_commission_pool']}")
    print(f"Identified Creator Leakage: ${res['identified_attribution_leakage']} ({res['leakage_rate_pct']}% of commissions)")
    print()
    print("Creator Attribution Comparison (Last Touch vs Fair Multi-Touch):")
    for c in res['creator_attribution_reconciliation']:
        print(f"  - [{c['status']}] {c['creator_id']}: LastTouch=${c['last_touch_commission']} -> FairMT=${c['fair_multi_touch_commission']} (Diff: {c['commission_discrepancy']:+0.2f})")

if __name__ == "__main__":
    main()
