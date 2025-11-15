# React Code Agent

使用 LangChain 和 Doubao 大模型构建的 React 开发智能助手。

## 功能特性

React Code Agent 可以帮助你：

- 🔍 **探索代码库** - 使用 ls、tree、grep 工具快速了解项目结构
- 📝 **创建组件** - 自动生成符合规范的 React 组件
- ✏️ **修改代码** - 智能修改现有组件，添加功能或修复问题
- 🔎 **查找问题** - 搜索 TODO、FIXME 或特定代码模式
- 🧪 **运行测试** - 执行 npm/yarn 命令，运行测试和构建
- 📚 **代码审查** - 提供代码改进建议和最佳实践

## 快速开始

### 基础用法

```python
from buddycode.react_agent import create_react_agent

# 创建 agent
agent = create_react_agent(verbose=True)

# 执行任务
result = agent.invoke({
    "input": "请查看当前目录的项目结构"
})

print(result["output"])
```

### 交互模式

```bash
# 启动交互式对话
uv run python src/buddycode/react_agent.py
```

交互模式下，你可以：
- 输入自然语言任务
- Agent 会自动选择合适的工具
- 实时查看 Agent 的思考过程
- 输入 'quit' 或 'exit' 退出

## 使用示例

### 示例 1: 探索项目结构

```python
from buddycode.react_agent import create_react_agent

agent = create_react_agent()

result = agent.invoke({
    "input": "使用 tree 工具查看当前目录结构，深度限制为 2 层"
})
```

**Agent 会：**
1. 调用 TreeTool
2. 设置 max_depth=2
3. 返回项目结构

### 示例 2: 创建 React 组件

```python
agent = create_react_agent()

result = agent.invoke({
    "input": """创建一个 Button 组件在 src/components/Button.tsx

要求：
- 使用 TypeScript
- 支持 children、onClick、disabled、variant 属性
- variant 可以是 'primary' | 'secondary' | 'danger'
- 添加 JSDoc 注释
"""
})
```

**Agent 会：**
1. 使用 EditTool 的 create 操作
2. 生成符合要求的 TypeScript 代码
3. 包含类型定义和注释

### 示例 3: 修改现有组件

```python
agent = create_react_agent()

result = agent.invoke({
    "input": """修改 src/components/Card.tsx：

1. 先查看当前内容
2. 添加一个 onCardClick 回调属性
3. 在 Card 组件上绑定 onClick 事件
"""
})
```

**Agent 会：**
1. 使用 EditTool view 查看文件
2. 分析代码结构
3. 使用 str_replace 或 insert 修改代码
4. 再次 view 验证修改

### 示例 4: 查找和修复问题

```python
agent = create_react_agent()

result = agent.invoke({
    "input": """帮我找到并修复项目中的问题：

1. 搜索所有 TODO 注释
2. 列出需要完成的任务
3. 如果有简单的 TODO，帮我完成它
"""
})
```

**Agent 会：**
1. 使用 GrepTool 搜索 "TODO"
2. 分析搜索结果
3. 可能使用 EditTool 修复简单问题

### 示例 5: 运行测试和构建

```python
agent = create_react_agent()

result = agent.invoke({
    "input": """执行以下步骤：

1. 检查 package.json 中的脚本
2. 运行测试命令
3. 如果测试通过，运行构建
"""
})
```

**Agent 会：**
1. 使用 EditTool view 查看 package.json
2. 使用 BashTool 运行 `npm test`
3. 根据结果决定是否运行 `npm run build`

### 示例 6: 代码审查

```python
agent = create_react_agent()

result = agent.invoke({
    "input": """审查 src/App.tsx 并提供改进建议：

1. TypeScript 类型使用
2. React Hooks 使用是否正确
3. 性能优化建议
4. 可访问性改进
"""
})
```

## 可用工具

Agent 可以使用以下工具：

### 1. EditTool (edit)
- **view**: 查看文件内容（带行号）
- **create**: 创建新文件
- **insert**: 在指定行插入内容
- **str_replace**: 替换文本

### 2. LsTool (ls)
- 列出目录内容
- 支持详细格式、递归列表

### 3. GrepTool (grep)
- 正则表达式搜索
- 文件过滤（如 `*.tsx`）
- 上下文行显示

### 4. TreeTool (tree)
- 显示目录树结构
- 控制深度
- 仅显示目录选项

### 5. BashTool (bash)
- 执行 shell 命令
- 运行 npm/yarn
- 执行测试、构建

## 完整示例脚本

运行预定义的示例：

```bash
# 运行所有示例
uv run python examples_react_agent.py

# 运行特定示例
uv run python examples_react_agent.py 1  # 探索项目
uv run python examples_react_agent.py 2  # 创建组件
uv run python examples_react_agent.py 3  # 查找 TODO
```

## 配置选项

### 创建 Agent

