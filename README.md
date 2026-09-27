# projseed

> 零运行时依赖的 Python CLI，一条命令为新项目补齐 `.gitignore`、`LICENSE`、`README`、`.editorconfig`、`CONTRIBUTING`、`CHANGELOG` 与 Issue / PR 模板。

**Language / 語言:**
[简体中文](#简体中文) · [繁體中文](#繁體中文) · [English](#english)

---

## 简体中文

### 🎉 项目介绍

每次新开一个仓库，你都要复制粘贴一堆模板文件：`.gitignore` 抄一半、`LICENSE` 忘了填版权人、`CHANGELOG` 忘记按 Keep a Changelog 格式写、Issue 模板每次重新发明轮子。**projseed** 把这些"每个仓库都要有、但没人想手写"的元文件收拢成一个零依赖的命令行工具。

它的灵感来自 gitignore.io、github/gitignore、choosealicense.com 与 cookiecutter 这一类工具的通用产品思路，但**模板文案与代码全部独立自研**：

- **离线可用**：不联网、不调用任何 API、不读远程模板。
- **零运行时依赖**：只用到 Python 标准库，`pipx` 装完即走。
- **生态预设合并**：选 `python node go` 三个标签，`.gitignore` 自动去重合并，不覆盖你已写的规则，还正确处理 `!` 取反。
- **`detect` 子命令**：扫描当前目录的技术栈，告诉你还缺哪些元文件。

### ✨ 核心特性

- 🪶 **零运行时依赖**：纯标准库，Python 3.9+ 即可，安装体积不到 50 KB。
- 🔌 **完全离线**：所有模板内置在包里，不依赖网络、不调用 LLM。
- 🧩 **多生态预设**：`general / python / node / go / rust / java / docker` 七套 `.gitignore` 片段，任意组合。
- 🧮 **智能合并 .gitignore**：自动去重、保留你已有规则、识别 `!` 取反、重复运行不会产生重复段落。
- 📜 **四种 LICENSE 一键生成**：`mit` / `isc` / `bsd-2` / `apache-2.0`，自动填入版权人与年份。
- 🕵️ **`detect` 子命令**：自动探测当前目录技术栈并报告缺失的元文件。
- 🧯 **幂等写入**：已存在的文件默认跳过，加 `--force` 才覆盖；`.gitignore` 采用合并而非覆盖策略。
- 💬 **交互 / 非交互双模式**：TTY 下会提问，CI 里用 `--non-interactive` 一把过。
- ✅ **unittest 全覆盖**：35 个用例覆盖合并逻辑、探测逻辑与全部子命令。

### 🚀 快速开始

**环境要求**：Python 3.9 或更高版本，无需任何第三方依赖。

**安装（任选其一）**：

```sh
# 方式一：pipx（推荐，隔离环境）
pipx install .

# 方式二：pip 直接装
pip install .

# 方式三：不安装，直接跑
python -m projseed --help
```

**30 秒生成一个新项目骨架**：

```sh
mkdir my-awesome-app && cd my-awesome-app
projseed init python --license mit --holder "Your Name" --year 2026 --project my-awesome-app --non-interactive
```

执行完你会得到：

```
.gitignore
LICENSE
README.md
.editorconfig
CONTRIBUTING.md
CHANGELOG.md
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
PULL_REQUEST_TEMPLATE.md
```

### 📖 详细使用指南

#### 一次性生成全部元文件

```sh
projseed init [ECOSYSTEMS...] [--license mit|isc|bsd-2|apache-2.0]
              [--holder NAME] [--year YEAR] [--project NAME]
              [--out-dir DIR] [--force] [--dry-run] [--non-interactive]
```

示例：同时为 Python + Node + Go 项目生成骨架：

```sh
projseed init python node go --license apache-2.0 --holder "Acme Corp"
```

#### 单独追加 .gitignore 片段

```sh
projseed add rust java
```

这条命令会把 Rust 与 Java 的常用忽略规则**合并**进现有 `.gitignore`，已存在的规则自动跳过，不会覆盖你手写的内容。

#### 单独写 LICENSE

```sh
projseed license mit          # 或 isc / bsd-2 / apache-2.0
```

版权人默认取 `git config user.name`，年份默认取当前年份。

#### 单独写其他元文件

```sh
projseed readme          # README.md 骨架
projseed editorconfig    # .editorconfig
projseed contributing    # CONTRIBUTING.md
projseed changelog       # CHANGELOG.md（Keep a Changelog 格式）
projseed issue-templates # .github/ISSUE_TEMPLATE/* + PULL_REQUEST_TEMPLATE.md
```

所有子命令都支持 `--out-dir`、`--force`、`--dry-run`、`--holder`、`--year`、`--project`。

#### 探测当前目录缺什么

```sh
projseed detect
```

输出示例：

```
project root: /path/to/your/repo
detected ecosystems: python, node
missing meta files:
  - LICENSE   (run: projseed license mit)
  - CHANGELOG.md   (run: projseed changelog)
```

退出码：缺文件时返回 `1`，全部齐全返回 `0`，方便接到 CI 里。

#### 幂等行为

- 已存在的文件默认**跳过**，不会动你的手写内容。
- 加 `--force` 才会覆盖。
- `.gitignore` 是例外：它走合并逻辑，重复运行只会追加真正缺失的规则，不会产生重复段落。

### 💡 设计思路与迭代规划

**为什么不直接用 cookiecutter？** cookiecutter 适合"整套项目模板"，但很多时候你只是想给一个已经存在的仓库补几个元文件。projseed 走的是"小而美"路线：不生成代码、不假设你的目录结构，只处理那 9 个每个仓库都该有的文件。

**技术选型**：刻意只用标准库。理由是这类工具的用户最在意的是"装完就能跑、不会被依赖锁死"。`argparse` 足够写这种多子命令 CLI，`pathlib` 处理路径，`unittest` 自带测试框架，零成本。

**后续迭代方向**：

- 支持更多 LICENSE（GPL-3.0、MPL-2.0）。
- 支持更多生态预设（php / ruby / dotnet / swift）。
- 增加 `projseed lint` 子命令，检查现有元文件是否过时。
- 可选输出到 `stdout`，方便管道使用。

### 📦 打包与部署指南

projseed 是一个纯 Python 包，没有二进制、没有原生扩展。

```sh
# 本地构建（需要 build 包）
python -m pip install build
python -m build

# 产物在 dist/ 下，可上传到 PyPI
```

日常使用不需要构建，`pipx install .` 或 `pip install .` 即可。兼容 Windows / macOS / Linux 上任意支持 Python 3.9+ 的环境。

### 🤝 贡献指南

欢迎 Issue 与 PR！请先阅读 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。要点：

- 提交信息遵循 Conventional Commits：`feat:` / `fix:` / `docs:` / `refactor:`。
- 跑通 `python -m unittest -v` 再提交。
- **不要引入第三方运行时依赖**——这是 projseed 的核心承诺。

### 📄 开源协议说明

本项目基于 [MIT License](./LICENSE) 开源，版权所有 © 2026 gitstq。你可以自由使用、修改、分发，只需保留版权声明。

---

## 繁體中文

### 🎉 專案介紹

每次開新儲存庫，你都得複製貼上一堆範本檔：`.gitignore` 抄一半、`LICENSE` 忘了填版權人、`CHANGELOG` 沒照 Keep a Changelog 格式寫、Issue 範本每次重新發明輪子。**projseed** 把這些「每個 repo 都該有、但沒人想手寫」的中繼檔收斂成一個零相依的指令列工具。

靈感來自 gitignore.io、github/gitignore、choosealicense.com 與 cookiecutter 這類工具的通用產品邏輯，但**範本文案與程式碼全部獨立自研**：

- **離線可用**：不聯網、不呼叫任何 API、不抓遠端範本。
- **零執行期相依**：只用 Python 標準函式庫，`pipx` 裝完就走。
- **生態系預設合併**：選 `python node go` 三個標籤，`.gitignore` 自動去重合併，不覆寫你已寫的規則，還正確處理 `!` 反向排除。
- **`detect` 子指令**：掃描目前目錄的技術堆疊，告訴你還缺哪些中繼檔。

### ✨ 核心特性

- 🪶 **零執行期相依**：純標準函式庫，Python 3.9+ 即可，安裝體積不到 50 KB。
- 🔌 **完全離線**：所有範本內建在套件中，不靠網路、不叫 LLM。
- 🧩 **多生態系預設**：`general / python / node / go / rust / java / docker` 七組 `.gitignore` 片段，任意組合。
- 🧮 **智慧合併 .gitignore**：自動去重、保留你既有規則、辨識 `!` 反向排除、重複執行不會產生重複段落。
- 📜 **四種 LICENSE 一鍵生成**：`mit` / `isc` / `bsd-2` / `apache-2.0`，自動帶入版權人與年份。
- 🕵️ **`detect` 子指令**：自動偵測目前目錄技術堆疊並回報缺漏的中繼檔。
- 🧯 **冪等寫入**：已存在的檔案預設跳過，加 `--force` 才覆寫；`.gitignore` 採合併而非覆寫策略。
- 💬 **互動 / 非互動雙模式**：TTY 下會提問，CI 裡用 `--non-interactive` 一次到位。
- ✅ **unittest 全覆蓋**：35 個測試案例涵蓋合併邏輯、偵測邏輯與全部子指令。

### 🚀 快速開始

**環境需求**：Python 3.9 或更新版本，完全不需要第三方相依套件。

**安裝（擇一即可）**：

```sh
# 方法一：pipx（推薦，隔離環境）
pipx install .

# 方法二：直接 pip 安裝
pip install .

# 方法三：不安裝，直接執行
python -m projseed --help
```

**30 秒產生新專案骨架**：

```sh
mkdir my-awesome-app && cd my-awesome-app
projseed init python --license mit --holder "Your Name" --year 2026 --project my-awesome-app --non-interactive
```

執行完你會得到：

```
.gitignore
LICENSE
README.md
.editorconfig
CONTRIBUTING.md
CHANGELOG.md
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
PULL_REQUEST_TEMPLATE.md
```

### 📖 詳細使用指南

#### 一次生成全部中繼檔

```sh
projseed init [ECOSYSTEMS...] [--license mit|isc|bsd-2|apache-2.0]
              [--holder NAME] [--year YEAR] [--project NAME]
              [--out-dir DIR] [--force] [--dry-run] [--non-interactive]
```

範例：同時為 Python + Node + Go 專案生成骨架：

```sh
projseed init python node go --license apache-2.0 --holder "Acme Corp"
```

#### 單獨追加 .gitignore 片段

```sh
projseed add rust java
```

這條指令會把 Rust 與 Java 的常用忽略規則**合併**進現有 `.gitignore`，已存在的規則自動跳過，不會覆寫你手寫的內容。

#### 單獨寫 LICENSE

```sh
projseed license mit          # 或 isc / bsd-2 / apache-2.0
```

版權人預設帶入 `git config user.name`，年份預設帶入當年度。

#### 單獨寫其他中繼檔

```sh
projseed readme          # README.md 骨架
projseed editorconfig    # .editorconfig
projseed contributing    # CONTRIBUTING.md
projseed changelog       # CHANGELOG.md（Keep a Changelog 格式）
projseed issue-templates # .github/ISSUE_TEMPLATE/* + PULL_REQUEST_TEMPLATE.md
```

所有子指令都支援 `--out-dir`、`--force`、`--dry-run`、`--holder`、`--year`、`--project`。

#### 偵測目前目錄缺什麼

```sh
projseed detect
```

輸出範例：

```
project root: /path/to/your/repo
detected ecosystems: python, node
missing meta files:
  - LICENSE   (run: projseed license mit)
  - CHANGELOG.md   (run: projseed changelog)
```

結束代碼：缺檔案時回傳 `1`，全部齊全回傳 `0`，方便接到 CI 裡。

#### 冪等行為

- 已存在的檔案預設**跳過**，不動你手寫的內容。
- 加 `--force` 才會覆寫。
- `.gitignore` 是例外：它走合併邏輯，重複執行只會追加真正缺漏的規則，不會產生重複段落。

### 💡 設計理念與迭代規劃

**為什麼不直接用 cookiecutter？** cookiecutter 適合「整套專案範本」，但很多時候你只是想幫一個已經存在的 repo 補幾個中繼檔。projseed 走的是「小而美」路線：不生成程式碼、不假設你的目錄結構，只處理那 9 個每個 repo 都該有的檔案。

**技術選擇**：刻意只用標準函式庫。理由是這類工具的使用者最在意的是「裝完就能跑、不會被相依鎖死」。`argparse` 寫這種多子指令 CLI 綽綽有餘，`pathlib` 處理路徑，`unittest` 內建測試框架，零成本。

**後續迭代方向**：

- 支援更多 LICENSE（GPL-3.0、MPL-2.0）。
- 支援更多生態系預設（php / ruby / dotnet / swift）。
- 新增 `projseed lint` 子指令，檢查現有中繼檔是否過時。
- 可選輸出到 `stdout`，方便接管線。

### 📦 打包與部署指南

projseed 是純 Python 套件，沒有二進位檔、沒有原生擴充。

```sh
# 本機建置（需要 build 套件）
python -m pip install build
python -m build

# 產物在 dist/ 下，可上傳到 PyPI
```

一般使用不需要建置，`pipx install .` 或 `pip install .` 即可。相容 Windows / macOS / Linux 上任何支援 Python 3.9+ 的環境。

### 🤝 貢獻指南

歡迎 Issue 與 PR！請先閱讀 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。重點：

- 提交訊息遵循 Conventional Commits：`feat:` / `fix:` / `docs:` / `refactor:`。
- 送出前跑通 `python -m unittest -v`。
- **不要引入第三方執行期相依**——這是 projseed 的核心承諾。

### 📄 開源協議說明

本專案基於 [MIT License](./LICENSE) 開源，版權所有 © 2026 gitstq。你可以自由使用、修改、散布，只需保留版權聲明。

---

## English

### 🎉 Project Introduction

Every time you start a new repository, you end up copy-pasting a pile of template files: half a `.gitignore`, a `LICENSE` with the copyright holder left blank, a `CHANGELOG` that doesn't follow Keep a Changelog, and an issue template you reinvent from scratch. **projseed** collects all these "every-repo-should-have-it-but-nobody-wants-to-write-it" meta files into a zero-dependency CLI.

It is inspired by the general product ideas behind gitignore.io, github/gitignore, choosealicense.com, and cookiecutter — but **all template text and code are written from scratch**:

- **Works fully offline**: no network, no API calls, no remote template fetch.
- **Zero runtime dependencies**: Python standard library only. Installs and runs in one shot.
- **Ecosystem presets merged**: pick `python node go` and your `.gitignore` is merged and deduped without clobbering your existing rules, with proper `!` negation handling.
- **`detect` subcommand**: scans the current directory's tech stack and tells you which meta files are missing.

### ✨ Key Features

- 🪶 **Zero runtime dependencies**: pure stdlib, Python 3.9+, installs in under 50 KB.
- 🔌 **Fully offline**: all templates ship inside the package; no network, no LLM calls.
- 🧩 **Multi-ecosystem presets**: `general / python / node / go / rust / java / docker` — combine any way you like.
- 🧮 **Smart .gitignore merging**: auto-dedupe, preserves your existing rules, honors `!` negation, never produces duplicate sections on re-run.
- 📜 **Four licenses one command away**: `mit` / `isc` / `bsd-2` / `apache-2.0`, with the copyright holder and year auto-filled.
- 🕵️ **`detect` subcommand**: auto-detects the current directory's stack and reports missing meta files.
- 🧯 **Idempotent writes**: existing files are skipped by default; `--force` overwrites. `.gitignore` is merged, never blown away.
- 💬 **Interactive / non-interactive**: prompts on a TTY; pass `--non-interactive` for CI.
- ✅ **unittest coverage**: 35 tests covering merge logic, detection, and every subcommand.

### 🚀 Quick Start

**Requirements**: Python 3.9 or newer. No third-party packages required.

**Install (pick one)**:

```sh
# Option 1: pipx (recommended, isolated env)
pipx install .

# Option 2: plain pip
pip install .

# Option 3: run without installing
python -m projseed --help
```

**Scaffold a new project in 30 seconds**:

```sh
mkdir my-awesome-app && cd my-awesome-app
projseed init python --license mit --holder "Your Name" --year 2026 --project my-awesome-app --non-interactive
```

You get:

```
.gitignore
LICENSE
README.md
.editorconfig
CONTRIBUTING.md
CHANGELOG.md
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
PULL_REQUEST_TEMPLATE.md
```

### 📖 Usage Guide

#### Generate everything at once

```sh
projseed init [ECOSYSTEMS...] [--license mit|isc|bsd-2|apache-2.0]
              [--holder NAME] [--year YEAR] [--project NAME]
              [--out-dir DIR] [--force] [--dry-run] [--non-interactive]
```

Example: scaffold for a Python + Node + Go project:

```sh
projseed init python node go --license apache-2.0 --holder "Acme Corp"
```

#### Append .gitignore snippets

```sh
projseed add rust java
```

This **merges** common Rust and Java ignore rules into your existing `.gitignore`. Rules already present are skipped; your hand-written lines are never overwritten.

#### Write a single LICENSE

```sh
projseed license mit          # or isc / bsd-2 / apache-2.0
```

The holder defaults to `git config user.name`; the year defaults to the current year.

#### Write other meta files individually

```sh
projseed readme          # README.md skeleton
projseed editorconfig    # .editorconfig
projseed contributing    # CONTRIBUTING.md
projseed changelog       # CHANGELOG.md (Keep a Changelog format)
projseed issue-templates # .github/ISSUE_TEMPLATE/* + PULL_REQUEST_TEMPLATE.md
```

Every subcommand accepts `--out-dir`, `--force`, `--dry-run`, `--holder`, `--year`, `--project`.

#### Detect what's missing

```sh
projseed detect
```

Sample output:

```
project root: /path/to/your/repo
detected ecosystems: python, node
missing meta files:
  - LICENSE   (run: projseed license mit)
  - CHANGELOG.md   (run: projseed changelog)
```

Exit code is `1` when files are missing and `0` when everything is present, so you can wire it into CI.

#### Idempotency

- Existing files are **skipped** by default; your hand-written content is untouched.
- Pass `--force` to overwrite.
- `.gitignore` is the exception: it uses merge semantics. Re-running only appends genuinely missing rules and never creates duplicate sections.

### 💡 Design Notes & Roadmap

**Why not just use cookiecutter?** cookiecutter is great for "whole project templates", but most of the time you just want to patch a few meta files into an existing repo. projseed takes the "small and sharp" route: it generates no code, assumes no directory layout, and only handles the nine files every repo should have.

**Tech choices**: we deliberately stick to the standard library. Users of this kind of tool care most about "installs and runs, no dependency hell". `argparse` is enough for a multi-subcommand CLI, `pathlib` handles paths, `unittest` is built in — zero cost.

**Roadmap**:

- More licenses (GPL-3.0, MPL-2.0).
- More ecosystem presets (php / ruby / dotnet / swift).
- A `projseed lint` subcommand to flag stale meta files.
- Optional stdout output for piping.

### 📦 Packaging & Deployment

projseed is a pure Python package: no binaries, no native extensions.

```sh
# Build a distribution locally (requires the build package)
python -m pip install build
python -m build

# Artifacts land in dist/ and can be uploaded to PyPI.
```

Day-to-day use needs no build step — `pipx install .` or `pip install .` is enough. It runs anywhere Python 3.9+ runs: Windows, macOS, Linux.

### 🤝 Contributing

Issues and PRs welcome! Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) first. Highlights:

- Commit messages follow Conventional Commits: `feat:` / `fix:` / `docs:` / `refactor:`.
- Make sure `python -m unittest -v` passes before opening a PR.
- **Do not add third-party runtime dependencies** — that is projseed's core promise.

### 📄 License

Released under the [MIT License](./LICENSE). Copyright © 2026 gitstq. Free to use, modify, and distribute as long as the copyright notice is retained.
