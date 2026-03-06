#!/usr/bin/env python3
"""
Load Compliance Division roster directly into ocss_app_state.json.

Run once (or repeatedly — it is idempotent):
    python3 scripts/load_compliance_roster.py

What this script does:
 • Creates 7 Compliance units with supervisors, staff, and caseload assignments
 • Upserts every person as an app user (role Supervisor or Support Officer)
 • Preserves ALL existing state (other departments, QA data, etc.)

Cross‑unit workers:
 • Lynniece Love       primary unit 18205 (all 5 caseloads consolidated there)
 • Antionette Robinson primary unit 18203 (all 3 caseloads incl. Locate/CCPA)
"""
import json, datetime
from pathlib import Path

STATE_FILE = Path("data/state/ocss_app_state.json")
DEPT = "Compliance"


def _name_key(s: str) -> str:
    return "".join(c.lower() for c in str(s or "") if c.isalpha())


def _series_prefix(cl: str) -> str:
    """Return 4-char caseload series prefix (e.g. '182301' → '1823')."""
    return cl[:4] if len(cl) >= 4 else cl


# ─── Compliance Division Data ────────────────────────────────────────────────
#  Format: unit_name → {supervisor, staff, assignments}
#  All names in "First Last" order (converted from "Last, First" source data).
# ─────────────────────────────────────────────────────────────────────────────
UNITS: dict = {
    "Compliance Unit 18203": {
        "supervisor": "Ezra Miklowski",
        "staff": [
            "Clovis DeAlmeida-Paludo",
            "David Judy",
            "Veronica Zatezalo",
            "Chantel Henderson",
            "Nikhol Rice",
            "Antionette Robinson",   # primary here; also has Locate/CCPA from 18207
            "Theresa Kamenir",
        ],
        "assignments": {
            "Clovis DeAlmeida-Paludo": ["182301", "182360"],
            "David Judy":              ["182302", "182305"],
            "Veronica Zatezalo":       ["182303", "182304"],
            "Chantel Henderson":       ["182306", "182310"],
            "Nikhol Rice":             ["182307", "182308"],
            "Antionette Robinson":     ["182309", "182730", "182740"],  # incl. cross-unit
            "Theresa Kamenir":         ["182311"],
            "Ezra Miklowski":          ["182320", "182330", "182340", "182350"],
        },
    },
    "Compliance Unit 18204": {
        "supervisor": "Karen Beeble",
        "staff": [
            "Michael Haygood",
            "Jazzmine Brown",
            "Destiny Nance",
            "Christie Ward",
            "Michelle Dowd",
            "Angela Booker-Speed",
            # Lynniece Love's 182460 is consolidated under her primary unit 18205
        ],
        "assignments": {
            "Michael Haygood":     ["182401", "182406", "182408", "182410", "182450"],
            "Jazzmine Brown":      ["182404"],
            "Destiny Nance":       ["182405"],
            "Christie Ward":       ["182407"],
            "Michelle Dowd":       ["182409"],
            "Angela Booker-Speed": ["182411"],
            "Karen Beeble":        ["182430", "182440"],
        },
    },
    "Compliance Unit 18205": {
        "supervisor": "Christie Cunningham",
        "staff": [
            "Nyree Morrison",
            "William Berry",
            "John Cook",
            "Barbara Jackson",
            "Angela Ray",
            "Lynniece Love",         # primary here; handles CNS across multiple units
            "Julie Solomon",
            "Sharhonda Corothers",
            "Valerie Adams",
            "Katara Pearson",
        ],
        "assignments": {
            "Nyree Morrison":       ["182501"],
            "William Berry":        ["182502"],
            "John Cook":            ["182504"],
            "Barbara Jackson":      ["182505"],
            "Angela Ray":           ["182506"],
            # Love's caseloads consolidated here from 18204/18205/18207
            "Lynniece Love":        ["182460", "182507", "182512", "182560", "182760"],
            "Julie Solomon":        ["182508"],
            "Sharhonda Corothers":  ["182509"],
            "Valerie Adams":        ["182510"],
            "Katara Pearson":       ["182511"],
            "Christie Cunningham":  ["182530", "182540", "182550"],
        },
    },
    "Compliance Unit 18206": {
        "supervisor": "Kimberly Mell",
        "staff": [
            "Ivonne Vega",       # handles FV-Bilingual, Bilingual caseloads
            "Kaytlin Dial",
            "Anaiya Manuel",
            "Jariya Polk",
            "Gloria Stefanick",
            "Breanna Byrd",
        ],
        "assignments": {
            "Ivonne Vega":      ["182220", "182221", "182611"],
            "Kaytlin Dial":     ["182601", "182602", "182660"],
            "Anaiya Manuel":    ["182604", "182609"],
            "Jariya Polk":      ["182605", "182608"],
            "Gloria Stefanick": ["182606"],
            "Breanna Byrd":     ["182607", "182610"],
            "Kimberly Mell":    ["182630", "182640", "182650"],
        },
    },
    "Compliance Unit 18207": {
        "supervisor": "Tiffany Mitchell",
        "staff": [
            "Jacqueline Hernandez-Mack",
            "Victoria Brown",
            "Kathryn Randall",
            "Christina Coles",
            "Alwyn Reid",
            "Dawn Sloan",
            "Mauriana Lynch",
            # Antionette Robinson (182730/182740) → consolidated in 18203
            # Lynniece Love (182760) → consolidated in 18205
        ],
        "assignments": {
            "Tiffany Mitchell":          ["182701", "182702", "182750"],
            "Jacqueline Hernandez-Mack": ["182704"],
            "Victoria Brown":            ["182705"],
            "Kathryn Randall":           ["182706"],
            "Christina Coles":           ["182707"],
            "Alwyn Reid":                ["182708"],
            "Dawn Sloan":                ["182709"],
            "Mauriana Lynch":            ["182710"],
        },
    },
    "Compliance Unit 18208": {
        "supervisor": "Alison Donze",
        "staff": [
            "Cynthia Hinske",
            "Gay Cain",
            "Dana Malone",
            "Shalawn Gilbert",   # also handles FV-R, Empl-R, CCPA, CNS
            "Maggie Jarus",      # also handles FV-I, Empl-I
            "Tonell Evans",
            "Ronnice Edmonds",
            "Elisha Crutcher",
        ],
        "assignments": {
            "Cynthia Hinske":  ["182801"],
            "Gay Cain":        ["182802"],
            "Dana Malone":     ["182803"],
            "Shalawn Gilbert": ["182804", "182811", "182813", "182840", "182860"],
            "Maggie Jarus":    ["182806", "182812", "182814"],
            "Tonell Evans":    ["182807"],
            "Ronnice Edmonds": ["182808"],
            "Elisha Crutcher": ["182810"],
            "Alison Donze":    ["182815"],
        },
    },
    # Special/misc compliance caseloads listed by supervisor last name only;
    # no full names available for Dillinger or Dobbins supervisors.
    "Compliance Unit - Misc": {
        "supervisor": "",
        "staff": [
            "Tameika Hill-White",   # handles 182199 (Dillinger)
            "Cynthia Hill",         # handles 189999 (Dobbins)
        ],
        "assignments": {
            "Tameika Hill-White": ["182199"],
            "Cynthia Hill":       ["189999"],
        },
    },
}

