import sys, json
from client import KocCreatorAttributionLeakageAuditorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    auditor = KocCreatorAttributionLeakageAuditorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "moras-koc-creator-attribution-leakage-auditor-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    events = req.get("conversion_events", [])
    res = auditor.audit_attribution_leakage(events)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
