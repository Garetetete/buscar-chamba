"""v2 de la demo de WarriorBabe, siguiendo las guías oficiales de n8n-io/skills."""
import json
import sys
import uuid
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://localhost:5678/webhook"
CRED = {"id": "wbHeaderAuth0001", "name": "SolarWinds webhook token"}


def uid():
    return str(uuid.uuid4())


def node(name, ntype, version, pos, params, **extra):
    n = {"parameters": params, "id": uid(), "name": name, "type": ntype, "typeVersion": version, "position": pos}
    n.update(extra)
    return n


def webhook(name, path, method, pos, respond="lastNode", auth=None):
    p = {"httpMethod": method, "path": path, "responseMode": respond, "options": {}}
    if respond == "lastNode":
        p["responseData"] = "firstEntryJson"
    extra = {"webhookId": uid()}
    if auth:
        p["authentication"] = "headerAuth"
        extra["credentials"] = {"httpHeaderAuth": CRED}
    return node(name, "n8n-nodes-base.webhook", 2, pos, p, **extra)


def code(name, js, pos):
    return node(name, "n8n-nodes-base.code", 2, pos, {"mode": "runOnceForEachItem", "jsCode": js.strip()})


def cond(left, op_type, operation, right=None):
    c = {"id": uid(), "leftValue": left, "rightValue": "" if right is None else right,
         "operator": {"type": op_type, "operation": operation}}
    if right is None:
        c["operator"]["singleValue"] = True
    return c


def if_node(name, conditions, pos, loose=False, **extra):
    p = {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose" if loose else "strict",
                        "version": 2},
            "conditions": conditions,
            "combinator": "and",
        },
        "options": {},
    }
    if loose:
        p["looseTypeValidation"] = True
    return node(name, "n8n-nodes-base.if", 2.2, pos, p, **extra)


def set_fields(name, fields, pos):
    return node(
        name, "n8n-nodes-base.set", 3.4, pos,
        {"mode": "manual",
         "assignments": {"assignments": [{"id": uid(), "name": k, "value": v, "type": t} for k, v, t in fields]},
         "options": {}},
    )


def http(name, method, path, pos, query=None, body=None, **extra):
    p = {"method": method, "url": f"{BASE}/{path}", "options": {}}
    if query:
        p["sendQuery"] = True
        p["queryParameters"] = {"parameters": [{"name": k, "value": v} for k, v in query]}
    if body:
        p["sendBody"] = True
        p["bodyParameters"] = {"parameters": [{"name": k, "value": v} for k, v in body]}
    return node(name, "n8n-nodes-base.httpRequest", 4.2, pos, p, retryOnFail=True, maxTries=3,
                waitBetweenTries=5000, onError="continueErrorOutput", **extra)


def respond(name, body, pos, code_=None, **extra):
    opts = {"responseCode": code_} if code_ is not None else {}
    return node(name, "n8n-nodes-base.respondToWebhook", 1.1, pos,
                {"respondWith": "json", "responseBody": body, "options": opts}, **extra)


def sticky(name, text, pos, w, h, color):
    return node(name, "n8n-nodes-base.stickyNote", 1, pos, {"content": text, "width": w, "height": h, "color": color})


def link(conns, src, dst, out=0):
    outs = conns.setdefault(src, {"main": []})["main"]
    while len(outs) <= out:
        outs.append([])
    outs[out].append({"node": dst, "type": "main", "index": 0})


# ===================================================================== main
A = "$('Map alert fields').item.json"

