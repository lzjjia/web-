# 🚀 Web 自动化测试框架（Selenium + Python + Pytest + Allure）

一个模块化、可扩展的 **Web UI 自动化测试框架**，基于 **Selenium WebDriver**、**Python**、**Pytest** 和 **Allure** 构建。采用 **Page Object Model（POM）** 设计模式，分层清晰，适合初学者学习及实际项目使用。

---

## 📁 目录结构

```
项目根目录/
├── base/                  ← 测试基类，封装通用 Selenium 操作方法
├── configfiles/           ← 环境配置文件（QA / Dev），YAML 格式
├── logs/                  ← 运行日志，按时间戳自动归档
├── pages/                 ← 页面对象类，封装页面元素定位与操作
├── reports/               ← Allure 测试报告，按日期 → 时间组织
├── screenshots/           ← 失败/手动截图，按日期 → 时间组织
├── testcases/             ← 测试用例脚本
├── testdata/              ← 测试数据，与用例逻辑分离
├── utilities/             ← 工具类与辅助函数
├── conftest.py            ← Pytest 的 fixture 与钩子，框架控制中心
├── pytest.ini             ← Pytest 配置（自定义标记等）
├── requirements.txt       ← 项目依赖清单
├── Runner.py              ← 测试执行入口，封装 pytest 命令行参数
├── Setup.bat              ← Windows 一键环境安装脚本
└── README.md              ← 项目说明文档
```

---

## ✅ 环境准备

在开始之前，请确保你的系统已安装：

- **Python** 3.8 及以上版本
- **pip**（Python 包管理工具）
- **Git**（版本控制）
- **代码编辑器**（推荐 VS Code 或 PyCharm）
- **Google Chrome** 或 **Firefox** 浏览器
- **Allure 命令行工具**（用于生成测试报告）

验证 Allure 是否安装成功：
```bash
allure --version
```

---

## ⚙️ 安装步骤

### 第一步：克隆项目

```bash
git clone https://github.com/lzjjia/web-.git
cd web-
```

### 第二步：一键安装（Windows）

双击运行 `Setup.bat`，脚本会自动完成虚拟环境创建和依赖安装。

### 第三步：手动安装（备选方案）

```bash
python -m venv venv              # 创建虚拟环境
venv\Scripts\activate            # 激活虚拟环境（Windows）
# 或 source venv/bin/activate    # macOS / Linux
pip install -r requirements.txt  # 安装所有依赖
```

---

## 🧪 编写测试用例

在该框架中编写测试用例遵循以下约定：

- 测试脚本统一放在 `testcases/` 目录下
- 测试文件和测试方法名必须以 `test_` 开头，pytest 才能自动识别
- 页面元素和操作封装在 `pages/` 目录下，每个页面一个类
- 可复用的业务动作提取到 `utilities/` 或 `base/` 中
- 测试数据统一放在 `testdata/` 目录，与测试逻辑分离

示例测试文件：`testcases/test_sample.py`

---

## ▶️ 运行测试

### 基本用法

```bash
python Runner.py                        # 运行全部测试（默认 Chrome 浏览器 + QA 环境）
```

### 按标记筛选（冒烟测试）

```bash
python Runner.py -m smoke               # 只运行标记为 smoke 的用例
```

### 指定浏览器和环境

```bash
python Runner.py --browser_name=firefox # 使用 Firefox 浏览器
python Runner.py --env=dev              # 加载 Dev 环境配置
python Runner.py --browser_name=edge --env=qa  # 组合使用
```

### 按关键字筛选

```bash
python Runner.py -k test_login          # 只运行名称匹配的用例
```

### 重复执行

```bash
python Runner.py -r 4                   # 每个用例重复执行 4 次
```

---

## 🗂️ 报告与日志

| 目录            | 说明                                        |
| --------------- | ------------------------------------------- |
| `logs/`         | 存放每次运行的时间戳日志文件                |
| `reports/`      | Allure 报告文件，按 日期 → 时间 分类存放    |
| `screenshots/`  | 失败自动截图与手动截图，按 日期 → 时间 组织 |

---

## 📄 配置文件说明

| 文件                   | 作用                               |
| ---------------------- | ---------------------------------- |
| `configfiles/*.yaml`   | 环境相关配置（URL、账号等）        |
| `pytest.ini`           | pytest 级别配置（自定义标记等）    |
| `conftest.py`          | fixture 与钩子，管理测试前后置逻辑 |

---

## 🛠️ 技术栈

- **Selenium WebDriver** — 浏览器自动化驱动
- **Python** — 核心开发语言
- **Pytest** — 测试执行引擎与 fixture 管理
- **Allure** — 可视化测试报告
- **PyYAML** — 环境配置解析
- **pytest-html** — 备用 HTML 报告
- **pytest-repeat** — 用例重复执行

---

## 🎯 框架特性

- **Page Object Model** 分层架构，页面与用例解耦
- **数据驱动测试**，一套用例覆盖多组数据
- **失败自动截图**，无需手动排查错误现场
- **多浏览器支持**（Chrome / Firefox / Edge）
- **多环境切换**（QA / Dev），一条命令切换配置
- **Allure 可视化报告**，包含步骤描述、截图、环境信息
- **自定义标记**，灵活筛选冒烟测试 / 回归测试
- **时间戳归档**，报告、日志、截图按运行时间独立存放
