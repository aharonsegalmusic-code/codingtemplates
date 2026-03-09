# port_report.py
# this script writes a text report about listening ports and common dev ports

import argparse
import datetime
import os
import platform
import socket
import sys


def now_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def file_stamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def try_import_psutil():
    try:
        import psutil
        return psutil
    except Exception:
        return None


def can_connect(host, port, timeout_seconds):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_seconds)
    try:
        s.connect((host, int(port)))
        return True, "open"
    except ConnectionRefusedError:
        return False, "refused"
    except socket.timeout:
        return False, "timeout"
    except OSError as e:
        return False, "oserror " + str(e)
    finally:
        try:
            s.close()
        except Exception:
            pass


def format_row(cols, widths):
    parts = []
    for i in range(len(cols)):
        val = str(cols[i])
        if len(val) > widths[i]:
            val = val[: widths[i] - 3] + "..."
        parts.append(val.ljust(widths[i]))
    return "  ".join(parts)


def get_listeners_psutil(psutil):
    listeners = []
    seen = set()

    for c in psutil.net_connections(kind="inet"):
        if c.status != "LISTEN":
            continue

        if not c.laddr:
            continue

        ip = c.laddr.ip if hasattr(c.laddr, "ip") else c.laddr[0]
        port = c.laddr.port if hasattr(c.laddr, "port") else c.laddr[1]
        pid = c.pid

        key = (ip, port, pid)
        if key in seen:
            continue
        seen.add(key)

        pname = ""
        try:
            if pid:
                pname = psutil.Process(pid).name()
        except Exception:
            pname = ""

        listeners.append(
            {
                "ip": ip,
                "port": int(port),
                "pid": pid or "",
                "process": pname,
            }
        )

    listeners.sort(key=lambda x: (x["port"], x["ip"]))
    return listeners


def index_listeners_by_port(listeners):
    by_port = {}
    for item in listeners:
        p = item["port"]
        by_port.setdefault(p, []).append(item)
    return by_port


def write_report(path, ports_of_interest, expected_by_port, timeout_seconds, max_listeners):
    lines = []

    lines.append("port report")
    lines.append("generated at: " + now_stamp())
    lines.append("os: " + platform.platform())
    lines.append("python: " + sys.version.replace("\n", " "))
    lines.append("cwd: " + os.getcwd())
    lines.append("")

    psutil = try_import_psutil()
    if psutil is None:
        lines.append("note: psutil is not installed so this report will not list all listening ports")
        lines.append("note: install it with: pip install psutil")
        lines.append("")

        lines.append("ports of interest status by tcp connect attempt to 127.0.0.1")
        widths = [14, 8, 10, 18]
        lines.append(format_row(["expected", "port", "reachable", "detail"], widths))
        lines.append(format_row(["-" * 8, "-" * 4, "-" * 9, "-" * 6], widths))

        for p in ports_of_interest:
            ok, detail = can_connect("127.0.0.1", p, timeout_seconds)
            expected = expected_by_port.get(int(p), "")
            lines.append(format_row([expected, p, str(ok), detail], widths))

        lines.append("")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return

    listeners = get_listeners_psutil(psutil)
    by_port = index_listeners_by_port(listeners)

    lines.append("ports of interest listening status")
    widths = [16, 8, 10, 16, 10, 24]
    lines.append(format_row(["expected", "port", "listening", "ip", "pid", "process"], widths))
    lines.append(format_row(["-" * 8, "-" * 4, "-" * 9, "-" * 2, "-" * 3, "-" * 7], widths))

    for p in ports_of_interest:
        expected = expected_by_port.get(int(p), "")
        items = by_port.get(int(p), [])
        if not items:
            lines.append(format_row([expected, p, "no", "", "", ""], widths))
        else:
            first = True
            for it in items:
                if first:
                    lines.append(format_row([expected, p, "yes", it["ip"], it["pid"], it["process"]], widths))
                    first = False
                else:
                    lines.append(format_row(["", "", "", it["ip"], it["pid"], it["process"]], widths))

    lines.append("")
    lines.append("all listening ports")
    widths = [8, 18, 10, 28]
    lines.append(format_row(["port", "ip", "pid", "process"], widths))
    lines.append(format_row(["-" * 4, "-" * 2, "-" * 3, "-" * 7], widths))

    shown = 0
    for it in listeners:
        lines.append(format_row([it["port"], it["ip"], it["pid"], it["process"]], widths))
        shown += 1
        if int(max_listeners) > 0 and shown >= int(max_listeners):
            break

    lines.append("")
    lines.append("notes")
    lines.append("- expected is what you normally run on that port in this project")
    lines.append("- if a port is no but you expected a ui to be up, the container is likely not running or not publishing that port")
    lines.append("- if pid or process is blank you may need admin privileges on your os")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="", help="output file path")
    parser.add_argument("--timeout", default="0.2", help="tcp connect timeout seconds for fallback mode")
    parser.add_argument("--max", default="300", help="max listening ports to list when psutil is available")
    args = parser.parse_args()

    ports_of_interest = [
        27017,
        3306,
        6379,
        8080,
        8081,
        8978,
        8000,
        8001,
        8002,
        9092,
        29092,
        5540,
    ]

    expected_by_port = {
        27017: "mongodb",
        3306: "mysql",
        6379: "redis",
        8080: "kafka ui",
        8081: "mongo express",
        8978: "cloudbeaver",
        8000: "producer api",
        8001: "optional api",
        8002: "analytics api",
        9092: "kafka host",
        29092: "kafka internal",
        5540: "redisinsight",
    }

    out_path = args.out.strip()
    if out_path == "":
        out_path = "ports_report_" + file_stamp() + ".txt"

    write_report(out_path, ports_of_interest, expected_by_port, float(args.timeout), int(args.max))
    print("wrote report to:", os.path.abspath(out_path))


if __name__ == "__main__":
    main()