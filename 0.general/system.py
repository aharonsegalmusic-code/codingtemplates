# pip install psutil

import psutil
from enum import Enum
import json


# -------------------------
# SETTINGS
# -------------------------
WRITE_JSON = False          # << Toggle ON/OFF
JSON_FILE_NAME = "process_report.json"
# -------------------------


class ConcernLevel(Enum):
    NONE = "None"
    LOW = "Low"
    MID = "Mid"
    HI = "High"


def evaluate_concern(cpu: float, mem: float) -> ConcernLevel:
    score = (cpu / 10) + (mem / 200)  # Weighted mix

    if score <= 0.5:
        return ConcernLevel.NONE
    elif score <= 1.5:
        return ConcernLevel.LOW
    elif score <= 3:
        return ConcernLevel.MID
    else:
        return ConcernLevel.HI


def icon(level: ConcernLevel) -> str:
    return {
        ConcernLevel.NONE: "🟢",
        ConcernLevel.LOW: "🟡",
        ConcernLevel.MID: "🟠",
        ConcernLevel.HI: "🔴"
    }[level]


def print_group(title: str, processes: list):
    print(f"\n\n===== {title} =====")
    for p in processes:
        print(
            f"{icon(p['level'])}  {p['name']:<30} "
            f"CPU: {p['cpu']:<6.1f}  "
            f"Memory: {p['mem']:<6.1f} MB"
        )


def main():
    processes_info = []

    for proc in psutil.process_iter(["name", "cpu_percent", "memory_info"]):
        try:
            name = proc.info["name"] or "Unknown"
            cpu = proc.info["cpu_percent"] or 0
            mem = (proc.info["memory_info"].rss / 1024 / 1024) if proc.info["memory_info"] else 0

            level = evaluate_concern(cpu, mem)

            processes_info.append({
                "name": name,
                "cpu": cpu,
                "mem": mem,
                "level": level
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Group processes by level
    groups = {
        ConcernLevel.HI: [],
        ConcernLevel.MID: [],
        ConcernLevel.LOW: [],
        ConcernLevel.NONE: []
    }

    for p in processes_info:
        groups[p["level"]].append(p)

    # Print to console
    print_group("HIGH CONCERN 🔴", groups[ConcernLevel.HI])
    print_group("MID CONCERN 🟠", groups[ConcernLevel.MID])
    print_group("LOW CONCERN 🟡", groups[ConcernLevel.LOW])
    print_group("NO CONCERN 🟢", groups[ConcernLevel.NONE])

    # ---------------------------------------------------
    # JSON OUTPUT (if enabled)
    # ---------------------------------------------------
    if WRITE_JSON:
        json_output = {
            "high_concern": groups[ConcernLevel.HI],
            "mid_concern": groups[ConcernLevel.MID],
            "low_concern": groups[ConcernLevel.LOW],
            "no_concern": groups[ConcernLevel.NONE]
        }

        # Convert Enum to string
        def fix_enum(obj):
            if isinstance(obj, ConcernLevel):
                return obj.value
            return obj

        # Write JSON file
        with open(JSON_FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(json_output, f, indent=4, default=fix_enum)

        print(f"\n\n📄 JSON written to: {JSON_FILE_NAME}")


if __name__ == "__main__":
    main()
