<!-- ColorScope-CLI README - Multi-language Version -->
<!-- 多语言版本 - 简体中文 / 繁體中文 / English -->

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/WCAG-2.1 compliant-brightgreen.svg" alt="WCAG">
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> | 
  <a href="#繁體中文">繁體中文</a> | 
  <a href="#english">English</a>
</p>

---

<a name="简体中文"></a>
# 🎨 ColorScope-CLI

## 🎉 项目介绍

**ColorScope-CLI** 是一款**轻量级终端颜色对比度检查与可访问性分析引擎**，专为设计师、开发者和无障碍专家打造。

### 解决的痛点

- ✅ **WCAG 合规检查**：快速验证颜色组合是否符合 WCAG 2.1 AA/AAA 标准
- ✅ **色盲模拟**：模拟 7 种色盲类型，确保设计对所有用户友好
- ✅ **智能建议**：自动生成可访问的颜色调整方案
- ✅ **批量处理**：支持从配置文件批量检查颜色组合
- ✅ **多格式报告**：JSON、Markdown、HTML、纯文本报告输出

### 🌟 自研差异化亮点

| 特性 | ColorScope-CLI | 传统在线工具 |
|------|----------------|--------------|
| **离线使用** | ✅ 完全离线 | ❌ 需要网络 |
| **批量处理** | ✅ 支持 | ❌ 通常不支持 |
| **色盲模拟** | ✅ 7 种类型 | ⚠️ 部分支持 |
| **智能建议** | ✅ 自动生成 | ❌ 手动调整 |
| **CLI 集成** | ✅ 原生支持 | ❌ 无 |
| **报告生成** | ✅ 多格式 | ⚠️ 有限 |

---

## ✨ 核心特性

### 📊 WCAG 2.1 对比度检查

- **精确计算**：严格遵循 WCAG 2.1 对比度公式
- **多级别支持**：AA (4.5:1)、AAA (7:1)、大文本标准
- **实时反馈**：即时显示通过/失败状态

### 👁️ 色盲模拟

支持 7 种色盲类型模拟：

| 类型 | 描述 | 影响人群 |
|------|------|----------|
| **Protanopia** | 红色盲 | ~1% 男性 |
| **Deuteranopia** | 绿色盲 | ~1% 男性 |
| **Tritanopia** | 蓝色盲 | 极罕见 |
| **Achromatopsia** | 全色盲 | 极罕见 |
| **Protanomaly** | 红色弱 | ~1% 男性 |
| **Deuteranomaly** | 绿色弱 | ~5% 男性（最常见）|
| **Tritanomaly** | 蓝色弱 | 极罕见 |

### 💡 智能颜色建议

- **自动调整**：智能生成符合 WCAG 标准的颜色替代方案
- **多维度优化**：支持调整前景色、背景色或两者同时
- **保留色相**：在调整亮度的同时保持原始色相

### 📦 多格式报告

- **JSON**：结构化数据，便于程序处理
- **Markdown**：适合文档和 GitHub 展示
- **HTML**：可视化报告，包含颜色预览
- **Text**：纯文本格式，适合终端输出

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux

### 安装

```bash
# 使用 pip 安装
pip install colorscope-cli

# 或使用 pipx 安装（推荐）
pipx install colorscope-cli

# 从源码安装
git clone https://github.com/yourusername/colorscope-cli.git
cd colorscope-cli
pip install -e .
```

### 基本使用

```bash
# 检查两个颜色的对比度
colorscope check "#FFFFFF" "#000000"

# 详细输出（包含建议）
colorscope check "#FF5733" "#FFFFFF" --detailed

# 模拟色盲效果
colorscope simulate "#FF5733" --type deuteranopia

# 获取改进建议
colorscope suggest "#FF5733" "#FFFFFF" --level aa

# 批量检查
colorscope batch colors.json --output report.md

# 交互模式
colorscope interactive
```

---

## 📖 详细使用指南

### 1️⃣ 对比度检查

