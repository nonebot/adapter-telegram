# Telegram Adapter 使用指南

本文默认你使用 `nb init` 创建了一个空的 bootstrap 项目。

## 安装适配器

```shell
nb adapter install nonebot-adapter-telegram
```

## 申请一个 Telegram 机器人

首先你需要有一个 Telegram 帐号，添加 [BotFather](https://t.me/botfather) 为好友。

接着，向它发送 `/newbot` 指令，按要求回答问题。

如果你成功创建了一个机器人，BotFather 会发给你机器人的 token：

```plain
1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI
```

将这个 token 填入 NoneBot 的 `env` 文件：

```dotenv
telegram_bots = [{"token": "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI"}]
```

> NOTE
>
> 如果你需要让你的 Bot 响应除了 `/` 开头之外的消息，你需要向 BotFather 发送 `/setprivacy` 并选择 `Disable`。
>
> 如果你需要让你的 Bot 接收 inline query，你还需要向 BotFather 发送 `/setinline`。

## 配置 NoneBot

### 配置驱动器

NoneBot 默认选择的驱动器为 FastAPI，它是一个服务端类型驱动器（ReverseDriver），而 Telegram 适配器至少需要一个客户端类型驱动器（ForwardDriver），所以你需要额外安装其他驱动器。

HTTPX 是推荐的客户端类型驱动器，你可以使用 nb-cli 进行安装。

```shell
nb driver install httpx
```

别忘了在环境文件中写入配置：

```dotenv
driver=~fastapi+~httpx
```

### 使用代理

如果运行 NoneBot 的服务器位于中国大陆，那么你可能需要配置代理，否则将无法调用 Telegram 提供的任何 API。

```dotenv
telegram_proxy = "http://127.0.0.1:10809"
```

> NOTE 如果你的代理使用 socks 协议，你需要安装 httpx\[socks\]。

### 使用 Long polling 获取事件（推荐）

只要不在 `env` 文件中设置 `url`，默认使用 long polling 模式。

### 使用 Webhook 获取事件（不推荐）

> NOTE 如果你坚持使用此方式获取更新，请确保自己掌握基本的服务器运维知识。

<details><summary>点击展开</summary>
<p>

Telegram Bot 的 webhook 必须使用 https 协议，所以你需要公网 IP、域名，以及 TLS 证书，并通过反向代理等方式使 NoneBot 能够接受到来自 Telegram 服务器的 webhook 消息。

要令 Telegram 适配器启用此模式，需要将域名填入 `env` 文件：

```dotenv
telegram_bots = [{"token": "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI", webhook_url: "https://yourdomain.com"}]
```

</p>
</details>

## 第一次对话

```python
import nonebot
from nonebot.adapters.telegram import Adapter as TelegramAdapter

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(TelegramAdapter)

nonebot.load_builtin_plugins("echo")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
```

现在，你可以私聊自己的 Telegram Bot `/echo hello world`，不出意外的话，它将回复你 `hello world`。

> NOTE 更多示例：<https://github.com/nonebot/adapter-telegram/blob/beta/example>

## FAQ（常见问题解答）

- 如何发图/回复/下载文件？  
  **看[示例](https://github.com/nonebot/adapter-telegram/blob/beta/example)**，示例里没有可以提 Issue。
- 日志里有一堆 NetworkError 怎么办？  
  请检查你的网络环境。
