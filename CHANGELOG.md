# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0-beta.10] - 2023-04-10

### 🚀 新功能

- 为回复消息的 MessageEvent 检测 to_me

## [0.1.0-beta.9] - 2023-03-19

### 🚀 新功能

- 为非私聊的 MessageEvent 检测 to_me
- 适配 Telegram Bot API 6.6

### 🐛 Bug 修复

修复 Message 处理时的 KeyError

## [0.1.0-beta.8] - 2023-02-10

### 💥 破坏性变更

- WebHook 模式下自动生成 secret_token ([#22](https://github.com/nonebot/adapter-telegram/issues/22))

### 🚀 新功能

- 新增更多 NoticeEvent
- 更好的 MessageSegment 显示

### 🐛 Bug 修复

- 修复上版本会在发送时删除 `File` 的问题

## [0.1.0-beta.7] - 2023-02-09

### 🚀 新功能

- 使用 NoneBot2 自带的 logger_wrapper

### 🐛 Bug 修复

- 修复上版本的 JSON 序列化错误

## [0.1.0-beta.6] - 2023-02-07

### 🚀 新功能

- 适配 Telegram Bot API 6.5
- 将 `reply_to_message` `pinned_message` 解析为 `MessageEvent`
- 使用真正的 Long Polling 获取事件

### 🐛 Bug 修复

- 为指定的 Method 而非全部 Method 检测文件

## [0.1.0-beta.5] - 2023-01-14

### 🚀 新功能

- 自动解析 call_api 的返回值，并支持位置参数
- 新增 `PRIVATE` `GROUP` 等 Permission
- 部分 MessageSegment 增加 `has_spoiler` 字段
- 新增 `InlineEvent` `PollEvent` `PollAnswerEvent` 等 Event

### 🐛 Bug 修复

- 修复许多错误字段
- 不再将所有 Excetion 视为 `NetworkException` 处理
- 修复部分 MessageSegment 的 data 错误

### 📝 文档

- 添加下载文件的示例

## [0.1.0-beta.4] - 2022-12-31

### 🚀 新功能

- 适配 Telegram Bot API 6.3
- 适配 Telegram Bot API 6.4
- 新增 `ForumTopicMessageEvent` `ForumTopicEditedMessageEvent`

### 📝 文档

- 更新使用指南

## [0.1.0-beta.3] - 2022-09-16

### 🚀 新功能

- 新增 `ChatJoinRequestEvent` [@lgc2333](https://github.com/lgc2333) ([#10](https://github.com/nonebot/adapter-telegram/pull/10))
- 适配 Telegram Bot API 6.1
- 适配 Telegram Bot API 6.2

### 🐛 Bug 修复

- 修复 `Audio` 的错误字段 [@lgc2333](https://github.com/lgc2333) ([#9](https://github.com/nonebot/adapter-telegram/pull/9))

### 📝 文档

- 添加回复消息和 Inline Mode 的示例

## [0.1.0-beta.2] - 2022-05-28

### 🚀 新功能

- photo 消息段的 file_id 现在指向分辨率最高的图片
- DEBUG 模式下打印较完整的事件描述
- 适配 Telegram Bot API 6.0

### 🐛 Bug 修复

- 修复带有 `<tag>` 的消息无法打印日志的问题

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

## [0.1.0-beta] - 2022-01-01

### 🚀 新功能

- 适配 NoneBot2 2.0.0b1
- 支持多个机器人同时在线

[Unreleased]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b10...HEAD
[0.1.0-beta.10]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b9...v0.1.0b10
[0.1.0-beta.9]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b8...v0.1.09b
[0.1.0-beta.8]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b7...v0.1.0b8
[0.1.0-beta.7]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b6...v0.1.0b7
[0.1.0-beta.6]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b5...v0.1.0b6
[0.1.0-beta.5]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b4...v0.1.0b5
[0.1.0-beta.4]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b3...v0.1.0b4
[0.1.0-beta.3]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b2...v0.1.0b3
[0.1.0-beta.2]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b1...v0.1.0b2
[0.1.0-beta.1]: https://github.com/nonebot/adapter-telegram/compare/v0.1.0b0...v0.1.0b1
[0.1.0-beta]: https://github.com/nonebot/adapter-telegram/releases/tag/v0.1.0b0