```bash
# 基本检查
colorscope check "#FFFFFF" "#000000"

# 输出示例：
# ┌─────────────────────────────────────┐
# │     🎨 Contrast Check Result        │
# ├─────────────┬───────────────────────┤
# │ Foreground  │ #FFFFFF               │
# │ Background  │ #000000               │
# │ Ratio       │ 21.00:1               │
# │ WCAG AA     │ ✅ PASS               │
# │ WCAG AAA    │ ✅ PASS               │
# └─────────────┴───────────────────────┘
```

### 2️⃣ 色盲模拟

```bash
# 模拟所有色盲类型
colorscope simulate "#FF5733"

# 模拟特定类型
colorscope simulate "#FF5733" --type deuteranopia
```

### 3️⃣ 智能建议

```bash
# 获取前景色调整建议
colorscope suggest "#FF5733" "#FFFFFF" --adjust foreground

# 获取背景色调整建议
colorscope suggest "#FF5733" "#FFFFFF" --adjust background

# 同时调整两者
colorscope suggest "#FF5733" "#FFFFFF" --adjust both
```

### 4️⃣ 批量处理

创建 `colors.json` 文件：

```json
{
  "colors": [
    {"foreground": "#FFFFFF", "background": "#000000"},
    {"foreground": "#FF5733", "background": "#FFFFFF"},
    {"foreground": "#767676", "background": "#FFFFFF"}
  ]
}
```

运行批量检查：

```bash
# 生成 Markdown 报告
colorscope batch colors.json --output report.md --format markdown

# 生成 HTML 报告
colorscope batch colors.json --output report.html --format html

# 生成 JSON 报告
colorscope batch colors.json --output report.json --format json
```

### 5️⃣ Python API

```python
from colorscope import ContrastChecker, Color, ColorBlindnessSimulator

# 创建检查器
checker = ContrastChecker()

# 检查对比度
result = checker.check("#FF5733", "#FFFFFF")
print(f"Contrast Ratio: {result.ratio:.2f}:1")
print(f"WCAG AA: {'PASS' if result.aa_normal else 'FAIL'}")

# 色盲模拟
simulator = ColorBlindnessSimulator()
sim_results = simulator.simulate_all(Color.from_hex("#FF5733"))

for blindness_type, sim_result in sim_results.items():
    print(f"{blindness_type}: {sim_result.simulated.to_hex()}")
```

---

## 💡 设计思路与迭代规划

### 设计理念

ColorScope-CLI 的设计遵循以下原则：

1. **零核心依赖**：仅依赖 Rich 库用于终端美化输出
2. **WCAG 优先**：严格遵循 WCAG 2.1 规范
3. **开发者友好**：提供 CLI 和 Python API 两种使用方式
4. **可扩展性**：模块化设计，易于添加新功能

### 技术选型

| 技术 | 选择原因 |
|------|----------|
| **Python 3.8+** | 广泛兼容性，丰富的生态系统 |
| **Rich** | 美观的终端输出，提升用户体验 |
| **纯算法实现** | 无需外部 API，完全离线可用 |

### 后续迭代计划

- [ ] **v1.1**: 添加 YAML 配置文件支持
- [ ] **v1.2**: 集成颜色名称数据库（如 "Coral Red" → "#FF7F50"）
- [ ] **v1.3**: 添加图片颜色提取功能
- [ ] **v1.4**: 支持从 CSS/SCSS 文件提取颜色
- [ ] **v2.0**: 图形界面版本（TUI）

---

## 📦 打包与部署指南

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/colorscope-cli.git
cd colorscope-cli

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black .
isort .

# 类型检查
mypy colorscope
```

### 构建发布

```bash
# 安装构建工具
pip install build twine

# 构建
python -m build

