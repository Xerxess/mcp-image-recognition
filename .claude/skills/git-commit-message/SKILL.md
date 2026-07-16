---
name: git-commit-message
description: >
  根据已暂存的 git diff 生成符合 Conventional Commits 规范的提交信息。
  当用户提到"我要提交""帮我写 commit""commit message""生成提交信息"
  "怎么写 commit""准备提交"等任何与编写 git 提交信息相关的场景时使用此技能。
  也适用于用户说"看看我改了什么，帮我写个 commit"这类组合请求。
---

# Git Commit Message 生成器

分析 `git diff --cached` 的变更内容，生成符合 Conventional Commits 规范的提交信息。
**仅生成建议，不执行任何 git 命令。**

## 工作流程

### 1. 获取变更

执行 `git diff --cached`。如果暂存区为空，提醒用户先 `git add`，终止流程。

### 2. 提取关键信息

快速扫一遍 diff，提取：

- 改了哪些文件（路径、新增/修改/删除）
- 改动性质（新功能、修 bug、重构、格式、文档等）
- 改动规模（文件数、行数）

### 3. 判定 type

| Type       | 适用场景                                       |
| ---------- | ---------------------------------------------- |
| `feat`     | 新功能、新页面、新组件、新接口                 |
| `fix`      | Bug 修复、异常处理、边界情况修正               |
| `docs`     | 仅文档/注释变更                                |
| `style`    | 代码格式（空格、缩进、分号、引号），不影响逻辑 |
| `refactor` | 重构——改结构不改行为                           |
| `perf`     | 性能优化（懒加载、缓存、减少请求等）           |
| `test`     | 测试代码                                       |
| `build`    | 构建系统或依赖（package.json、vite.config 等） |
| `ci`       | CI/CD 配置                                     |
| `chore`    | 其他杂务（非 src/test 的维护性改动）           |
| `revert`   | 回退之前的提交                                 |

**判断优先级**：看改动的主要目的。一个 commit 里可能同时有新功能和重构，以主导目的为准。

### 4. 推断 scope

从文件路径推断影响范围。参考以下映射：

| 路径模式                       | scope         |
| ------------------------------ | ------------- |
| `src/pages/<name>/`            | `<name>`      |
| `src/api/modules/<name>.ts`    | `<name>`      |
| `src/components/base/`         | `base`        |
| `src/stores/modules/<name>.ts` | `<name>`      |
| `src/composables/`             | `composables` |
| `src/utils/`                   | `utils`       |
| `src/config/`                  | `config`      |
| `src/styles/`                  | `styles`      |
| `src/types/`                   | `types`       |
| `src/locale/`                  | `locale`      |
| `src/platform/`                | `platform`    |
| 根目录配置文件                 | `config`      |

**多模块规则**：

- 主要改动集中在一个模块 → 只用该模块
- 均匀分散在 3+ 个模块 → 省略 scope
- 配置文件 + 一个模块 → 用那个模块的 scope

### 5. 编写 subject

- **语言**：中文
- **长度**：≤ 50 字符
- **风格**：祈使句，以「添加/修复/重构/优化/更新/移除/回退/简化/调整」开头
- 不加句号
- 描述**用户/开发者能感知的变化**，而非代码细节

✅ 好：

```
feat(order): 添加订单取消功能
fix(auth): 修复 token 过期后白屏的问题
refactor(api): 简化请求拦截器链
```

❌ 差：

```
feat: 新增了 OrderCancelButton 组件  ← 描述代码而非功能，且 ≤50 字符不应写 body
fix: 改了一个 bug                      ← 太模糊
Feat(user): 添加用户管理页面           ← 大写前缀
```

### 6. 编写 body（按需）

以下情况才需要 body：

- 改动原因不明显，需要解释「为什么」
- 涉及多个不相关文件的改动
- 实现方式有值得说明的权衡

格式：

- 每行 ≤ 72 字符
- 用 `- ` 项目符号列出要点
- 解释**动机和决策**，diff 已经说清了「改了什么」

### 7. 编写 footer（按需）

- 关联 Issue：`Closes #<编号>` 或 `Refs #<编号>`（如果 diff 中能判断或用户告知）
- Breaking Change：`BREAKING CHANGE:` 开头，说明具体影响和迁移方式

### 8. 输出

用代码块包裹完整提交信息：

````
```
<type>(<scope>): <subject>

<body>

<footer>
```
````

然后 1-2 句话说明判断依据（为什么是这个 type 和 scope）。

## 注意事项

- 请使用中文提交
- 注意PowerShell 5.1 中，@'...'@ 用于给 PowerShell 变量赋多行字符串值
- 执行提交指南 — 新增"用户要求执行提交时"小节：要求用 PowerShell here-string @'...'@ 传多行消息，禁止用 Bash 执行 git commit -m
- 确保subject正确
- 暂存区超过 500 行改动时，提示用户考虑拆分为多个提交
- 如果检测到疑似敏感信息（API key、token、密码等明文），提醒用户检查
- **不执行任何 git 命令**——只生成建议
- 不要为了凑格式而编造 scope 或 body
