import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import NCard from './components/NCard.vue'
import './style.css'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: Layout,
  enhanceApp({ app }) {
    app.component('NCard', NCard)
  }
}