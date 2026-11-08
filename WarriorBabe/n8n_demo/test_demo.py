"""Prueba de punta a punta de la demo: manda alertas sintéticas y verifica cada resultado.

Uso:  python test_demo.py     (n8n en http://localhost:5678 con los dos flujos publicados)
"""
import json
import sys
import urllib.error
import urllib.request

BASE = "http://localhost:5678/webhook"
TOKEN = {"X-Webhook-Token": "demo-token-123"}
sys.stdout.reconfigure(encoding="utf-8")


def call(method, path, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{BASE}/{path}", data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status, raw = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read().decode()
    try:
        return status, json.loads(raw or "null")
    except json.JSONDecodeError:
        return status, raw


def send(body, headers=TOKEN):
    return call("POST", "solarwinds-alert", body, headers)


def alert(**over):
    a = {
        "AlertID": 9001,
        "NodeName": "db-prod-01",
        "MetricName": "CPU Load",
        "MetricValue": 97,
        "Threshold": 90,
        "Severity": "Critical",
        "Message": "CPU load above 90% for 5 minutes",
        "TriggeredAt": "2026-11-07T10:00:00-05:00",
    }
    a.update(over)
    return a


failures = 0


def check(label, cond, detail=""):
    global failures
    print(("  OK   " if cond else "  FAIL ") + label + (f"  -> {detail}" if not cond else ""))
    if not cond:
        failures += 1


print("0. Reset")
call("POST", "mock/reset")
check("state empty", call("GET", "mock/state")[1]["serviceDeskTickets"] == 0)

print("1. No token -> rejected by the webhook")
st, r = send(alert(), headers={})
check("HTTP 403", st == 403, (st, r))
st, r = send(alert(), headers={"X-Webhook-Token": "wrong"})
check("wrong token HTTP 403", st == 403, (st, r))
check("nothing created", call("GET", "mock/state")[1]["serviceDeskTickets"] == 0)

print("2. New critical CPU alert -> creates a ticket")
st, r = send(alert())
check("HTTP 200", st == 200, (st, r))
check("outcome created", r.get("outcome") == "created", r)
check("ticket ARD-1001", r.get("ticketId") == "ARD-1001", r)
check("occurrences 1", r.get("occurrences") == 1, r)

print("3. Same alert again -> updates the same ticket, no duplicate")
st, r = send(alert(MetricValue=99, TriggeredAt="2026-11-07T10:05:00-05:00"))
check("outcome updated", r.get("outcome") == "updated", r)
check("same ticket ARD-1001", r.get("ticketId") == "ARD-1001", r)
check("occurrences 2", r.get("occurrences") == 2, r)

print("4. Re-run the exact same alert (simulated retry) -> still no duplicate")
st, r = send(alert(MetricValue=99, TriggeredAt="2026-11-07T10:05:00-05:00"))
check("outcome updated", r.get("outcome") == "updated", r)
check("same ticket ARD-1001", r.get("ticketId") == "ARD-1001", r)

print("5. Different machine, disk warning -> second ticket")
st, r = send(alert(AlertID=9002, NodeName="app-02", MetricName="Disk C: used %", MetricValue=91, Threshold=85,
                   Severity="Warning", Message="Disk C: above 85%"))
check("outcome created", r.get("outcome") == "created", r)
check("ticket ARD-1002", r.get("ticketId") == "ARD-1002", r)

print("6. Informational alert -> skipped")
st, r = send(alert(NodeName="web-03", Severity="Information"))
check("HTTP 200", st == 200, (st, r))
check("outcome ignored", r.get("outcome") == "ignored", r)
check("reason informational", r.get("reason") == "Informational severity", r)

print("7. Value below threshold -> skipped")
st, r = send(alert(NodeName="web-04", MetricValue=40))
check("outcome ignored", r.get("outcome") == "ignored", r)
check("reason below threshold", r.get("reason") == "Value is below the threshold", r)

print("8. Invalid payloads -> 400, no crash")
st, r = send(alert(NodeName=""))
check("empty NodeName HTTP 400", st == 400, (st, r))
check("validation_error", isinstance(r, dict) and r.get("error") == "validation_error", r)
bad = alert()
del bad["MetricName"]
st, r = send(bad)
check("missing MetricName HTTP 400", st == 400, (st, r))

print("9. Node down (availability) -> ticket even without value or threshold")
st, r = send({"NodeName": "fw-01", "MetricName": "Node Status Down", "Severity": "Critical",
              "Message": "Node not responding"})
check("outcome created", r.get("outcome") == "created", r)
check("ticket ARD-1003", r.get("ticketId") == "ARD-1003", r)

print("10. Service desk outage -> 502 after retries, nothing half-written")
call("POST", "mock/outage", {"on": True})
outage_alert = alert(AlertID=9010, NodeName="mail-01", MetricName="Memory used %", MetricValue=95, Threshold=90)
st, r = send(outage_alert)
check("HTTP 502", st == 502, (st, r))
check("sanitized upstream_error", isinstance(r, dict) and r.get("error") == "upstream_error"
      and "503" not in json.dumps(r), r)
s = call("GET", "mock/state")[1]
check("no ticket created during outage", s["serviceDeskTickets"] == 3, s["serviceDeskTickets"])
check("no source-of-truth record during outage", "mail-01|memory used %" not in s["sourceOfTruth"], list(s["sourceOfTruth"]))

print("11. Outage over, re-send the same alert -> recovered with exactly one ticket")
call("POST", "mock/outage", {"on": False})
st, r = send(outage_alert)
check("outcome created", r.get("outcome") == "created", r)
check("ticket ARD-1004", r.get("ticketId") == "ARD-1004", r)
st, r = send(outage_alert)
check("second re-send updates, no duplicate", r.get("outcome") == "updated" and r.get("ticketId") == "ARD-1004", r)

print("12. Final state: both systems agree")
_, s = call("GET", "mock/state")
tickets = {t["id"]: t for t in s["serviceDesk"]}
sot = s["sourceOfTruth"]
check("4 tickets in service desk", s["serviceDeskTickets"] == 4, s["serviceDeskTickets"])
check("4 records in source of truth", len(sot) == 4, list(sot))
check("every record points to a real ticket", all(rec["ticketId"] in tickets for rec in sot.values()), sot)
check("no two records share a ticket", len({rec["ticketId"] for rec in sot.values()}) == len(sot), sot)
cpu = sot.get("db-prod-01|cpu load", {})
check("CPU incident has 3 occurrences", cpu.get("occurrences") == 3, cpu)
t1 = tickets.get("ARD-1001", {})
check("ARD-1001 has 2 notes", len(t1.get("updates", [])) == 2, t1)
check("ARD-1001 note text", t1.get("updates", [{}])[0].get("note", "").startswith("Repeated alert: CPU Load = 99"), t1)
check("ARD-1001 title", t1.get("title") == "[P1] Performance: CPU Load on db-prod-01", t1.get("title"))
check("ARD-1002 title", tickets.get("ARD-1002", {}).get("title") == "[P2] Capacity: Disk C: used % on app-02",
      tickets.get("ARD-1002", {}).get("title"))
check("ARD-1003 title", tickets.get("ARD-1003", {}).get("title", "").startswith("[P1] Availability: Node Status Down"),
      tickets.get("ARD-1003", {}).get("title"))

print()
print("ALL CHECKS PASSED" if failures == 0 else f"{failures} CHECK(S) FAILED")
sys.exit(1 if failures else 0)
