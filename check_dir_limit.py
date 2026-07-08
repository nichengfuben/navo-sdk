from __future__ import annotations

"""目录直接子项数量合规检查（每层 ≤7，含豁免与运行时子项排除）。"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

MAX_CHILDREN = 7

EXEMPT_SUBTREE_PREFIXES: tuple[tuple[str, ...], ...] = (
    ("src", "platforms"),
    ("logs",),
    ("persist",),
    ("docs-src",),
    ("tests",),
    ("template",),
    ("tmp",),
)

RUNTIME_DIR_NAMES = frozenset({
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
})

RUNTIME_FILE_SUFFIXES = (".pyc", ".pyo")

EXEMPT_SUMMARY = (
    "项目根目录；src/platforms/、logs/、persist/、docs-src/、tests/、template/、tmp/ 整棵子树；"
    "任意层级以 . 开头的目录"
)

__all__ = [
    "MAX_CHILDREN",
    "EXEMPT_SUBTREE_PREFIXES",
    "RUNTIME_DIR_NAMES",
    "is_exempt_dir",
    "countable_children",
    "scan_violations",
    "format_report",
]


@dataclass(frozen=True)
class DirViolation:
    """单个违规目录记录。"""

    path: Path
    child_count: int
    children: tuple[str, ...]


def is_exempt_dir(root: Path, directory: Path) -> bool:
    """判断目录是否豁免 ≤7 检查。"""
    root_resolved = root.resolve()
    directory_resolved = directory.resolve()
    if directory_resolved == root_resolved:
        return True
    try:
        rel = directory_resolved.relative_to(root_resolved)
    except ValueError:
        return False
    parts = rel.parts
    if any(part.startswith(".") for part in parts):
        return True
    for prefix in EXEMPT_SUBTREE_PREFIXES:
        if len(parts) >= len(prefix) and parts[:len(prefix)] == prefix:
            return True
    return False


def countable_children(directory: Path) -> list[Path]:
    """返回计入直接子项数量的条目（排除运行时缓存目录与字节码文件）。"""
    children: list[Path] = []
    for item in directory.iterdir():
        if item.name in RUNTIME_DIR_NAMES:
            continue
        if item.is_file() and item.suffix in RUNTIME_FILE_SUFFIXES:
            continue
        children.append(item)
    return sorted(children, key=lambda entry: entry.name.lower())


def scan_violations(root: Path, *, max_children: int = MAX_CHILDREN) -> list[DirViolation]:
    """扫描 root 下受约束的子目录，返回直接子项超过 max_children 的目录列表。"""
    violations: list[DirViolation] = []
    for dirpath, _dirnames, _filenames in _walk_dirs(root):
        current = Path(dirpath)
        if is_exempt_dir(root, current):
            continue
        children = countable_children(current)
        if len(children) > max_children:
            violations.append(
                DirViolation(
                    path=current,
                    child_count=len(children),
                    children=tuple(item.name for item in children),
                )
            )
    violations.sort(key=lambda item: (-item.child_count, str(item.path).lower()))
    return violations


def _walk_dirs(root: Path):
    """深度优先遍历目录；豁免子树不再向下遍历。"""
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except OSError:
            continue
        dirs = [item for item in entries if item.is_dir()]
        yield str(current), [item.name for item in dirs], [item.name for item in entries if item.is_file()]
        for item in reversed(dirs):
            if is_exempt_dir(root, item):
                continue
            stack.append(item)


def format_report(
    root: Path,
    violations: list[DirViolation],
    *,
    max_children: int = MAX_CHILDREN,
) -> str:
    """生成可读检查报告。"""
    lines = [
        "目录直接子项合规检查",
        "根目录: {}".format(root.resolve()),
        "约束: 受检目录每层直接子项 ≤ {}".format(max_children),
        "豁免目录: {}".format(EXEMPT_SUMMARY),
        "不计入子项: {} 及 {}".format(
            ", ".join(sorted(RUNTIME_DIR_NAMES)),
            ", ".join(RUNTIME_FILE_SUFFIXES),
        ),
        "违规目录数: {}".format(len(violations)),
        "",
    ]
    if not violations:
        lines.append("全部合规。")
        return "\n".join(lines) + "\n"

    for item in violations:
        rel = item.path.resolve().relative_to(root.resolve())
        lines.append("{} ({} 项)".format(rel, item.child_count))
        for name in item.children:
            lines.append("  - {}".format(name))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(
        description="检查目录直接子项是否 ≤7（含豁免子树与运行时子项排除）",
    )
    parser.add_argument("path", nargs="?", default=".", help="检查根路径，默认项目根目录")
    parser.add_argument(
        "--max",
        type=int,
        default=MAX_CHILDREN,
        help="每层允许的最大直接子项数，默认 7",
    )
    parser.add_argument("--output", default="", help="报告输出路径，默认写入 logs/scriptgen")
    args = parser.parse_args()

    root = (PROJECT_ROOT / args.path).resolve() if not Path(args.path).is_absolute() else Path(args.path)
    if not root.is_dir():
        raise ValueError("指定路径不是目录: {}".format(root))

    violations = scan_violations(root, max_children=args.max)
    report = format_report(root, violations, max_children=args.max)

    output = Path(args.output) if args.output else PROJECT_ROOT / "logs" / "scriptgen" / "dir_limit.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(report, end="")

    if violations:
        print("发现 {} 个违规目录，详见 {}".format(len(violations), output), file=sys.stderr)
        return 1
    print("全部合规，报告已写入 {}".format(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