main_nodes = [
    webhook("Receive SolarWinds alert", "solarwinds-alert", "POST", [0, 0], respond="responseNode", auth=True),
    if_node(
        "Is payload valid?",
        [cond("={{ $json.body.NodeName }}", "string", "notEmpty"),
         cond("={{ $json.body.MetricName }}", "string", "notEmpty")],
        [224, 0], loose=True,
    ),
    respond(
        "Reject invalid payload",
        '={{ { error: "validation_error", message: "NodeName and MetricName are required" } }}',
        [448, 192], code_=400,
    ),
    set_fields(
        "Map alert fields",
        [
            ("node", "={{ $json.body.NodeName.trim() }}", "string"),
            ("metric", "={{ $json.body.MetricName.trim() }}", "string"),
            ("value", "={{ $json.body.MetricValue }}", "number"),
            ("threshold", "={{ $json.body.Threshold }}", "number"),
            ("severity", "={{ $json.body.Severity ?? 'Information' }}", "string"),
            ("message", "={{ $json.body.Message ?? '' }}", "string"),
            ("alertAt", "={{ $json.body.TriggeredAt ?? $now.toISO() }}", "string"),
            ("priority", "={{ { Critical: 'P1', Warning: 'P2' }[$json.body.Severity] ?? '' }}", "string"),
            ("alertType",
             "={{ /down|status|ping/i.test($json.body.MetricName) ? 'Availability'"
             " : /disk|volume|storage/i.test($json.body.MetricName) ? 'Capacity'"
             " : /cpu|memory|ram|load/i.test($json.body.MetricName) ? 'Performance' : 'Other' }}",
             "string"),
            ("dedupeKey", "={{ ($json.body.NodeName.trim() + '|' + $json.body.MetricName.trim()).toLowerCase() }}",
             "string"),
        ],
        [448, 0],
    ),
    if_node(
        "Needs a ticket?",
        [cond("={{ $json.priority }}", "string", "notEmpty"),
         cond("={{ $json.alertType === 'Availability' || $json.value >= $json.threshold }}", "boolean", "true")],
        [672, 0],
        notes="Critical or Warning only",
        notesInFlow=True,
    ),
    respond(
        "Skip alert",
        "={{ { outcome: 'ignored', reason: $json.priority ? 'Value is below the threshold'"
        " : 'Informational severity', dedupeKey: $json.dedupeKey } }}",
        [896, 192],
    ),
    http(
        "Find open ticket",
        "GET", "mock/sot/find", [896, 0],
        query=[("key", "={{ $json.dedupeKey }}")],
        notes="Decides create vs. update",
        notesInFlow=True,
    ),
    if_node("Ticket already open?", [cond("={{ $json.found }}", "boolean", "true")], [1120, 0]),
    http(
        "Add note to ticket",
        "POST", "mock/aranda/update", [1344, -96],
        body=[
            ("ticketId", "={{ $json.record.ticketId }}"),
            ("priority", "={{ " + A + ".priority }}"),
            ("note", "=Repeated alert: {{ " + A + ".metric }} = {{ " + A + ".value }} (threshold {{ "
             + A + ".threshold }}) at {{ " + A + ".alertAt }}"),
        ],
    ),
    http(
        "Create ticket in service desk",
        "POST", "mock/aranda/create", [1344, 96],
        body=[
            ("title", "=[{{ " + A + ".priority }}] {{ " + A + ".alertType }}: {{ " + A + ".metric }} on {{ "
             + A + ".node }}"),
            ("priority", "={{ " + A + ".priority }}"),
            ("description", "={{ " + A + ".message }} | value {{ " + A + ".value }}, threshold {{ "
             + A + ".threshold }}"),
            ("source", "SolarWinds"),
        ],
    ),
    http(
        "Save ticket in source of truth",
        "POST", "mock/sot/upsert", [1568, 0],
        body=[
            ("key", "={{ " + A + ".dedupeKey }}"),
            ("ticketId", "={{ $json.id }}"),
            ("alertType", "={{ " + A + ".alertType }}"),
            ("priority", "={{ " + A + ".priority }}"),
            ("alertAt", "={{ " + A + ".alertAt }}"),
        ],
    ),
    respond(
        "Return ticket result",
        "={{ { outcome: $json.isNewTicket ? 'created' : 'updated', ticketId: $json.record.ticketId,"
        " occurrences: $json.record.occurrences, dedupeKey: $json.record.key } }}",
        [1792, 0],
    ),
    respond(
        "Return upstream error",
        '={{ { error: "upstream_error", message: "Service desk or source of truth unavailable. '
        'The alert can be re-sent safely." } }}',
        [1792, 288], code_=502,
        notes="Sanitized, safe to re-send",
        notesInFlow=True,
    ),
]
mc = {}
link(mc, "Receive SolarWinds alert", "Is payload valid?")
link(mc, "Is payload valid?", "Map alert fields", 0)
link(mc, "Is payload valid?", "Reject invalid payload", 1)
link(mc, "Map alert fields", "Needs a ticket?")
link(mc, "Needs a ticket?", "Find open ticket", 0)
link(mc, "Needs a ticket?", "Skip alert", 1)
link(mc, "Find open ticket", "Ticket already open?", 0)
link(mc, "Find open ticket", "Return upstream error", 1)
link(mc, "Ticket already open?", "Add note to ticket", 0)
link(mc, "Ticket already open?", "Create ticket in service desk", 1)
for n in ("Add note to ticket", "Create ticket in service desk"):
    link(mc, n, "Save ticket in source of truth", 0)
    link(mc, n, "Return upstream error", 1)
