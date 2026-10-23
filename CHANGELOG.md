# Changelog

本项目所有重要变更均记录于此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### Added
- 

### Changed
- 

### Fixed
- 

### Removed
- 

---

## [0.1.3] - 2026-10-23

### Added
- 分类归档新增"多格式文件归档"规范：同一文档存在多种格式时（如 PDF 源文件 + 解析的 MD + 转出的 DOCX），为该文档建立独立子文件夹，内部按格式分子目录归档
- 新增工作流程"格式转换与多格式归档"，明确 `_source`（源文件）、`_md`、`_docx` 等格式子目录的命名与归位规则
- 明确多格式文件的命名一致性（相同编号/名称/版本号/日期戳，仅扩展名不同）与版本同步要求

---

## [0.1.2] - 2026-10-16

### Fixed
- 明确编号为"文件夹内独立编号"，修复文档归档到新文件夹时出现双重编号（如 `01_03_test.txt`）的问题
- 归档/移动文档时应按目标文件夹内顺序重新编号，并在版本日志"变更"维度记录更名信息

### Added
- validate_project.py 新增双重编号检测
- SKILL.md 新增"归档/移动文档"工作流程
- 版本日志模板补充更名记录示例

---

## [0.1.1] - 2026-10-12

### Fixed
- 移除 skill 对用户项目中 `00_项目版本管理.md` 和 `CHANGELOG.md` 的要求，这两个文件为 skill 项目自身工程文件，不属于用户使用范围

### Removed
- 规则7"项目自身版本与 CHANGELOG"从核心规范中移除
- `changelog-template.md` 模板从发布包中移除
- validate_project.py 不再检查 CHANGELOG.md 是否存在

---

## [0.1.0] - 2026-10-12

### Added
- 初始版本发布
- 文档编号排序规范（NN_ 前缀，行业规范文件例外）
- 文档版本号与日期戳规则（V主.次-YYMMDD）
- 变更留痕机制（禁止原地修改，版本日志含修改时间）
- 分类归档规则
- 根目录索引机制（00_索引.md）
- AGENTS.md 同步检查流程
- 项目级 SemVer 版本管理与 CHANGELOG
- 三个脚本工具：validate_project.py、generate_index.py、create_version.py
- 三个模板：版本日志、索引、CHANGELOG

---

<!-- 分类说明：
### Added     新增的功能或文档
### Changed   对已有功能或文档的变更
### Fixed     问题修复
### Removed   移除的功能或文档
-->
