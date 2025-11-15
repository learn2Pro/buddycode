"""
React Agent Examples - Demonstrating React development tasks with the agent.

This file shows various ways to use the React code agent for common tasks.
"""

import os
from buddycode.react_agent import create_react_agent


def example_1_explore_project():
    """Example 1: Explore a React project structure."""
    print("\n" + "=" * 70)
    print("示例 1: 探索 React 项目结构")
    print("=" * 70)

    agent = create_react_agent(verbose=True)

    task = "请使用 tree 工具查看当前目录的结构，深度限制为 2 层"

    print(f"\n任务: {task}\n")
    result = agent.invoke({"input": task})

    print("\n结果:")
    print(result["output"])


def example_2_create_component():
    """Example 2: Create a new React component."""
    print("\n" + "=" * 70)
    print("示例 2: 创建新的 React 组件")
    print("=" * 70)

    agent = create_react_agent(verbose=True)

    task = """请在 /Users/bytedance/tmp 目录下创建一个名为 Button.tsx 的 React 组件。

要求：
1. 使用 TypeScript
2. 支持 children、onClick、disabled 属性
3. 添加基本的样式类名
4. 包含 JSDoc 注释"""

    print(f"\n任务: {task}\n")
    result = agent.invoke({"input": task})

    print("\n结果:")
    print(result["output"])


def example_3_find_todos():
    """Example 3: Find TODO comments in the project."""
    print("\n" + "=" * 70)
    print("示例 3: 查找项目中的 TODO 注释")
    print("=" * 70)

    agent = create_react_agent(verbose=True)

    task = "使用 grep 工具在当前项目中搜索所有 Python 文件中的 TODO 注释，最多显示 10 个结果"

    print(f"\n任务: {task}\n")
    result = agent.invoke({"input": task})

    print("\n结果:")
    print(result["output"])


def example_4_modify_component():
    """Example 4: Modify an existing component."""
    print("\n" + "=" * 70)
    print("示例 4: 修改现有组件")
    print("=" * 70)

    agent = create_react_agent(verbose=True)

    # First create a test component
    test_component = "/Users/bytedance/tmp/TestComponent.tsx"

    # Create test component using EditTool directly
    from buddycode.tools import EditTool
    edit = EditTool()

    initial_content = """import React from 'react';

interface TestProps {
  title: string;
}

export const TestComponent: React.FC<TestProps> = ({ title }) => {
  return <div>{title}</div>;
};
"""

    edit._run(operation="create", file_path=test_component, content=initial_content)
    print(f"✓ 创建测试组件: {test_component}\n")

    task = f"""请修改 {test_component} 文件：

1. 先查看当前内容
2. 添加一个新的 subtitle 属性到 TestProps
3. 在组件中显示 subtitle
4. 添加一个 className 属性"""

    print(f"任务: {task}\n")
    result = agent.invoke({"input": task})

    print("\n结果:")
    print(result["output"])


def example_5_run_commands():
    """Example 5: Run npm/yarn commands."""
    print("\n" + "=" * 70)
    print("示例 5: 运行 npm 命令")
    print("=" * 70)

    agent = create_react_agent(verbose=True)

    task = "使用 bash 工具检查系统中是否安装了 node 和 npm，并显示它们的版本"

    print(f"\n任务: {task}\n")
    result = agent.invoke({"input": task})

    print("\n结果:")
    print(result["output"])


def example_6_complex_workflow():
    """Example 6: Complex workflow - Create and test a component."""
    print("\n" + "=" * 70)
    print("示例 6: 复杂工作流 - 创建并测试组件")
    print("=" * 70)

    agent = create_react_agent(verbose=True)

    task = """请执行以下任务：

1. 在 /Users/bytedance/tmp 目录创建一个 Card.tsx 组件
2. 组件应该包含 title、description 和 imageUrl 属性
3. 创建后查看文件内容以验证
4. 使用 grep 确认所有属性都被正确使用"""

    print(f"\n任务: {task}\n")
    result = agent.invoke({"input": task})

    print("\n结果:")
    print(result["output"])


def example_7_code_review():
    """Example 7: Code review and suggestions."""
    print("\n" + "=" * 70)
    print("示例 7: 代码审查和建议")
    print("=" * 70)

    agent = create_react_agent(verbose=True)

    # Create a component with issues
    test_file = "/Users/bytedance/tmp/BadComponent.tsx"

    from buddycode.tools import EditTool
    edit = EditTool()

    bad_code = """import React from 'react';

export const BadComponent = (props) => {
  const data = props.data;
  return <div onClick={() => alert(data)}>{data}</div>;
};
"""

    edit._run(operation="create", file_path=test_file, content=bad_code)
    print(f"✓ 创建测试组件: {test_file}\n")

    task = f"""请审查 {test_file} 文件，指出以下问题：

1. TypeScript 类型定义
2. Props 解构
3. 事件处理最佳实践
4. 并提供改进建议"""

    print(f"任务: {task}\n")
    result = agent.invoke({"input": task})

    print("\n结果:")
    print(result["output"])


def run_all_examples():
    """Run all examples in sequence."""
    print("\n" + "=" * 70)
    print("React Agent - 完整示例演示")
    print("=" * 70)

    examples = [
        ("探索项目结构", example_1_explore_project),
        ("创建新组件", example_2_create_component),
        ("查找 TODO", example_3_find_todos),
        ("修改组件", example_4_modify_component),
        ("运行命令", example_5_run_commands),
        ("复杂工作流", example_6_complex_workflow),
        ("代码审查", example_7_code_review),
    ]

    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{'='*70}")
        print(f"运行示例 {i}/{len(examples)}: {name}")
        print(f"{'='*70}")

        try:
            func()
        except Exception as e:
            print(f"\n错误: {e}")

        # Pause between examples
        if i < len(examples):
            input("\n按 Enter 继续下一个示例...")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        examples_map = {
            "1": example_1_explore_project,
            "2": example_2_create_component,
            "3": example_3_find_todos,
            "4": example_4_modify_component,
            "5": example_5_run_commands,
            "6": example_6_complex_workflow,
            "7": example_7_code_review,
        }

        if example_num in examples_map:
            examples_map[example_num]()
        else:
            print(f"示例 {example_num} 不存在")
            print("可用示例: 1-7")
    else:
        # Run all examples
        run_all_examples()