# ─── Load state ──────────────────────────────────────────────────────────────
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
state: dict = {}
if STATE_FILE.exists():
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"⚠ Could not load existing state ({exc}); starting fresh.")

users: list = state.get("users", [])
units: dict = state.get("units", {})
reports: dict = state.get("reports_by_caseload", {})

# Index existing users by normalised name key
existing_idx: dict[str, int] = {_name_key(u["name"]): i for i, u in enumerate(users)}

stats = {"added_users": 0, "updated_users": 0, "new_caseloads": 0, "new_units": 0}


def upsert_user(name: str, role: str, unit_name: str) -> None:
    key = _name_key(name)
    record = {
        "name":       name,
        "role":       role,
        "department": DEPT,
        "unit":       unit_name,
        "unit_role":  "",
    }
    if key in existing_idx:
        idx = existing_idx[key]
        users[idx].update(record)
        stats["updated_users"] += 1
    else:
        existing_idx[key] = len(users)
        users.append(record)
        stats["added_users"] += 1


# ─── Apply compliance data ───────────────────────────────────────────────────
for unit_name, unit_data in UNITS.items():
    sup_name = unit_data["supervisor"]
    staff    = unit_data["staff"]
    asst     = unit_data["assignments"]

    # Collect all caseloads for this unit
    all_cls: list[str] = []
    for cl_list in asst.values():
        for cl in cl_list:
            if cl not in all_cls:
                all_cls.append(cl)

    prefixes = sorted({_series_prefix(cl) for cl in all_cls})

    # Build / update unit record
    unit_rec = units.get(unit_name, {})
    is_new = unit_name not in units
    if is_new:
        stats["new_units"] += 1

    unit_rec["department"]              = DEPT
    unit_rec["unit_type"]               = "standard"
    if sup_name:
        unit_rec["supervisor"]          = sup_name
    unit_rec["caseload_series_prefixes"] = sorted(
        set(unit_rec.get("caseload_series_prefixes", [])) | set(prefixes)
    )
    unit_rec["caseload_numbers"] = sorted(
        set(unit_rec.get("caseload_numbers", [])) | set(all_cls)
    )

    # team_leads: none in this compliance data
    unit_rec.setdefault("team_leads", [])

    # support_officers list
    so_list = unit_rec.setdefault("support_officers", [])
    for worker in staff:
        if worker not in so_list:
            so_list.append(worker)

    # assignments
    unit_asst = unit_rec.setdefault("assignments", {})
    for worker, caseloads in asst.items():
        w_list = unit_asst.setdefault(worker, [])
        for cl in caseloads:
            if cl not in w_list:
                w_list.append(cl)
                stats["new_caseloads"] += 1
            reports.setdefault(cl, [])   # ensure slot in reports_by_caseload

    units[unit_name] = unit_rec

    # Upsert supervisor (as Support Officer in their own unit for caseload tracking)
    if sup_name:
        upsert_user(sup_name, "Supervisor", unit_name)

    # Upsert staff
    for worker in staff:
        upsert_user(worker, "Support Officer", unit_name)


# ─── Save ────────────────────────────────────────────────────────────────────
state["users"]               = users
state["units"]               = units
state["reports_by_caseload"] = reports
state["saved_at"]            = datetime.datetime.now().isoformat(timespec="seconds")

STATE_FILE.write_text(
    json.dumps(state, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(
    f"✅ Compliance Division loaded.\n"
    f"   Users added:       {stats['added_users']}\n"
    f"   Users updated:     {stats['updated_users']}\n"
    f"   Units created:     {stats['new_units']}\n"
    f"   Caseloads assigned:{stats['new_caseloads']}\n"
    f"   State saved → {STATE_FILE}"
)