link(mc, "Save ticket in source of truth", "Return ticket result", 0)
link(mc, "Save ticket in source of truth", "Return upstream error", 1)

# Layout on the 16px grid: main row y=0, side outputs below, ~224px between columns,
# and a gap between stages so the zones never overlap.
POS = {
    "Receive SolarWinds alert": [0, 0],
    "Is payload valid?": [256, 0],
    "Reject invalid payload": [480, 192],
    "Map alert fields": [720, 0],
    "Needs a ticket?": [944, 0],
    "Skip alert": [1168, 192],
    "Find open ticket": [1408, 0],
    "Ticket already open?": [1632, 0],
    "Add note to ticket": [1856, -160],
    "Create ticket in service desk": [1856, 160],
    "Save ticket in source of truth": [2080, 0],
    "Return ticket result": [2304, 0],
    "Return upstream error": [2304, 384],
}
for n in main_nodes:
    n["position"] = POS[n["name"]]


def frame_box(name, text, points, color):
    # Framing from n8n-io/skills STICKY_NOTES.md (nodes are 96x96): 96 above for the header,
    # side padding widened to the 56px ceiling, plus room below for node labels and notes.
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    left, right, top, bottom = min(xs), max(xs) + 96, min(ys), max(ys) + 96
    return sticky(name, text, [left - 56, top - 96], right - left + 112, bottom - top + 160, color)


def frame(name, text, members, color):
    return frame_box(name, text, [POS[m] for m in members], color)


main_nodes += [
    frame("Zone: validate payload", "### 1. Validate payload\nMissing fields get a 400.",
          ["Is payload valid?", "Reject invalid payload"], 5),
    frame("Zone: business rules", "### 2. Apply business rules\nOnly real problems become tickets.",
          ["Map alert fields", "Needs a ticket?", "Skip alert"], 5),
    frame("Zone: ticket", "### 3. Create or update the ticket\nCheck the source of truth first, so nothing duplicates.",
          ["Find open ticket", "Ticket already open?", "Add note to ticket", "Create ticket in service desk",
           "Save ticket in source of truth", "Return ticket result", "Return upstream error"], 4),
]

main_wf = {
    "id": "wbSolarwindsFlow",
    "name": "Webhook: create service desk tickets from SolarWinds alerts",
    "description": (
        "Turns SolarWinds alerts into service desk tickets without duplicates. Business rules decide which alerts "
        "deserve a ticket, and the source of truth decides whether to create a new ticket or update the open one, "
        "so re-sending an alert is always safe. Synthetic demo: the downstream systems are mocked."
    ),
    "nodes": main_nodes,
    "connections": mc,
    "nodeGroups": [],
    "settings": {"executionOrder": "v1"},
    "tags": [{"name": "monitoring"}, {"name": "service desk"}, {"name": "demo"}],
    "active": False,
    "pinData": {},
}

# ===================================================================== mocks
STORE = ("const sd = $getWorkflowStaticData('global');\n"
         "sd.sot = sd.sot || {};\n"
         "sd.desk = sd.desk || { seq: 1000, tickets: {}, outage: false };\n")

mock_nodes, kc = [], {}


def endpoint(hook_name, path, method, code_name, js, x0, y, respond_name=None):
    if respond_name:
        mock_nodes.append(webhook(hook_name, path, method, [x0, y], respond="responseNode"))
        mock_nodes.append(code(code_name, js, [x0 + 224, y]))
        mock_nodes.append(respond(respond_name, "={{ $json.body }}", [x0 + 448, y], code_="={{ $json.statusCode }}"))
        link(kc, hook_name, code_name)
        link(kc, code_name, respond_name)
    else:
        mock_nodes.append(webhook(hook_name, path, method, [x0, y]))
        mock_nodes.append(code(code_name, js, [x0 + 224, y]))
        link(kc, hook_name, code_name)


