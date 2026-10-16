#!/usr/bin/env python3
"""
校验项目目录的文档治理规范符合度。

检查项:
    1. 文件是否有数字前缀编号
    2. 文档文件名是否包含版本号 VX.Y 和日期戳 YYMMDD
    3. 是否存在 00_索引.md
    4. 是否存在 AGENTS.md
    5. 各分类文件夹是否有版本管理日志
    6. 根目录是否散落未分类文件

用法:
    python validate_project.py <项目根目录>
"""

import re
import sys
from pathlib import Path

# 文档文件名模式
DOC_PATTERN = re.compile(
    r'^(?P<prefix>\d{2}_)?(?P<name>.+?)[-\s]*V(?P<major>\d+)\.(?P<minor>\d+)-(?P<date>\d{6})\.(?P<ext>\w+)$'
)

# 根目录允许的特殊文件
ROOT_ALLOWED_FILES = {
    '00_索引.md',
    'AGENTS.md',
    'README.md',
    '.gitignore',
}

EXCLUDE_DIRS = {'.git', '.svn', '__pycache__', 'node_modules', '.idea', '.vscode'}


def validate_project(root: Path):
    """执行全部校验，返回问题列表。"""
    issues: list[str] = []

    # 1. 检查根目录特殊文件
    index_file = root / '00_索引.md'
    if not index_file.exists():
        issues.append("⚠️  缺少根目录索引文件: 00_索引.md")

    agents_file = root / 'AGENTS.md'
    if not agents_file.exists():
        issues.append("⚠️  缺少 AGENTS.md（建议将文档治理规范写入）")
    else:
        # 简单检查是否包含相关关键词
        content = agents_file.read_text(encoding='utf-8', errors='ignore')
        has_version = '版本' in content or 'V1.0' in content
        has_index = '索引' in content
        if not has_version or not has_index:
            issues.append("💡  AGENTS.md 内容可能未包含文档治理规范，建议同步更新")

    # 2. 遍历所有文件检查命名
    for dirpath, dirnames, filenames in walk(root):
        # 过滤排除目录
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]

        rel_dir = Path(dirpath).relative_to(root)

        for filename in filenames:
            if filename.startswith('.'):
                continue

            filepath = Path(dirpath) / filename

            # 根目录文件检查
            if rel_dir == Path('.'):
                if filename not in ROOT_ALLOWED_FILES:
                    issues.append(f"📂  根目录散落文件: {filename}（建议归档到分类文件夹）")
                continue

            # 版本管理日志文件跳过格式检查
            if filename.endswith('-版本管理.md'):
                continue

            # 检查双重编号（如 01_03_xxx.md）
            if re.match(r'^\d{2}_\d{2}_', filename):
                issues.append(f"🔢  双重编号问题: {rel_dir / filename}")
                issues.append(f"    应去掉原编号，按当前文件夹内顺序重新编号")
                continue

            # 检查文档命名
            m = DOC_PATTERN.match(filename)
            if not m:
                # 非文档类文件（如代码、图片）跳过严格检查
                ext = filepath.suffix.lower()
                if ext in {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.css', '.html',
                           '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
                           '.json', '.yaml', '.yml', '.toml', '.xml',
                           '.gitignore', '.lock', '.log'}:
                    continue
                issues.append(f"📝  文件名不符合规范: {rel_dir / filename}")
                issues.append(f"    期望格式: NN_名称-VX.Y-YYMMDD.ext")

    # 3. 检查各分类文件夹是否有版本管理日志
    for item in sorted(root.iterdir()):
        if not item.is_dir():
            continue
        if item.name in EXCLUDE_DIRS or item.name.startswith('.'):
            continue
        # 检查文件夹内是否有文档文件
        has_docs = any(
            f.suffix.lower() in {'.md', '.docx', '.doc', '.txt', '.xlsx', '.pptx', '.pdf'}
            for f in item.rglob('*') if f.is_file()
        )
        if has_docs:
            log_files = list(item.glob('00_*-版本管理.md'))
            if not log_files:
                issues.append(f"📋  分类文件夹缺少版本管理日志: {item.name}/ （建议创建 00_{item.name}-版本管理.md）")

    return issues


def walk(root: Path):
    """模拟 os.walk。"""
    yield root, [d.name for d in root.iterdir() if d.is_dir()], [f.name for f in root.iterdir() if f.is_file()]
    for item in sorted(root.iterdir()):
        if item.is_dir() and item.name not in EXCLUDE_DIRS and not item.name.startswith('.'):
            yield from walk(item)


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_project.py <项目根目录>")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"❌ 目录不存在: {root}")
        sys.exit(1)

    print(f"🔍 正在校验项目: {root}")
    print()

    issues = validate_project(root)

    if not issues:
        print("✅ 项目文档规范检查通过！")
    else:
        print(f"发现 {len(issues)} 项建议/问题：")
        print()
        for issue in issues:
            print(f"  {issue}")

    print()
    print(f"共 {len(issues)} 项")


if __name__ == '__main__':
    main()
