import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/ChickenStack_doc/',
  title: 'ChickenStack',
  description: '鍩轰簬鏍堢殑鍥剧伒瀹屽缂栫▼璇█',
  ignoreDeadLinks: true,
  
  themeConfig: {
    nav: [
      { text: '棣栭〉', link: '/' },
      { text: '蹇€熷紑濮?, link: '/guide/navigation' },
      { text: '鍏充簬', link: '/about/' },
      { text: '璁稿彲璇?, link: '/license/' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: '蹇€熷紑濮?,
          collapsed: false,
          items: [
            { text: '椤甸潰瀵艰埅', link: '/guide/navigation' },
            { text: '浠€涔堟槸 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '瀹夎', link: '/guide/installation' }
          ]
        },
        {
          text: '浣跨敤鎸囧崡',
          collapsed: true,
          items: [
            { text: '杩愯鏂瑰紡', link: '/guide/running' },
            { text: '鎸囦护闆?, link: '/guide/instruction-set' },
            { text: '鏍堟搷浣?, link: '/guide/stack-operations' },
            { text: '璇硶', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 鏂囨。',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '铏氭嫙鏈?API', link: '/guide/vm-api' },
            { text: '瑙ｆ瀽鍣?API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '绀轰緥',
          collapsed: false,
          items: [
            {
              text: '鍩虹绀轰緥',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '鏁板杩愮畻', link: '/examples/math' },
                { text: '鏍堟搷浣?, link: '/examples/stack' }
              ]
            },
            {
              text: '杩涢樁绀轰緥',
              collapsed: false,
              items: [
                { text: '寰幆', link: '/examples/loops' },
                { text: '鏂愭尝閭ｅ鏁板垪', link: '/examples/fibonacci' },
                { text: '闃朵箻', link: '/examples/factorial' },
                { text: '瀛楃涓插弽杞?, link: '/examples/reverse-string' },
                { text: '姹傚拰', link: '/examples/sum' },
                { text: '涔樻硶琛?, link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '鍏朵粬绀轰緥',
              collapsed: false,
              items: [
                { text: '瀛楃鎿嶄綔', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '甯歌闂', link: '/qa/' }
          ]
        },
        {
          text: '鏇存柊鏃ュ織',
          link: '/changelog/'
        }
      ],
      '/examples/': [
        {
          text: '蹇€熷紑濮?,
          collapsed: false,
          items: [
            { text: '椤甸潰瀵艰埅', link: '/guide/navigation' },
            { text: '浠€涔堟槸 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '瀹夎', link: '/guide/installation' }
          ]
        },
        {
          text: '浣跨敤鎸囧崡',
          collapsed: true,
          items: [
            { text: '杩愯鏂瑰紡', link: '/guide/running' },
            { text: '鎸囦护闆?, link: '/guide/instruction-set' },
            { text: '鏍堟搷浣?, link: '/guide/stack-operations' },
            { text: '璇硶', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 鏂囨。',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '铏氭嫙鏈?API', link: '/guide/vm-api' },
            { text: '瑙ｆ瀽鍣?API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '绀轰緥',
          collapsed: false,
          items: [
            {
              text: '鍩虹绀轰緥',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '鏁板杩愮畻', link: '/examples/math' },
                { text: '鏍堟搷浣?, link: '/examples/stack' }
              ]
            },
            {
              text: '杩涢樁绀轰緥',
              collapsed: false,
              items: [
                { text: '寰幆', link: '/examples/loops' },
                { text: '鏂愭尝閭ｅ鏁板垪', link: '/examples/fibonacci' },
                { text: '闃朵箻', link: '/examples/factorial' },
                { text: '瀛楃涓插弽杞?, link: '/examples/reverse-string' },
                { text: '姹傚拰', link: '/examples/sum' },
                { text: '涔樻硶琛?, link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '鍏朵粬绀轰緥',
              collapsed: false,
              items: [
                { text: '瀛楃鎿嶄綔', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '甯歌闂', link: '/qa/' }
          ]
        },
        {
          text: '鏇存柊鏃ュ織',
          link: '/changelog/'
        }
      ],
      '/changelog/': [
        {
          text: '蹇€熷紑濮?,
          collapsed: false,
          items: [
            { text: '椤甸潰瀵艰埅', link: '/guide/navigation' },
            { text: '浠€涔堟槸 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '瀹夎', link: '/guide/installation' }
          ]
        },
        {
          text: '浣跨敤鎸囧崡',
          collapsed: true,
          items: [
            { text: '杩愯鏂瑰紡', link: '/guide/running' },
            { text: '鎸囦护闆?, link: '/guide/instruction-set' },
            { text: '鏍堟搷浣?, link: '/guide/stack-operations' },
            { text: '璇硶', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 鏂囨。',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '铏氭嫙鏈?API', link: '/guide/vm-api' },
            { text: '瑙ｆ瀽鍣?API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '绀轰緥',
          collapsed: false,
          items: [
            {
              text: '鍩虹绀轰緥',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '鏁板杩愮畻', link: '/examples/math' },
                { text: '鏍堟搷浣?, link: '/examples/stack' }
              ]
            },
            {
              text: '杩涢樁绀轰緥',
              collapsed: false,
              items: [
                { text: '寰幆', link: '/examples/loops' },
                { text: '鏂愭尝閭ｅ鏁板垪', link: '/examples/fibonacci' },
                { text: '闃朵箻', link: '/examples/factorial' },
                { text: '瀛楃涓插弽杞?, link: '/examples/reverse-string' },
                { text: '姹傚拰', link: '/examples/sum' },
                { text: '涔樻硶琛?, link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '鍏朵粬绀轰緥',
              collapsed: false,
              items: [
                { text: '瀛楃鎿嶄綔', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '甯歌闂', link: '/qa/' }
          ]
        },
        {
          text: '鏇存柊鏃ュ織',
          link: '/changelog/'
        }
      ],
      '/license/': [
        {
          text: '蹇€熷紑濮?,
          collapsed: false,
          items: [
            { text: '椤甸潰瀵艰埅', link: '/guide/navigation' },
            { text: '浠€涔堟槸 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '瀹夎', link: '/guide/installation' }
          ]
        },
        {
          text: '浣跨敤鎸囧崡',
          collapsed: true,
          items: [
            { text: '杩愯鏂瑰紡', link: '/guide/running' },
            { text: '鎸囦护闆?, link: '/guide/instruction-set' },
            { text: '鏍堟搷浣?, link: '/guide/stack-operations' },
            { text: '璇硶', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 鏂囨。',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '铏氭嫙鏈?API', link: '/guide/vm-api' },
            { text: '瑙ｆ瀽鍣?API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '绀轰緥',
          collapsed: false,
          items: [
            {
              text: '鍩虹绀轰緥',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '鏁板杩愮畻', link: '/examples/math' },
                { text: '鏍堟搷浣?, link: '/examples/stack' }
              ]
            },
            {
              text: '杩涢樁绀轰緥',
              collapsed: false,
              items: [
                { text: '寰幆', link: '/examples/loops' },
                { text: '鏂愭尝閭ｅ鏁板垪', link: '/examples/fibonacci' },
                { text: '闃朵箻', link: '/examples/factorial' },
                { text: '瀛楃涓插弽杞?, link: '/examples/reverse-string' },
                { text: '姹傚拰', link: '/examples/sum' },
                { text: '涔樻硶琛?, link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '鍏朵粬绀轰緥',
              collapsed: false,
              items: [
                { text: '瀛楃鎿嶄綔', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: true,
          items: [
            { text: '甯歌闂', link: '/qa/' }
          ]
        },
        {
          text: '鏇存柊鏃ュ織',
          link: '/changelog/'
        }
      ],
      '/qa/': [
        {
          text: '蹇€熷紑濮?,
          collapsed: false,
          items: [
            { text: '椤甸潰瀵艰埅', link: '/guide/navigation' },
            { text: '浠€涔堟槸 ChickenStack', link: '/guide/what-is-chickenstack' },
            { text: '瀹夎', link: '/guide/installation' }
          ]
        },
        {
          text: '浣跨敤鎸囧崡',
          collapsed: true,
          items: [
            { text: '杩愯鏂瑰紡', link: '/guide/running' },
            { text: '鎸囦护闆?, link: '/guide/instruction-set' },
            { text: '鏍堟搷浣?, link: '/guide/stack-operations' },
            { text: '璇硶', link: '/guide/syntax' }
          ]
        },
        {
          text: 'API 鏂囨。',
          collapsed: true,
          items: [
            { text: 'Python API', link: '/guide/python-api' },
            { text: '铏氭嫙鏈?API', link: '/guide/vm-api' },
            { text: '瑙ｆ瀽鍣?API', link: '/guide/parser-api' }
          ]
        },
        {
          text: '绀轰緥',
          collapsed: false,
          items: [
            {
              text: '鍩虹绀轰緥',
              collapsed: false,
              items: [
                { text: 'Hello World', link: '/examples/hello-world' },
                { text: '鏁板杩愮畻', link: '/examples/math' },
                { text: '鏍堟搷浣?, link: '/examples/stack' }
              ]
            },
            {
              text: '杩涢樁绀轰緥',
              collapsed: false,
              items: [
                { text: '寰幆', link: '/examples/loops' },
                { text: '鏂愭尝閭ｅ鏁板垪', link: '/examples/fibonacci' },
                { text: '闃朵箻', link: '/examples/factorial' },
                { text: '瀛楃涓插弽杞?, link: '/examples/reverse-string' },
                { text: '姹傚拰', link: '/examples/sum' },
                { text: '涔樻硶琛?, link: '/examples/multiplication-table' }
              ]
            },
            {
              text: '鍏朵粬绀轰緥',
              collapsed: false,
              items: [
                { text: '瀛楃鎿嶄綔', link: '/examples/char-operations' }
              ]
            }
          ]
        },
        {
          text: 'Q&A',
          collapsed: false,
          items: [
            { text: '甯歌闂', link: '/qa/' }
          ]
        },
        {
          text: '鏇存柊鏃ュ織',
          link: '/changelog/'
        }
      ]
    },

    editLink: {
      pattern: 'https://github.com/llz162652/ChickenStack/edit/main/docs/:path',
      text: '鍦?GitHub 涓婄紪杈戞椤甸潰'
    },

    docFooter: {
      prev: '涓婁竴椤?,
      next: '涓嬩竴椤?
    },

    outline: {
      label: '椤甸潰瀵艰埅'
    },

    lastUpdated: {
      text: '鏈€鍚庢洿鏂颁簬',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/llz162652/ChickenStack' }
    ],

    footer: {
      message: 'MIT Licensed | Copyright 漏 2025-Present',
      copyright: 'Powered by AI GLM-4.7 | Built with <a href="https://vitepress.dev/" target="_blank">VitePress</a>'
    }
  }
})
