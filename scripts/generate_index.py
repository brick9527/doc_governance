#!/usr/bin/env python3
"""
扫描项目目录，生成/更新根目录的 00_索引.md。

用法:
    python generate_index.py <项目根目录>

说明:
    - 自动识别所有符合命名规范的文档（含 VX.Y-YYMMDD 模式）
    - 同一文档的多个版本只展示最新一版
    - 排除特殊文件（版本管理日志、索引自身、AGENTS.md、CHANGELOG 等）
"""

import re
import sys
from datetime import datetime
from pathlib import Path

# 文件名模式: 可选NN_前缀 + 名称 + -VX.Y-YYMMDD.ext
DOC_PATTERN = re.compile(
    r'^(?P<prefix>\d{2}_)?(?P<name>.+?)[-\s]*V(?P<major>\d+)\.(?P<minor>\d+)-(?P<date>\d{6})\.(?P<ext>\w+)$'
)

# 排除的特殊文件（不纳入索引）
EXCLUDE_NAMES = {
    '00_索引.md',
    '00_项目版本管理.md',
    'AGENTS.md',
    'CHANGELOG.md',
    'README.md',
}
EXCLUDE_SUFFIX = '-版本管理.md'
EXCLUDE_DIRS = {'.git', '.svn', '__pycache__', 'node_modules', '.idea', '.vscode'}


def is_excluded(filepath: Path) -> bool:
    """判断文件是否应排除出索引。"""
    name = filepath.name
    if name in EXCLUDE_NAMES:
        return True
    if name.endswith(EXCLUDE_SUFFIX):
        return True
    if filepath.name.startswith('.'):
        return True
    return False


def parse_doc(filepath: Path):
    """解析文档文件，返回结构化信息或 None。"""
    m = DOC_PATTERN.match(filepath.name)
    if not m:
        return None
    return {
        'name': m.group('name'),
        'major': int(m.group('major')),
        'minor': int(m.group('minor')),
        'date': m.group('date'),
        'ext': m.group('ext'),
        'full_path': filepath,
        'version': f"V{m.group('major')}.{m.group('minor')}",
    }


def collect_docs(project_root: Path) -> list:
    """收集项目下所有文档，按名称分组取最新版。"""
    docs_by_name: dict[str, dict] = {}

    for dirpath, dirnames, filenames in os_walk(project_root):
        # 过滤排除目录
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]

        for filename in filenames:
            if filename.startswith('.'):
                continue
            filepath = Path(dirpath) / filename
            if is_excluded(filepath):
                continue
            parsed = parse_doc(filepath)
            if not parsed:
                continue

            key = parsed['name']
            existing = docs_by_name.get(key)
            if existing is None or is_newer(parsed, existing):
                docs_by_name[key] = parsed

    return sorted(docs_by_name.values(), key=lambda x: x['name'])


def os_walk(root: Path):
    """模拟 os.walk，但用 pathlib。"""
    for item in sorted(root.iterdir()):
        if item.is_dir():
            yield from os_walk(item)
        else:
            yield root, [], [item.name]


def is_newer(candidate: dict, current: dict) -> bool:
    """比较两个版本，candidate 是否更新。"""
    if candidate['major'] != current['major']:
        return candidate['major'] > current['major']
    if candidate['minor'] != current['minor']:
        return candidate['minor'] > current['minor']
    return candidate['date'] > current['date']


def format_date(date_str: str) -> str:
    """YYMMDD → YYYY-MM-DD。"""
    try:
        return f"20{date_str[:2]}-{date_str[2:4]}-{date_str[4:6]}"
    except (IndexError, ValueError):
        return date_str


def generate_index_md(docs: list, project_root: Path) -> str:
    """生成索引 Markdown 内容。"""
    lines = [
        '# 项目文档索引',
        '',
        '> 本文件列出项目内所有文档的最新版本清单。历史版本不重复展示。',
        f'> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}',
        '',
        '---',
        '',
        '| 序号 | 文件名 | 文件位置 | 版本号 | 更新日期 |',
        '|:---:|:---|:---|:---:|:---:|',
    ]

    for i, doc in enumerate(docs, 1):
        rel_path = doc['full_path'].relative_to(project_root).as_posix()
        lines.append(
            f"| {i} | {doc['name']} | `{rel_path}` | {doc['version']} | {format_date(doc['date'])} |"
        )

    lines.extend([
        '',
        '---',
        '',
        f'*共 {len(docs)} 份文档 · 最后生成：{datetime.now().strftime("%Y-%m-%d")}*',
    ])
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_index.py <项目根目录>")
        sys.exit(1)

    project_root = Path(sys.argv[1]).resolve()
    if not project_root.is_dir():
        print(f"❌ 目录不存在: {project_root}")
        sys.exit(1)

    docs = collect_docs(project_root)
    if not docs:
        print("⚠️  未找到符合命名规范的文档")
        sys.exit(0)

    index_md = generate_index_md(docs, project_root)
    index_path = project_root / '00_索引.md'
    index_path.write_text(index_md, encoding='utf-8')

    print(f"✅ 已生成索引: {index_path}")
    print(f"   共收录 {len(docs)} 份文档的最新版本")


if __name__ == '__main__':
    main()
