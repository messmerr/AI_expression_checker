

# 表达式等价比对器

这是一个基于大模型API的数学表达式等价性判断工具，可以判断两个数学表达式是否在所有可能的取值下都相等。该工具提供命令行界面和图形用户界面两种使用方式，适合用于测试表达式变换程序的正确性。

## 功能特点

- 通过调用大模型API判断两个数学表达式是否等价
- 支持自定义API服务地址、API密钥和模型名称
- 提供命令行界面和图形用户界面两种使用方式
- 模块化设计，易于扩展和集成到其他测试工具中
- 支持详细模式，显示API请求和响应的详细信息

## 安装依赖

```bash
pip install requests
```

如果需要使用图形界面，还需要安装tkinter（大多数Python安装已包含）：

```bash
# 在Debian/Ubuntu系统上
sudo apt-get install python3-tk

# 在CentOS/RHEL系统上
sudo yum install python3-tkinter

# 在macOS上（使用Homebrew）
brew install python-tk
```

## 使用方法

### 命令行界面

```bash
# 基本用法
python expression_equivalence.py --expr1 "a+b" --expr2 "b+a" --api_key "your_api_key"

# 使用自定义API地址
python expression_equivalence.py --expr1 "a*(b+c)" --expr2 "a*b+a*c" --base_url "https://your-api-server.com/v1" --api_key "your_api_key"

# 使用详细模式查看更多信息
python expression_equivalence.py --expr1 "sin(x)^2 + cos(x)^2" --expr2 "1" --verbose --api_key "your_api_key"
```

### 图形用户界面

```bash
python expression_equivalence_gui.py
```

在图形界面中，您可以：
1. 输入两个需要比较的数学表达式
2. 配置API设置（基础URL、API密钥、模型名称和温度参数）
3. 点击"判断等价性"按钮进行判断
4. 查看判断结果

## 环境变量配置

您可以通过设置以下环境变量来提供默认配置：

- `LLM_API_BASE_URL`: API基础URL（默认为"https://api.openai.com/v1"）
- `LLM_API_KEY`: API密钥
- `LLM_MODEL`: 使用的模型名称（默认为"gpt-3.5-turbo"）

例如：

```bash
export LLM_API_BASE_URL="https://your-api-server.com/v1"
export LLM_API_KEY="your_api_key"
export LLM_MODEL="gpt-4"
```

## 返回状态码

命令行版本会返回以下状态码：

- `0`: 表达式等价
- `1`: 表达式不等价
- `2`: 无法确定是否等价
- `3`: 发生错误（如API调用失败）

## 示例

### 等价表达式示例

- `a+b` 和 `b+a`（交换律）
- `a*(b+c)` 和 `a*b+a*c`（分配律）
- `sin(x)^2 + cos(x)^2` 和 `1`（三角恒等式）
- `(a+b)^2` 和 `a^2+2*a*b+b^2`（平方展开）

### 不等价表达式示例

- `a+b` 和 `a-b`
- `x^2` 和 `x`
- `sin(x)` 和 `x`（仅在x接近0时近似相等）

## 项目结构

- `expression_equivalence.py`: 命令行版本，包含核心功能
- `expression_equivalence_gui.py`: 图形界面版本，复用命令行版本的核心功能

## 扩展性

该工具采用模块化设计，核心功能与界面分离，便于扩展和集成：

1. 可以轻松添加新的界面（如Web界面）
2. 可以扩展为批量处理多组表达式
3. 可以集成到自动化测试流程中
4. 可以添加缓存机制，避免重复API调用

## 注意事项

- 该工具依赖于大模型的数学能力，不同模型可能有不同的判断准确度
- 对于复杂表达式，建议使用更强大的模型（如GPT-4）获得更准确的结果
- API调用可能产生费用，请注意控制使用量

## 许可证

MIT

## 贡献

欢迎提交问题报告和改进建议！
