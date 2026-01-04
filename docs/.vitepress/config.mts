import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/ChickenStack_doc/',
  ignoreDeadLinks: true,
  title: 'ChickenStack',
  description: '基于栈的图灵完备编程语言',
  
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '快速开始', link: '/guide/navigation' },
      { text: '关于', link: '/about/' },
      { text: '许可证', link: '/license/' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: '快速开始',
          collapsed: false,
          items: [
            { text: '页面导航', link: '/guide/navigation' },
            { text: '什么是 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '安装', link: '/guide/installation' }
          ]
        },
        {
          text: '使用指南',
          collapsed: true,
          items: [
            { text: '运行方式', link: '/guide/running' },
            { text: '指令集', link: '/guide/instruction-set' },
            { text: '栈操作', link: '/guide/stack-operations' },
            { text: '语法', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 文档',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '虚拟机 API', link: '/guide/vm-api' },
            { text: '解析器 API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '示例',
          collapsed: false,
          items: [
            {
              text: '基础示例',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '数学运算', link: '/examples/math' },
                { text: '栈操作', link: '/examples/stack' }
              ]
            },
            {
              text: '进阶示例',
              collapsed: false,
              items: [
                { text: '循环', link: '/examples/loops' },
                { text: '斐波那契数列', link: '/examples/fibonacci' },
                { text: '阶乘', link: '/examples/factorial' },
                { text: '字符串反转', link: '/examples/reverse-string' },
                { text: '求和', link: '/examples/sum' },
                { text: '乘法表', link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '其他示例',
              collapsed: false,
              items: [
                { text: '字符操作', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '常见问题', link: '/qa/' }
          ]
        },
        {
          text: '更新日志',
          link: '/changelog/'
        }
      ],
      '/examples/': [
        {
          text: '快速开始',
          collapsed: false,
          items: [
            { text: '页面导航', link: '/guide/navigation' },
            { text: '什么是 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '安装', link: '/guide/installation' }
          ]
        },
        {
          text: '使用指南',
          collapsed: true,
          items: [
            { text: '运行方式', link: '/guide/running' },
            { text: '指令集', link: '/guide/instruction-set' },
            { text: '栈操作', link: '/guide/stack-operations' },
            { text: '语法', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 文档',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '虚拟机 API', link: '/guide/vm-api' },
            { text: '解析器 API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '示例',
          collapsed: false,
          items: [
            {
              text: '基础示例',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '数学运算', link: '/examples/math' },
                { text: '栈操作', link: '/examples/stack' }
              ]
            },
            {
              text: '进阶示例',
              collapsed: false,
              items: [
                { text: '循环', link: '/examples/loops' },
                { text: '斐波那契数列', link: '/examples/fibonacci' },
                { text: '阶乘', link: '/examples/factorial' },
                { text: '字符串反转', link: '/examples/reverse-string' },
                { text: '求和', link: '/examples/sum' },
                { text: '乘法表', link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '其他示例',
              collapsed: false,
              items: [
                { text: '字符操作', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '常见问题', link: '/qa/' }
          ]
        },
        {
          text: '更新日志',
          link: '/changelog/'
        }
      ],
      '/changelog/': [
        {
          text: '快速开始',
          collapsed: false,
          items: [
            { text: '页面导航', link: '/guide/navigation' },
            { text: '什么是 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '安装', link: '/guide/installation' }
          ]
        },
        {
          text: '使用指南',
          collapsed: true,
          items: [
            { text: '运行方式', link: '/guide/running' },
            { text: '指令集', link: '/guide/instruction-set' },
            { text: '栈操作', link: '/guide/stack-operations' },
            { text: '语法', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 文档',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '虚拟机 API', link: '/guide/vm-api' },
            { text: '解析器 API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '示例',
          collapsed: false,
          items: [
            {
              text: '基础示例',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '数学运算', link: '/examples/math' },
                { text: '栈操作', link: '/examples/stack' }
              ]
            },
            {
              text: '进阶示例',
              collapsed: false,
              items: [
                { text: '循环', link: '/examples/loops' },
                { text: '斐波那契数列', link: '/examples/fibonacci' },
                { text: '阶乘', link: '/examples/factorial' },
                { text: '字符串反转', link: '/examples/reverse-string' },
                { text: '求和', link: '/examples/sum' },
                { text: '乘法表', link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '其他示例',
              collapsed: false,
              items: [
                { text: '字符操作', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '常见问题', link: '/qa/' }
          ]
        },
        {
          text: '更新日志',
          link: '/changelog/'
        }
      ],
      '/license/': [
        {
          text: '快速开始',
          collapsed: false,
          items: [
            { text: '页面导航', link: '/guide/navigation' },
            { text: '什么是 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '安装', link: '/guide/installation' }
          ]
        },
        {
          text: '使用指南',
          collapsed: true,
          items: [
            { text: '运行方式', link: '/guide/running' },
            { text: '指令集', link: '/guide/instruction-set' },
            { text: '栈操作', link: '/guide/stack-operations' },
            { text: '语法', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 文档',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '虚拟机 API', link: '/guide/vm-api' },
            { text: '解析器 API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '示例',
          collapsed: false,
          items: [
            {
              text: '基础示例',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '数学运算', link: '/examples/math' },
                { text: '栈操作', link: '/examples/stack' }
              ]
            },
            {
              text: '进阶示例',
              collapsed: false,
              items: [
                { text: '循环', link: '/examples/loops' },
                { text: '斐波那契数列', link: '/examples/fibonacci' },
                { text: '阶乘', link: '/examples/factorial' },
                { text: '字符串反转', link: '/examples/reverse-string' },
                { text: '求和', link: '/examples/sum' },
                { text: '乘法表', link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '其他示例',
              collapsed: false,
              items: [
                { text: '字符操作', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '常见问题', link: '/qa/' }
          ]
        },
        {
          text: '更新日志',
          link: '/changelog/'
        }
      ],
      '/qa/': [
        {
          text: '快速开始',
          collapsed: false,
          items: [
            { text: '页面导航', link: '/guide/navigation' },
            { text: '什么是 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '安装', link: '/guide/installation' }
          ]
        },
        {
          text: '使用指南',
          collapsed: true,
          items: [
            { text: '运行方式', link: '/guide/running' },
            { text: '指令集', link: '/guide/instruction-set' },
            { text: '栈操作', link: '/guide/stack-operations' },
            { text: '语法', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 文档',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '虚拟机 API', link: '/guide/vm-api' },
            { text: '解析器 API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '示例',
          collapsed: false,
          items: [
            {
              text: '基础示例',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '数学运算', link: '/examples/math' },
                { text: '栈操作', link: '/examples/stack' }
              ]
            },
            {
              text: '进阶示例',
              collapsed: false,
              items: [
                { text: '循环', link: '/examples/loops' },
                { text: '斐波那契数列', link: '/examples/fibonacci' },
                { text: '阶乘', link: '/examples/factorial' },
                { text: '字符串反转', link: '/examples/reverse-string' },
                { text: '求和', link: '/examples/sum' },
                { text: '乘法表', link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '其他示例',
              collapsed: false,
              items: [
                { text: '字符操作', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: false,
          items: [
            { text: '常见问题', link: '/qa/' }
          ]
        },
        {
          text: '更新日志',
          link: '/changelog/'
        }
      ]
    },

    editLink: {
      pattern: 'https://github.com/llz162652/ChickenStack_doc/edit/main/:path',
      text: '在 GitHub 上编辑此页面'
    },

    docFooter: {
      prev: '上一页',
      next: '下一页'
    },

    outline: {
      label: '页面导航'
    },

    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/llz162652/ChickenStack' }
    ],

    footer: {
      message: 'MIT Licensed | Copyright © 2025-Present',
      copyright: 'Powered by AI GLM-4.7 | Built with <a href="https://vitepress.dev/" target="_blank">VitePress</a>'
    }
  }
})

