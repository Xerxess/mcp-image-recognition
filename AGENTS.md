# 仓库指南

## 项目结构与模块组织

应用代码位于 `src/image_recognition_server/`。`server.py` 定义 MCP 工具及服务商选择逻辑；`vision/` 包含 Anthropic 和 OpenAI 适配器；`utils/` 负责图像转换与可选的 OCR 功能。测试位于 `tests/`，按功能命名，如 `test_server.py` 和 `test_ocr.py`。根目录包含打包配置 `setup.py`、依赖清单、Windows 辅助脚本、Docker 配置及环境变量模板。

## 构建、测试与开发命令

- `python -m pip install -r requirements-dev.txt && python -m pip install -e .`：安装运行及开发依赖，并以可编辑模式安装项目。
- `build.bat`：安装依赖，格式化并检查 `src/`，随后构建软件包至 `build/`。
- `run.bat test`：运行完整 pytest 测试；`run.bat test server`：仅运行服务端测试。
- `python -m pytest tests/test_ocr.py -v`：直接运行单个测试模块。
- `python -m image_recognition_server.server`：启动以可编辑模式安装的服务；`run.bat debug`：使用 MCP Inspector 启动构建后的服务。
- `docker build -t mcp-image-recognition .`：构建容器镜像。

## 编码风格与命名约定

使用 Python 3.10 或更高版本。采用四空格缩进，为公共接口添加类型注解，并为工具、fixture 和不直观的辅助函数编写简洁的文档字符串。模块、函数及变量使用 `snake_case`，类使用 `PascalCase`，常量使用 `UPPER_CASE`。提交前运行 `black src tests`、`isort src tests`、`ruff check src tests` 和 `mypy src`。

## 测试指南

项目使用 `pytest` 和 `pytest-asyncio`。测试文件命名为 `test_<功能>.py`，测试函数命名为 `test_<行为>`。协程测试须添加 `@pytest.mark.asyncio`；使用 fixture 和 `monkeypatch` 隔离环境变量与外部客户端。OCR 集成测试需要 Tesseract，服务商测试可能需要 API 配置。单元测试应保持确定性，并模拟网络请求。项目未强制覆盖率阈值，但修改核心处理流程时应运行 `pytest tests -v --cov=src`。

## 配置与安全

复制 `.env.example` 为 `.env` 以配置本地环境。禁止提交 API 密钥、生成的日志或本地图像数据。新增环境变量时，需同时更新 `.env.example` 和 `README.md`，并提供安全的默认值。

## 提交与拉取请求规范

现有历史使用简短的祈使句主题，如 `Update ...`、`Fix ...` 和 `Simplify ...`；请沿用此风格，并确保每个提交只聚焦一个改动。拉取请求应说明行为变化、列出验证命令、关联相关 Issue，并注明配置变更。仅在有助于说明用户可见行为时附上截图或 MCP Inspector 输出。