# 检查
twine check dist/*

# 上传到 PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 本仓库
2. **创建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **提交** Pull Request

### 提交规范

请遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 问题反馈

如果您发现 Bug 或有功能建议，请在 [Issues](https://github.com/yourusername/colorscope-cli/issues) 页面提交。

---

## 📄 开源协议说明

本项目采用 **MIT 协议** 开源。

这意味着您可以：
- ✅ 商业使用
- ✅ 修改代码
- ✅ 分发代码
- ✅ 私人使用

唯一要求是在代码中保留版权声明。

---

<p align="center">
  Made with ❤️ by ColorScope Team
</p>

---

<a name="繁體中文"></a>
# 🎨 ColorScope-CLI

## 🎉 專案介紹

**ColorScope-CLI** 是一款**輕量級終端顏色對比度檢查與無障礙分析引擎**，專為設計師、開發者和無障礙專家打造。

### 解決的痛點

- ✅ **WCAG 合規檢查**：快速驗證顏色組合是否符合 WCAG 2.1 AA/AAA 標準
- ✅ **色盲模擬**：模擬 7 種色盲類型，確保設計對所有使用者友善
- ✅ **智慧建議**：自動生成無障礙的顏色調整方案
- ✅ **批次處理**：支援從設定檔批次檢查顏色組合
- ✅ **多格式報告**：JSON、Markdown、HTML、純文字報告輸出

### 🌟 自研差異化亮點

| 特性 | ColorScope-CLI | 傳統線上工具 |
|------|----------------|--------------|
| **離線使用** | ✅ 完全離線 | ❌ 需要網路 |
| **批次處理** | ✅ 支援 | ❌ 通常不支援 |
| **色盲模擬** | ✅ 7 種類型 | ⚠️ 部分支援 |
| **智慧建議** | ✅ 自動生成 | ❌ 手動調整 |
| **CLI 整合** | ✅ 原生支援 | ❌ 無 |
| **報告生成** | ✅ 多格式 | ⚠️ 有限 |

---

## ✨ 核心特性

### 📊 WCAG 2.1 對比度檢查

- **精確計算**：嚴格遵循 WCAG 2.1 對比度公式
- **多級別支援**：AA (4.5:1)、AAA (7:1)、大文字標準
- **即時回饋**：即時顯示通過/失敗狀態

### 👁️ 色盲模擬

支援 7 種色盲類型模擬：

| 類型 | 描述 | 影響人群 |
|------|------|----------|
| **Protanopia** | 紅色盲 | ~1% 男性 |
| **Deuteranopia** | 綠色盲 | ~1% 男性 |
| **Tritanopia** | 藍色盲 | 極罕見 |
| **Achromatopsia** | 全色盲 | 極罕見 |
| **Protanomaly** | 紅色弱 | ~1% 男性 |
| **Deuteranomaly** | 綠色弱 | ~5% 男性（最常見）|
| **Tritanomaly** | 藍色弱 | 極罕見 |

### 💡 智慧顏色建議

- **自動調整**：智慧生成符合 WCAG 標準的顏色替代方案
- **多維度最佳化**：支援調整前景色、背景色或兩者同時
- **保留色相**：在調整亮度的同時保持原始色相

---

## 🚀 快速開始

### 環境要求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows / macOS / Linux

### 安裝

```bash
# 使用 pip 安裝
pip install colorscope-cli

# 或使用 pipx 安裝（推薦）
pipx install colorscope-cli
```

### 基本使用

```bash
# 檢查兩個顏色的對比度
colorscope check "#FFFFFF" "#000000"

# 詳細輸出（包含建議）
colorscope check "#FF5733" "#FFFFFF" --detailed

# 模擬色盲效果
colorscope simulate "#FF5733" --type deuteranopia

# 取得改進建議
colorscope suggest "#FF5733" "#FFFFFF" --level aa

# 批次檢查
colorscope batch colors.json --output report.md

# 互動模式
colorscope interactive
```

---

## 📖 詳細使用指南

### Python API 範例

```python
from colorscope import ContrastChecker, Color, ColorBlindnessSimulator

# 建立檢查器
checker = ContrastChecker()

# 檢查對比度
result = checker.check("#FF5733", "#FFFFFF")
print(f"對比度: {result.ratio:.2f}:1")
print(f"WCAG AA: {'通過' if result.aa_normal else '失敗'}")

# 色盲模擬
simulator = ColorBlindnessSimulator()
sim_results = simulator.simulate_all(Color.from_hex("#FF5733"))

for blindness_type, sim_result in sim_results.items():
    print(f"{blindness_type}: {sim_result.simulated.to_hex()}")
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 如何貢獻

1. **Fork** 本倉庫
2. **建立** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 變更 (`git commit -m 'feat: Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **提交** Pull Request

---

## 📄 開源協議說明

本專案採用 **MIT 協議** 開源。

---

<p align="center">
  Made with ❤️ by ColorScope Team
</p>

---

<a name="english"></a>
# 🎨 ColorScope-CLI

## 🎉 Introduction

**ColorScope-CLI** is a **lightweight terminal color contrast checker and accessibility analysis engine**, designed for designers, developers, and accessibility experts.

### Problems Solved

- ✅ **WCAG Compliance**: Quickly verify color combinations meet WCAG 2.1 AA/AAA standards
- ✅ **Color Blindness Simulation**: Simulate 7 types of color vision deficiency
- ✅ **Smart Suggestions**: Automatically generate accessible color alternatives
- ✅ **Batch Processing**: Check multiple color pairs from configuration files
- ✅ **Multi-format Reports**: JSON, Markdown, HTML, and plain text output

### 🌟 Key Differentiators

| Feature | ColorScope-CLI | Traditional Online Tools |
|---------|----------------|--------------------------|
| **Offline Use** | ✅ Fully offline | ❌ Requires internet |
| **Batch Processing** | ✅ Supported | ❌ Usually not |
| **Color Blindness Sim** | ✅ 7 types | ⚠️ Partial support |
| **Smart Suggestions** | ✅ Auto-generated | ❌ Manual adjustment |
| **CLI Integration** | ✅ Native support | ❌ None |
| **Report Generation** | ✅ Multi-format | ⚠️ Limited |

---

## ✨ Core Features

### 📊 WCAG 2.1 Contrast Checking

- **Accurate Calculation**: Strictly follows WCAG 2.1 contrast formula
- **Multi-level Support**: AA (4.5:1), AAA (7:1), large text standards
- **Instant Feedback**: Real-time pass/fail status

### 👁️ Color Blindness Simulation

Supports 7 types of color vision deficiency:

| Type | Description | Affected Population |
|------|-------------|---------------------|
| **Protanopia** | Red blindness | ~1% of males |
| **Deuteranopia** | Green blindness | ~1% of males |
| **Tritanopia** | Blue blindness | Very rare |
| **Achromatopsia** | Total color blindness | Extremely rare |
| **Protanomaly** | Red weakness | ~1% of males |
| **Deuteranomaly** | Green weakness | ~5% of males (most common) |
| **Tritanomaly** | Blue weakness | Very rare |

### 💡 Smart Color Suggestions

- **Auto Adjustment**: Intelligently generate WCAG-compliant alternatives
- **Multi-dimensional Optimization**: Adjust foreground, background, or both
- **Hue Preservation**: Maintain original hue while adjusting lightness

### 📦 Multi-format Reports

- **JSON**: Structured data for programmatic processing
- **Markdown**: Documentation-friendly format
- **HTML**: Visual reports with color previews
- **Text**: Plain text for terminal output

---

## 🚀 Quick Start

### Requirements

- **Python**: 3.8 or higher
- **OS**: Windows / macOS / Linux

### Installation

```bash
# Install with pip
pip install colorscope-cli

# Or with pipx (recommended)
pipx install colorscope-cli

# Install from source
git clone https://github.com/yourusername/colorscope-cli.git
cd colorscope-cli
pip install -e .
```

### Basic Usage

```bash
# Check contrast between two colors
colorscope check "#FFFFFF" "#000000"

# Detailed output with suggestions
colorscope check "#FF5733" "#FFFFFF" --detailed

# Simulate color blindness
colorscope simulate "#FF5733" --type deuteranopia

# Get improvement suggestions
colorscope suggest "#FF5733" "#FFFFFF" --level aa

# Batch processing
colorscope batch colors.json --output report.md

# Interactive mode
colorscope interactive
```

---

## 📖 Detailed Usage Guide

### 1️⃣ Contrast Checking

```bash
# Basic check
colorscope check "#FFFFFF" "#000000"

# Example output:
# ┌─────────────────────────────────────┐
# │     🎨 Contrast Check Result        │
# ├─────────────┬───────────────────────┤
# │ Foreground  │ #FFFFFF               │
# │ Background  │ #000000               │
# │ Ratio       │ 21.00:1               │
# │ WCAG AA     │ ✅ PASS               │
# │ WCAG AAA    │ ✅ PASS               │
# └─────────────┴───────────────────────┘
```

### 2️⃣ Color Blindness Simulation

```bash
# Simulate all types
colorscope simulate "#FF5733"

# Simulate specific type
colorscope simulate "#FF5733" --type deuteranopia
```

### 3️⃣ Smart Suggestions

```bash
# Get foreground adjustment suggestions
colorscope suggest "#FF5733" "#FFFFFF" --adjust foreground

# Get background adjustment suggestions
colorscope suggest "#FF5733" "#FFFFFF" --adjust background

# Adjust both
colorscope suggest "#FF5733" "#FFFFFF" --adjust both
```

### 4️⃣ Batch Processing

Create `colors.json`:

```json
{
  "colors": [
    {"foreground": "#FFFFFF", "background": "#000000"},
    {"foreground": "#FF5733", "background": "#FFFFFF"},
    {"foreground": "#767676", "background": "#FFFFFF"}
  ]
}
```

Run batch check:

```bash
# Generate Markdown report
colorscope batch colors.json --output report.md --format markdown

# Generate HTML report
colorscope batch colors.json --output report.html --format html

# Generate JSON report
colorscope batch colors.json --output report.json --format json
```

### 5️⃣ Python API

```python
from colorscope import ContrastChecker, Color, ColorBlindnessSimulator

# Create checker
checker = ContrastChecker()

# Check contrast
result = checker.check("#FF5733", "#FFFFFF")
print(f"Contrast Ratio: {result.ratio:.2f}:1")
print(f"WCAG AA: {'PASS' if result.aa_normal else 'FAIL'}")

# Color blindness simulation
simulator = ColorBlindnessSimulator()
sim_results = simulator.simulate_all(Color.from_hex("#FF5733"))

for blindness_type, sim_result in sim_results.items():
    print(f"{blindness_type}: {sim_result.simulated.to_hex()}")
```

---

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Zero Core Dependencies**: Only Rich library for beautiful terminal output
2. **WCAG First**: Strictly follow WCAG 2.1 specifications
3. **Developer Friendly**: Both CLI and Python API available
4. **Extensibility**: Modular design for easy feature additions

### Tech Stack

| Technology | Reason |
|------------|--------|
| **Python 3.8+** | Wide compatibility, rich ecosystem |
| **Rich** | Beautiful terminal output, enhanced UX |
| **Pure Algorithm** | No external APIs, fully offline |

### Roadmap

- [ ] **v1.1**: YAML configuration file support
- [ ] **v1.2**: Color name database integration
- [ ] **v1.3**: Image color extraction feature
- [ ] **v1.4**: CSS/SCSS file color extraction
- [ ] **v2.0**: TUI (Terminal User Interface) version

---

## 📦 Build & Deployment

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/colorscope-cli.git
cd colorscope-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Type check
mypy colorscope
```

### Build & Publish

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Check
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### How to Contribute

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Submit** a Pull Request

### Commit Convention

Please follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related
- `chore:` Build/tool related

### Bug Reports

If you find a bug or have a feature request, please submit it on the [Issues](https://github.com/yourusername/colorscope-cli/issues) page.

---

## 📄 License

This project is licensed under the **MIT License**.

This means you can:
- ✅ Commercial use
- ✅ Modify code
- ✅ Distribute code
- ✅ Private use

The only requirement is to keep the copyright notice in the code.

---

<p align="center">
  Made with ❤️ by ColorScope Team
</p>
