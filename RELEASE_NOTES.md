# 更新日志

## v0.1.1 Alpha - 性能与文档更新 (2026-01-03)

### 🚀 性能改进

**38.63% 性能提升** 🎉

- **解析器优化**
  - 方法缓存以减少属性访问开销
  - 使用 frozenset 替代普通集合存储不可变数据
  - 类级常量用于频繁使用的数据
  - 优化数字处理逻辑
  - 优化循环表构建

- **基准测试**
  - 平均解析时间从 0.013954ms 降低到 0.012331ms
  - 所有 400+ 测试用例全部通过
  - 20 次验证测试，包含详细统计数据

### 🧪 测试基础设施

- **测试脚本修复**
  - 修复所有测试脚本中的 `sys.path` 配置
  - 修复 `test_comment_validation.py` 中的 Token 对象比较
  - 所有测试现在都可以从命令行运行

- **新增测试工具**
  - `test_optimization.py` - 20 次优化验证
  - `tests/benchmark_parser.py` - 性能基准测试工具
  - `tests/run_comprehensive_tests.py` - 完整测试套件（400+ 用例）
  - `analyze_results.py` - 结果分析工具
  - `compare_results.py` - 性能对比工具

- **测试结果存储**
  - 基于 JSON 的结果存储在 `tests/results/`
  - 历史性能跟踪
  - 详细统计信息（平均值、最小值、最大值、标准差）

### 📚 文档系统

- **VitePress 文档站点**
  - 完整的文档站点：https://llz162652.github.io/ChickenStack_doc/
  - API 文档（Python API、虚拟机 API、解析器 API）
  - 示例代码文档
  - 安装和使用指南
  - 问答部分

- **文档特性**
  - 响应式设计，自定义主题
  - 导航和侧边栏
  - 搜索功能
  - GitHub Pages 自动部署
  - 修复了指向文档仓库的编辑链接

### 📖 README 改进

- **双语支持**
  - 独立的英文（README.md）和中文（README_zh.md）版本
  - 语言切换链接
  - 遵循 GitHub 最佳实践

- **增强的视觉设计**
  - 项目徽章（Python 版本、许可证、状态、贡献者、Forks、Stars、Issues）
  - 快速导航链接
  - Mermaid 流程图（替代 ASCII 艺术）
  - 专业和现代的布局

- **新增部分**
  - AI 开发者致谢
  - 仓库状态图表
  - Star 历史图
  - 增强的功能描述

### 🔧 Bug 修复

- **README 404 链接**
  - 移除损坏的 shields.io 徽章
  - 替换为简单的文本链接
  - 所有链接现在正常工作

- **文档编辑链接**
  - 修复 editLink 配置
  - 正确指向 ChickenStack_doc 仓库
  - 移除错误的 `docs/` 路径前缀

- **GitHub Actions**
  - 修复部署分支配置（master → main）
  - 文档现在自动部署到 GitHub Pages

### 📦 项目结构

- **从主项目中移除 docs/**
  - 文档现在在单独的仓库中管理（ChickenStack_doc）
  - 将 `docs/` 添加到 `.gitignore`
  - 更清晰的主项目结构

- **测试组织**
  - 所有测试脚本在 `tests/` 目录中
  - 所有示例在 `examples/` 目录中
  - 结果存储在 `tests/results/`

### 🤝 贡献者

- **AI 开发者**：GLM-4.7
  - 代码生成
  - 测试和验证
  - 文档编写
  - 性能优化

- **人类开发者**：llz162652
  - 项目规划
  - 代码审查
  - 需求定义

### 📊 统计数据

- **修改文件数**：146 个文件
- **新增行数**：104,012 行
- **删除行数**：85 行
- **性能提升**：38.63%
- **测试覆盖**：400+ 测试用例
- **文档页面**：30+ 页

### 🔄 迁移说明

- 无破坏性更改
- 所有现有代码保持兼容
- 性能改进是透明的
- 新文档站点可用

### 📝 已知问题

无

### 🔮 未来计划

- JIT 编译优化
- Web 版解释器
- 更多语言绑定（JavaScript、Go）
- IDE 插件支持
- 在线代码编辑器

---

## v0.1.0 Alpha - 初始版本

- 基础指令集实现
- Python API 封装
- 核心解析器和虚拟机
- 简单示例
- 基础文档

---

**完整更新日志**：https://github.com/llz162652/ChickenStack/commits/main