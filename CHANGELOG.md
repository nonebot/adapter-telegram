# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🚀 新功能

- photo 消息段的 file_id 现在指向分辨率最高的图片
- DEBUG 模式下打印较完整的事件描述

## [0.1.0-beta.1] - 2022-03-15

### 🚀 新功能

- 适配 NoneBot2 2.0.0b2
- 适配 Telegram Bot API 5.7
- 提供 telegram_model 字段
- 使用类似 OneBot 的消息段
- 缩短事件在日志中的描述

### 🐛 Bug 修复

- 修复 Bot 方法中的可选参数
- 修复 MessageSegment 中的 bytes 类型注解
- 修复使用 bytes 无法发送文件的问题
- 修复 pydantic Model 的 JSON 序列化
- 修复 Model 中的可选字段

### 📝 文档

- 添加发送图片的示例

### 💫 杂项

- 不再使用 nb-cli 作为开发依赖以防依赖冲突
- 使用 pre-commit 在提交前自动格式化代码

## [0.1.0-beta] - 2022-01-01

### 🚀 新功能

- 适配 NoneBot2 2.0.0b1
- 支持多个机器人同时在线

[Unreleased]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b1...HEAD
[0.1.0-beta.1]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b0...v0.1.0b1
[0.1.0-beta]: https://github.com/nonebot/adapter-telegram/releases/tag/v0.1.0b0
