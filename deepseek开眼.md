# deepseek开眼

## 原理

mcp + 多模态模型

## 前置条件

- python
- uv 

```
# python版本
python --version

# uvx 版本
uvx --version
```

## mcp

- 以 claude code 的 .mcp.json 文件为例，配置如下： 

```
{
  "mcpServers": {
    "mcp-vision-recognition": {
      "args": [
        "mcp-vision-recognition"
      ],
      "command": "uvx",
      "env": {
        "VISION_PROVIDER": "anthropic",
        "ANTHROPIC_API_KEY": "ollama",
        "ANTHROPIC_BASE_URL": "http://localhost:11434",
        "ANTHROPIC_MODEL": "minimax-m3:cloud",
        "MAX_TOKENS": "4080"
      }
    }
  }
}
```

## 多模态模型

### 白嫖方案

https://ollama.com/

- 推荐： minimax-m3:cloud
- 用量
    - 两小时限：10 - 15张图片
    - 周限：40 - 80张图片

### 自费方案

- 中转站便宜的模型

## 最后

执行 /mcp 命令，列表显示  mcp-vision-recognition 连接成功，即配置成功