```python
from buddycode.react_agent import create_react_agent

# 启用详细输出（显示 Agent 思考过程）
agent = create_react_agent(verbose=True)

# 安静模式（只显示结果）
agent = create_react_agent(verbose=False)
```

### Agent 参数

Agent 配置了以下参数：
- `max_iterations=15` - 最大迭代次数
- `handle_parsing_errors=True` - 自动处理解析错误
- `return_intermediate_steps=True` - 返回中间步骤

## 最佳实践

### 1. 明确的任务描述

✅ 好的提示：
```
创建一个 UserCard 组件在 src/components/UserCard.tsx

要求：
- 使用 TypeScript
- Props: name (string), email (string), avatar (string)
- 显示用户头像、名字和邮箱
- 添加 hover 效果
```

❌ 不好的提示：
```
帮我创建一个组件
```

### 2. 分步骤执行复杂任务

对于复杂任务，明确列出步骤：

```
执行以下步骤：
1. 查看 src/components 目录结构
2. 创建 Button.tsx 组件
3. 创建 Button.test.tsx 测试文件
4. 运行测试验证
```

### 3. 先查看再修改

修改代码前，让 Agent 先查看：

```
修改 src/App.tsx：
1. 先查看当前内容
2. 在第 10 行后添加新的 import
3. 验证修改
```

### 4. 使用具体的文件路径

✅ 具体：`src/components/Button.tsx`
❌ 模糊：`Button 组件`

### 5. 利用 Agent 的上下文

Agent 可以记住当前对话的上下文：

```
你: 查看 src/App.tsx
Agent: [显示内容]

你: 在第 5 行添加一个 import 语句
Agent: [知道你指的是 App.tsx]
```

## 常见任务模板

### 创建新功能

```
我要添加一个登录功能：
1. 创建 LoginForm.tsx 组件
2. 包含 username 和 password 输入框
3. 添加提交按钮
4. 使用 TypeScript 和表单验证
```

### 重构代码

```
重构 src/components/OldComponent.tsx：
1. 查看当前代码
2. 将 class 组件改为函数组件
3. 使用 Hooks 替换生命周期方法
4. 保持功能不变
```

### 调试问题

```
帮我调试 src/components/Header.tsx：
1. 查看代码
2. 查找可能导致渲染问题的代码
3. 检查 Props 类型定义
4. 提供修复建议
```

### 添加测试

```
为 src/components/Button.tsx 添加测试：
1. 创建 Button.test.tsx
2. 测试所有 props 组合
3. 测试 onClick 事件
4. 运行测试验证
```

## 故障排除

### Agent 无法找到文件

确保使用绝对路径或正确的相对路径：

```python
# 使用绝对路径
agent.invoke({"input": "查看 /Users/user/project/src/App.tsx"})

# 或者先确认当前目录
agent.invoke({"input": "使用 bash 命令 pwd 查看当前目录"})
```

### Agent 修改了错误的内容

使用更精确的字符串匹配：

```
使用 str_replace 操作，将：
old_str: "const [count, setCount] = useState(0);"
new_str: "const [count, setCount] = useState(10);"
```

### Agent 执行太慢

减少任务复杂度，分成多个简单任务：

```
# 不要这样
"创建整个登录系统，包括表单、验证、API 调用和错误处理"

# 应该这样
"创建登录表单组件 LoginForm.tsx"
# 然后
"添加表单验证逻辑"
# 然后
"添加 API 调用处理"
```

## 高级用法

### 自定义系统提示

```python
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate
from buddycode.chat_model import init_chat_model
from buddycode.tools import get_file_system_tools

llm = init_chat_model()
tools = get_file_system_tools()

# 自定义系统提示
custom_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专注于性能优化的 React 专家..."),
    # ... 其他消息
])

agent = create_structured_chat_agent(llm, tools, custom_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

### 添加自定义工具

```python
from langchain.tools import Tool
from buddycode.tools import get_file_system_tools

def my_custom_tool(input_str: str) -> str:
    """自定义工具逻辑"""
    return f"处理: {input_str}"

custom_tool = Tool(
    name="custom_tool",
    description="自定义工具描述",
    func=my_custom_tool
)

tools = get_file_system_tools() + [custom_tool]
```

## 示例输出

### 创建组件示例输出

```
你: 创建一个 Button 组件

Agent: 我来为你创建一个 Button 组件。

> 使用 edit 工具创建文件...

成功创建了 Button.tsx 文件，包含以下特性：
- TypeScript 类型定义
- Props: children, onClick, disabled, variant
- 支持三种样式变体: primary, secondary, danger
- 包含完整的 JSDoc 注释
- 可访问性属性 (aria-disabled)

组件已创建在: src/components/Button.tsx
```

## 相关文档

- [LangChain 文档](https://python.langchain.com/)
- [Doubao 模型文档](https://www.volcengine.com/docs/82379)
- [BuddyCode 工具文档](README.md)

## 贡献

欢迎贡献！如果你有改进建议或发现问题，请提交 Issue 或 PR。

## 许可证

MIT License
