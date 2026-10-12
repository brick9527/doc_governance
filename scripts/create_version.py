#!/usr/bin/env python3
"""
基于最新版文档创建新版本文件。

用法:
    python create_version.py <源文件路径> [--minor|--major]

示例:
    python create_version.py "01_需求文档/01_需求说明书-V1.0-261012.md"
    python create_version.py "01_需求文档/01_需求说明书-V1.3-261101.md" --major
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# 文件名模式: NN_名称-VX.Y-YYMMDD.ext
FILENAME_PATTERN = re.compile(
    r'^(?P<prefix>\d{2}_)?(?P<name>.+?)[-\s]*V(?P<major>\d+)\.(?P<minor>\d+)-(?P<date>\d{6})\.(?P<ext>\w+)$'
)


def parse_filename(filepath: Path):
    """解析文件名，返回各组成部分。"""
    m = FILENAME_PATTERN.match(filepath.name)
    if not m:
        print(f"❌ 文件名不符合规范: {filepath.name}")
        print(f"   期望格式: NN_名称-VX.Y-YYMMDD.ext")
        print(f"   示例:     01_需求说明书-V1.0-261012.md")
        return None
    return m.groupdict()


def bump_version(parsed: dict, bump_type: str) -> tuple[int, int]:
    """递增版本号。"""
    major = int(parsed['major'])
    minor = int(parsed['minor'])
    if bump_type == 'major':
        return major + 1, 0
    else:
        return major, minor + 1


def main():
    parser = argparse.ArgumentParser(description='基于最新版文档创建新版本')
    parser.add_argument('source', help='源文件路径（最新版本）')
    parser.add_argument('--minor', action='store_const', const='minor', default='minor',
                        help='次版本号 +1（默认）')
    parser.add_argument('--major', action='store_const', const='major', dest='bump_type',
                        help='主版本号 +1，次版本归零')
    args = parser.parse_args()

    src = Path(args.source).resolve()
    if not src.exists():
        print(f"❌ 文件不存在: {src}")
        sys.exit(1)

    parsed = parse_filename(src)
    if not parsed:
        sys.exit(1)

    new_major, new_minor = bump_version(parsed, args.bump_type)
    today = datetime.now().strftime('%y%m%d')
    prefix = parsed['prefix'] or ''
    name = parsed['name']
    ext = parsed['ext']

    new_filename = f"{prefix}{name}-V{new_major}.{new_minor}-{today}.{ext}"
    new_path = src.parent / new_filename

    if new_path.exists():
        print(f"⚠️  目标文件已存在: {new_path}")
        sys.exit(1)

    shutil.copy2(src, new_path)
    print(f"✅ 已创建新版本:")
    print(f"   旧版本: {src.name}")
    print(f"   新版本: {new_filename}")
    print(f"   位置:   {new_path.parent}")
    print()
    print(f"下一步:")
    print(f"  1. 在新文件上进行编辑修改")
    print(f"  2. 更新对应分类的 00_xxx-版本管理.md")
    print(f"  3. 更新根目录 00_索引.md")


if __name__ == '__main__':
    main()
