# doc-governance

> 项目文档全生命周期治理规范 — 约定项目文件夹下文档的开发、变更、编写、删除行为，确保文档有序、可追溯、可索引。

## 功能特性

| 模块 | 说明 |
|------|------|
| 编号排序 | 文件夹和业务文档统一 `NN_` 前缀编号，行业规范文件例外 |
| 版本管理 | 文件名格式 `名称-V主.次-YYMMDD.ext`，版本+日期双标识 |
| 变更留痕 | 禁止原地修改，新建版本迭代；维护版本日志（新增/变更/删除 + 修改时间） |
| 分类归档 | 同类文件归入编号文件夹，根目录保持干净 |
| 根目录索引 | `00_索引.md` 列出所有文档最新版清单 |
| AGENTS.md 同步 | 检查项目规范文件是否包含文档治理约定，提示用户更新 |
| 项目版本 | 遵循 SemVer 规则（MAJOR.MINOR.PATCH），配套 CHANGELOG |

## 目录结构

```
doc-governance/
├── SKILL.md                          # 技能主文件（核心规范与工作流程）
├── README.md                         # 项目说明
├── CHANGELOG.md                      # 变更日志（内部维护，不发布）
├── 00_项目版本管理.md                # 项目版本演进记录（内部维护，不发布）
├── .gitignore                        # Git 忽略规则
├── scripts/                          # 运行时脚本（随技能发布）
│   ├── validate_project.py           # 校验项目文档规范符合度
│   ├── generate_index.py            # 扫描生成/更新根目录索引
│   └── create_version.py             # 基于最新版创建新版本文件
├── assets/                           # 模板资源（随技能发布）
│   └── templates/
│       ├── version-log-template.md    # 版本日志模板
│       ├── index-template.md          # 索引模板
│       └── changelog-template.md      # CHANGELOG 模板
├── dev/                              # 开发工具（不发布）
│   └── package_release.py            # 打包发布脚本
└── output/                           # 打包输出（Git 忽略）
    └── doc-governance-vX.Y.Z.zip
```

## 安装方式

将整个 `doc-governance` 文件夹复制到技能目录即可自动加载：

```
~/.doubao/agent_mode/workspace/.user_skills/doc-governance/
```

## 脚本工具

### validate_project.py — 规范校验

```bash
python scripts/validate_project.py <项目根目录>
```

扫描项目目录，检查命名规范、版本号格式、缺失的版本日志、索引是否过期、AGENTS.md 同步状态等。

### generate_index.py — 生成索引

```bash
python scripts/generate_index.py <项目根目录>
```

自动识别所有符合命名规范的文档，按文档分组取最新版本，生成/更新根目录 `00_索引.md`。

### create_version.py — 创建新版本

```bash
python scripts/create_version.py <源文件路径> [--minor|--major]
```

基于最新版文件复制生成新版本文件，自动递增版本号并填充当天日期。默认次版本号 +0.1，加 `--major` 升主版本号。

## 命名规范速查

```
文件夹：    01_需求文档/  02_设计文档/  03_会议纪要/
业务文档：  01_需求说明书-V1.0-261012.md
特殊文件：  00_索引.md  00_项目版本管理.md  00_需求文档-版本管理.md
例外文件：  AGENTS.md  README.md  CHANGELOG.md（不加编号）
```

## 版本

当前版本：**v0.1.0**（2026-10-12）

详见 [CHANGELOG.md](CHANGELOG.md)。
