# navo-sdk

[Navo IM](https://github.com/aijianai/NavoIM) 的 Python 客户端 SDK。

本仓库是 [NavoIM](https://github.com/aijianai/NavoIM) 即时通讯平台的官方 Python SDK，用于通过 HTTP / WebSocket 与 Navo IM 服务端交互，支持登录、消息收发、会话管理、好友与频道等功能。

- **Navo IM 主项目（服务端 + Web 客户端）**：[https://github.com/aijianai/NavoIM](https://github.com/aijianai/NavoIM)
- **本 SDK 仓库**：[https://github.com/nichengfuben/navo-sdk](https://github.com/nichengfuben/navo-sdk)

## 安装

```bash
pip install navo-sdk
```

或从源码安装：

```bash
git clone https://github.com/nichengfuben/navo-sdk.git
cd navo-sdk
pip install -e .
```

## 快速开始

```python
from navo import Navo

# 同步登录（默认连接 https://navo.airoe.cn）
im = Navo().login("username", "password")

# 获取会话列表
conversations = im.get_conversations()
print(conversations)
```

异步用法：

```python
import asyncio
from navo import Navo

async def main():
    im = Navo()
    await im.alogin("username", "password")
    conversations = await im.aget_conversations()
    print(conversations)
    await im.aclose()

asyncio.run(main())
```

连接自建 Navo IM 实例时，可指定服务端地址：

```python
im = Navo(base_url="https://your-server.example.com", ws_url="wss://your-server.example.com/ws")
```

## 要求

- Python >= 3.10

## 许可证

MIT
