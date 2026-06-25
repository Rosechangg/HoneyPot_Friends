#!/usr/bin/env python3
"""Auto-sync the marketplace from each plugin's own manifest + filesystem.

이 스크립트는 `plugins/<name>/`를 스캔해서 `.claude-plugin/marketplace.json`과
`README.md`의 플러그인 표를 자동으로 맞춰준다. 기여자는 자기 플러그인 폴더만
손대면 되고, 마켓플레이스 등록/버전/표는 push 시 GitHub Actions가 알아서 갱신한다.

Source of truth:
  - plugin.json  ->  version, author, license, (신규 플러그인의) description
  - filesystem   ->  source, skills, commands, agents (실제 폴더/파일 기준)
  - marketplace  ->  기존 플러그인의 description 은 사람이 큐레이션한 값 유지

Usage:
  python scripts/sync_marketplace.py          # 동기화 + 파일 기록 (push 워크플로우)
  python scripts/sync_marketplace.py --check   # 검증만, 기록 안 함 (PR 워크플로우)

Exit code:
  0 = 정상(검증 통과)
  1 = 검증 실패(잘못된 JSON / name 누락 등)
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MP_PATH = ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = ROOT / "plugins"
README_PATH = ROOT / "README.md"

# marketplace 항목 키 정렬 순서 (기존 컨벤션과 동일)
CANON_ORDER = [
    "name", "source", "description", "version",
    "author", "license", "category", "strict",
    "commands", "skills", "agents",
]

README_START = "<!-- PLUGINS-TABLE:START -->"
README_END = "<!-- PLUGINS-TABLE:END -->"

errors: list[str] = []
notes: list[str] = []


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        errors.append(f"{rel(p)}: invalid JSON ({e})")
        return None


def discover_plugins() -> dict[str, dict]:
    """dirname -> plugin.json dict (유효한 것만)."""
    found: dict[str, dict] = {}
    if not PLUGINS_DIR.is_dir():
        return found
    for d in sorted(PLUGINS_DIR.iterdir()):
        if not d.is_dir():
            continue
        pj = d / ".claude-plugin" / "plugin.json"
        if not pj.is_file():
            errors.append(f"plugins/{d.name}: missing .claude-plugin/plugin.json")
            continue
        data = load_json(pj)
        if data is None:
            continue
        if not data.get("name"):
            errors.append(f"{rel(pj)}: missing 'name'")
            continue
        found[d.name] = data
    return found


def md_list(dirpath: Path, subdir: str) -> list[str]:
    sub = dirpath / subdir
    if not sub.is_dir():
        return []
    return sorted(f"./{subdir}/{p.name}" for p in sub.glob("*.md"))


def order_preserving(existing: list[str], desired: list[str]) -> list[str]:
    """기존 순서 유지 + 사라진 것 제거 + 새 것은 정렬해 append (churn 최소화)."""
    desired_set = set(desired)
    kept = [x for x in (existing or []) if x in desired_set]
    added = [x for x in desired if x not in set(kept)]
    return kept + added


def build_entry(dirname: str, plugin: dict, existing: dict | None) -> dict:
    e = dict(existing) if existing else {}
    e["name"] = plugin["name"]
    e["source"] = f"./plugins/{dirname}"

    # version 은 항상 plugin.json 기준으로 전파 ("수정내용" 의 핵심 신호)
    if "version" in plugin:
        e["version"] = plugin["version"]
    # description / author / license 는 마켓플레이스 큐레이션 값을 유지하고,
    # 없을 때(신규 플러그인)만 plugin.json 에서 채운다. (오타성 author 덮어쓰기 방지)
    for k in ("description", "author", "license"):
        if k not in e and k in plugin:
            e[k] = plugin[k]

    # filesystem = source of truth
    pdir = PLUGINS_DIR / dirname
    cmds = order_preserving(e.get("commands", []), md_list(pdir, "commands"))
    agents = order_preserving(e.get("agents", []), md_list(pdir, "agents"))
    if cmds:
        e["commands"] = cmds
    else:
        e.pop("commands", None)
    if (pdir / "skills").is_dir():
        e["skills"] = ["./skills"]
    else:
        e.pop("skills", None)
    if agents:
        e["agents"] = agents
    else:
        e.pop("agents", None)

    # 표준 키 순서로 재정렬 (알 수 없는 추가 키는 뒤에 보존)
    ordered = {k: e[k] for k in CANON_ORDER if k in e}
    for k, v in e.items():
        ordered.setdefault(k, v)
    return ordered


def bump_patch(v: str) -> str:
    parts = str(v).split(".")
    try:
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
    except ValueError:
        return v


def esc(text: str) -> str:
    return str(text).replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()


def render_table(plugins: list[dict]) -> str:
    rows = ["| 플러그인 | 버전 | 카테고리 | 설명 |", "|----------|:----:|:--------:|------|"]
    for p in plugins:
        name = p.get("name", "?")
        src = p.get("source", "").lstrip("./") or f"plugins/{name}"
        ver = p.get("version", "-")
        cat = p.get("category", "-")
        desc = esc(p.get("description", ""))
        rows.append(f"| [**{name}**]({src}) | `{ver}` | {cat} | {desc} |")
    return "\n".join(rows)


def sync_readme(plugins: list[dict]) -> bool:
    if not README_PATH.is_file():
        return False
    text = README_PATH.read_text(encoding="utf-8")
    if README_START not in text or README_END not in text:
        notes.append(
            f"README.md: 마커({README_START} / {README_END})가 없어 표 자동생성을 건너뜀"
        )
        return False
    table = render_table(plugins)
    new_block = f"{README_START}\n{table}\n{README_END}"
    new_text = re.sub(
        re.escape(README_START) + r".*?" + re.escape(README_END),
        lambda _m: new_block,
        text,
        flags=re.DOTALL,
    )
    if new_text != text:
        README_PATH.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    # Windows 콘솔(cp949)에서도 한글/기호 출력이 깨지거나 죽지 않도록 UTF-8 강제
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass

    check_only = "--check" in sys.argv[1:]

    mp = load_json(MP_PATH)
    if mp is None:
        print("FATAL: marketplace.json 을 읽을 수 없습니다.", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        return 1

    existing = mp.get("plugins", [])
    existing_by_name = {e.get("name"): e for e in existing}
    discovered = discover_plugins()
    discovered_by_name = {data["name"]: (dirname, data) for dirname, data in discovered.items()}

    if errors:
        print("검증 실패:", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        return 1

    # 기존 순서 유지 + 살아있는 것만, 그 뒤에 신규 append
    new_plugins: list[dict] = []
    seen: set[str] = set()
    for entry in existing:
        nm = entry.get("name")
        if nm in discovered_by_name:
            dirname, data = discovered_by_name[nm]
            new_plugins.append(build_entry(dirname, data, entry))
            seen.add(nm)
        else:
            notes.append(f"stale 항목 제거: {nm} (대응 폴더 없음)")
    for dirname in sorted(discovered.keys()):
        data = discovered[dirname]
        nm = data["name"]
        if nm not in seen:
            new_plugins.append(build_entry(dirname, data, None))
            seen.add(nm)
            notes.append(f"신규 플러그인 등록: {nm}")

    plugins_changed = existing != new_plugins
    mp["plugins"] = new_plugins
    if plugins_changed:
        old_v = mp.get("metadata", {}).get("version", "1.0.0")
        new_v = bump_patch(old_v)
        mp.setdefault("metadata", {})["version"] = new_v
        notes.append(f"marketplace version bump: {old_v} -> {new_v}")

    new_mp_text = json.dumps(mp, ensure_ascii=False, indent=2) + "\n"
    mp_will_change = new_mp_text != MP_PATH.read_text(encoding="utf-8")

    # README 표는 현재(또는 갱신될) plugins 기준으로 미리 렌더해 비교
    readme_will_change = False
    if README_PATH.is_file():
        cur = README_PATH.read_text(encoding="utf-8")
        if README_START in cur and README_END in cur:
            rendered = re.sub(
                re.escape(README_START) + r".*?" + re.escape(README_END),
                lambda _m: f"{README_START}\n{render_table(new_plugins)}\n{README_END}",
                cur,
                flags=re.DOTALL,
            )
            readme_will_change = rendered != cur

    if check_only:
        print("[OK] 검증 통과 (--check): JSON 유효, 모든 플러그인 name 존재")
        if mp_will_change or readme_will_change:
            print("[i] 동기화 대기 중인 변경이 있습니다 (push 시 자동 반영):")
            for n in notes:
                print("  - " + n)
            if mp_will_change:
                print("  - marketplace.json 갱신 예정")
            if readme_will_change:
                print("  - README 플러그인 표 갱신 예정")
        return 0

    wrote = []
    if mp_will_change:
        MP_PATH.write_text(new_mp_text, encoding="utf-8")
        wrote.append("marketplace.json")
    if sync_readme(new_plugins):
        wrote.append("README.md")

    for n in notes:
        print("- " + n)
    if wrote:
        print("갱신됨: " + ", ".join(wrote))
    else:
        print("이미 동기화 상태, 변경 없음.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
