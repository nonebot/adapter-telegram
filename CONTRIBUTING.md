# NoneBot Adapter Telegram 贡献指南

首先，感谢你愿意为 NoneBot 社区贡献自己的一份力量！

本指南旨在引导你更规范地提交贡献，请务必认真阅读。

## 提交 Issue

在提交 Issue 前，我建议你先查看 [FAQ](./MANUAL.md#FAQ（常见问题解答）) 与[已有的 Issues](https://github.com/nonebot/adapter-telegram/issues)，以防重复提交。

### 报告问题、故障与漏洞

NoneBot Adapter Telegram 仍然是一个不够稳定的开发中项目，如果你在使用过程中发现问题并确信是由本项目引起的，欢迎提交 Issue。

### 建议功能

欢迎在 Issue 中提议要加入哪些**便于插件开发**的新功能，为了让开发者更好地理解你的意图，请认真描述你所需要的特性，可能的话可以提出你认为可行的解决方案。

## Pull Request

本项目使用 [pdm](https://pdm.fming.dev/) 管理项目依赖，由于 pre-commit 也经其管理，所以在此一并说明。

下面的命令能在已安装 pdm 的情况下帮你快速配置开发环境。

```bash
# 安装 python 依赖
pdm sync
# 安装 pre-commit git hook
pdm run pre-commit install
```

### 使用 GitHub Codespaces（Dev Container）

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=beta&repo=370031734)

### Commit 规范

请确保你的每一个 commit 都能清晰地描述其意图，一个 commit 尽量只有一个意图。

本项目的 commit message 格式遵循 [gitmoji](https://gitmoji.dev/) 规范，在创建 commit 时请牢记这一点。

或者使用 [nonemoji](https://github.com/nonebot/nonemoji) 代替 git 进行 commit，nonemoji 已默认作为项目开发依赖安装。

```bash
nonemoji commit [-e EMOJI] [-m MESSAGE] [-- ...]
```

### 工作流概述

请在 fork 本仓库后，向本仓库的 `beta` 分支发起 Pull Request，注意遵循先前提到的 commit message 规范创建 commit。我将在 code review 通过后通过 squash merge 方式将您的贡献合并到主分支。

### 撰写文档

以下是比较重要的排版规范。

1. 中文与英文、数字、半角符号之间需要有空格。例：`NoneBot2 是一个可扩展的 Python 异步机器人框架。`
2. 若非英文整句，使用全角标点符号。例：`现在你可以看到机器人回复你：“Hello, World !”。`
3. 直引号`「」`和弯引号`“”`都可接受，但同一份文件里应使用同种引号。
4. **不要使用斜体**，你不需要一种与粗体不同的强调。除此之外，你也可以考虑使用 GitHub 提供的[告示](https://github.com/community/community/discussions/16925)功能。

这是 NoneBot 社区创始人 richardchien 的中文排版规范，可供参考：<https://stdrc.cc/style-guides/chinese>。

如果你需要编辑器提示 Markdown 规范，可以安装 VSCode 上的 markdownlint 插件。

### 参与开发

本项目代码风格遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 与 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 规范，请确保你的代码风格和项目已有的代码保持一致，变量命名清晰，有适当的注释。

如果是适配 [Telegram Bot API](https://core.telegram.org/bots/api) 的更新，需遵守如下规范：commit 必须仅包含 `api.py` 和 `model.py` 的更改，并使用 :alien: 作为 commit message 的 intention，如 <https://github.com/nonebot/adapter-telegram/commit/b1a06fb2c3fb8a400013b77397aac4293747efba>。若还需要更改适配器内部逻辑以适配该更新，请在同一个 PR 的下一个 commit 包含该更改，并使用 :sparkles: 作为 commit message 的 intention。

如果你要给 `api.py`、`method.py`、`event.py` 添加 docstring，请使用**简体中文**，并注意不要写无用注释。

## 为社区做贡献

如果你开发了一个兼容 Telegram Adapter 的插件，在发布到 [NoneBot 商店](https://nonebot.dev/store)时可以添加 `a:Telegram` 的标签，以便于用户在 OneBot V11 插件的海洋里找到你。