endpoint("On find record", "mock/sot/find", "GET", "Look up record", STORE + """
const key = String($json.query.key || '').toLowerCase();
const record = sd.sot[key] || null;
return { json: { found: record !== null, record } };
""", 0, 0)
endpoint("On save record", "mock/sot/upsert", "POST", "Upsert record", STORE + """
const b = $json.body;
const key = String(b.key).toLowerCase();
const prev = sd.sot[key];
const isNewTicket = !prev || prev.ticketId !== b.ticketId;
const record = {
  key,
  ticketId: b.ticketId,
  alertType: b.alertType,
  priority: b.priority,
  status: 'Open',
  firstAlertAt: isNewTicket ? b.alertAt : prev.firstAlertAt,
  lastAlertAt: b.alertAt,
  occurrences: isNewTicket ? 1 : prev.occurrences + 1,
};
sd.sot[key] = record;
return { json: { isNewTicket, record } };
""", 0, 192)
endpoint("On create ticket", "mock/aranda/create", "POST", "Create ticket", STORE + """
if (sd.desk.outage) {
  return { json: { statusCode: 503, body: { error: 'service desk unavailable (simulated outage)' } } };
}
const b = $json.body;
sd.desk.seq += 1;
const id = 'ARD-' + sd.desk.seq;
const ticket = {
  id,
  title: b.title,
  priority: b.priority,
  description: b.description,
  source: b.source,
  status: 'Open',
  createdAt: new Date().toISOString(),
  updates: [],
};
sd.desk.tickets[id] = ticket;
return { json: { statusCode: 200, body: ticket } };
""", 544, 0, respond_name="Return create result")
endpoint("On add note", "mock/aranda/update", "POST", "Append note", STORE + """
const b = $json.body;
const ticket = sd.desk.tickets[b.ticketId];
if (!ticket) {
  return { json: { error: 'ticket not found', ticketId: b.ticketId } };
}
ticket.updates.push({ at: new Date().toISOString(), note: b.note });
ticket.priority = b.priority;
return { json: ticket };
""", 544, 192)
endpoint("On show state", "mock/state", "GET", "Read all data", STORE + """
const tickets = Object.values(sd.desk.tickets);
return { json: { serviceDeskTickets: tickets.length, outage: sd.desk.outage, sourceOfTruth: sd.sot, serviceDesk: tickets } };
""", 1328, 0)
endpoint("On reset", "mock/reset", "POST", "Clear demo data", """
const sd = $getWorkflowStaticData('global');
sd.sot = {};
sd.desk = { seq: 1000, tickets: {}, outage: false };
return { json: { reset: true } };
""", 1328, 192)
endpoint("On toggle outage", "mock/outage", "POST", "Set outage flag", STORE + """
sd.desk.outage = $json.body.on === true || $json.body.on === 'true';
return { json: { outage: sd.desk.outage } };
""", 1328, 384)


mock_nodes += [
    frame_box("Zone: source of truth", "### Source of truth (mock)\nOne record per alert key.",
              [[0, 0], [224, 192]], 5),
    frame_box("Zone: service desk", "### Service desk (mock)\nStands in for Aranda.",
              [[544, 0], [992, 192]], 4),
    frame_box("Zone: demo utilities", "### Demo utilities\nInspect, reset, simulate an outage.",
              [[1328, 0], [1552, 384]], 7),
]

mock_wf = {
    "id": "wbMockSystems001",
    "name": "Webhook: mock source of truth and service desk",
    "description": (
        "Synthetic stand-ins for the internal source-of-truth service and the Aranda service desk, so the alert "
        "workflow can be demoed without real systems. State lives in workflow static data."
    ),
    "nodes": mock_nodes,
    "connections": kc,
    "settings": {"executionOrder": "v1"},
    "tags": [{"name": "demo"}, {"name": "mock"}],
    "active": False,
    "pinData": {},
}

cred = [{
    "id": CRED["id"],
    "name": CRED["name"],
    "type": "httpHeaderAuth",
    "data": {"name": "X-Webhook-Token", "value": "demo-token-123"},
}]

(OUT / "1_mock_systems.json").write_text(json.dumps(mock_wf, indent=2, ensure_ascii=False), encoding="utf-8")
(OUT / "2_solarwinds_to_servicedesk.json").write_text(json.dumps(main_wf, indent=2, ensure_ascii=False),
                                                       encoding="utf-8")
(OUT / "credential_webhook_token.json").write_text(json.dumps(cred, indent=2), encoding="utf-8")
print("ok")
