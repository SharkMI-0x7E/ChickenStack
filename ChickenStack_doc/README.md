# ChickenStack 文档系统

ChickenStack 编程语言的官方文档系统，基于 VitePress 构建。

## 简介

这是 ChickenStack 语言的完整文档系统，包含：

- 入门指南：快速开始、安装、语法说明
- API 文档：Python API、解析器 API、虚拟机 API
- 示例代码：Hello World、阶乘、斐波那契等
- 参考文档：FAQ、版本信息、许可证

## 特性

- 响应式设计，支持桌面、平板、手机
- 深色模式
- 全文搜索
- 支持 Mermaid 图表与 LaTeX 数学公式

## 快速开始

### 环境要求

- Node.js 16.0 或更高版本
- npm 或 pnpm

### 安装依赖

```bash
npm install
```

或使用 pnpm：

```bash
pnpm install
```

### 启动开发服务器

```bash
npm run docs:dev
```

访问 http://localhost:5173 查看文档。

### 构建与预览

```bash
npm run docs:build
npm run docs:preview
```

## 目录结构

`ChickenStack_doc/` 即文档站根目录（现已移回主仓库）：

```
ChickenStack_doc/
├── .vitepress/     # VitePress 配置（config.mts、自定义主题）
├── guide/          # 入门指南（介绍、安装、语法、指令集、API 等）
├── examples/       # 示例代码说明
├── license/        # 许可证文档
├── manual/         # 手册
├── qa/             # 常见问题
├── changelog/      # 更新日志
├── public/         # 静态资源（图片、图标等）
├── about.md        # 关于
├── index.md        # 首页
├── package.json    # 依赖配置
└── README.md       # 本文件
```

## 技术栈

- VitePress：基于 Vue 3 的静态站点生成器
- Vue 3：渐进式 JavaScript 框架
- Mermaid：图表和可视化工具
- Markdown：文档格式

## 编写文档

所有文档使用 Markdown 格式，支持代码高亮、Mermaid 图表、数学公式与自定义组件。

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(20)
vm.op_add()
vm.op_print_num()  # 输出: 30
```

## 配置说明

配置文件位于 `.vitepress/config.mts`，可修改站点标题与描述、导航栏、侧边栏、主题与插件配置。

## 相关链接

- 主仓库：https://github.com/SharkMI-0x7E/ChickenStack
- 在线文档：https://SharkMI-0x7E.github.io/ChickenStack_doc/
- 问题反馈：https://github.com/SharkMI-0x7E/ChickenStack/issues

## 贡献

欢迎在主仓库提交 Issue 与 Pull Request。

## 许可证

MIT License - 详见 [LICENSE](../LICENSE) 文件
