#!/usr/bin/env python3
"""
打包 doc-governance 技能为 zip 发布包。

用法:
    python dev/package_release.py

输出:
    output/doc-governance-v{版本号}.zip
"""

import re
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / 'output'

VERSION_PATTERN = re.compile(r'## \[(\d+\.\d+\.\d+)\]')

EXCLUDE_DIRS = {'.git', '.github', '__pycache__', '.vscode', '.idea', 'node_modules', 'dist', 'build', 'output', 'dev'}
EXCLUDE_FILES = {'.DS_Store', 'Thumbs.db', '.gitignore', 'package_release.py', '00_项目版本管理.md', 'CHANGELOG.md'}
EXCLUDE_EXTENSIONS = {'.pyc', '.pyo', '.pyd', '.zip'}


def read_version() -> str:
    changelog = PROJECT_ROOT / 'CHANGELOG.md'
    if not changelog.exists():
        return '0.0.0'
    content = changelog.read_text(encoding='utf-8')
    for line in content.splitlines():
        m = VERSION_PATTERN.match(line.strip())
        if m:
            return m.group(1)
    return '0.0.0'


def should_exclude(filepath: Path, root: Path) -> bool:
    rel_path = filepath.relative_to(root)
    for part in rel_path.parts:
        if part in EXCLUDE_DIRS:
            return True
    if filepath.name in EXCLUDE_FILES:
        return True
    if filepath.suffix.lower() in EXCLUDE_EXTENSIONS:
        return True
    return False


def collect_files(root: Path) -> list:
    files = []
    for item in sorted(root.rglob('*')):
        if item.is_file() and not should_exclude(item, root):
            files.append(item)
    return files


def create_zip(version: str, files: list) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    zip_name = f'doc-governance-v{version}.zip'
    zip_path = OUTPUT_DIR / zip_name
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in files:
            arcname = Path('doc-governance') / file_path.relative_to(PROJECT_ROOT)
            zf.write(file_path, arcname)
    return zip_path


def main():
    version = read_version()
    print(f'📦 正在打包 doc-governance v{version} ...')
    print()
    files = collect_files(PROJECT_ROOT)
    if not files:
        print('❌ 没有找到需要打包的文件')
        return
    print(f'包含文件（{len(files)} 个）：')
    for f in files:
        rel = f.relative_to(PROJECT_ROOT)
        print(f'  + {rel}')
    print()
    zip_path = create_zip(version, files)
    size_kb = zip_path.stat().st_size / 1024
    print(f'✅ 打包完成：')
    print(f'   文件：{zip_path.name}')
    print(f'   大小：{size_kb:.1f} KB')
    print(f'   位置：{zip_path}')


if __name__ == '__main__':
    main()
