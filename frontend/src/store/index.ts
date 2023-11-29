import { ref, inject, nextTick, Ref } from 'vue'
import { defineStore } from 'pinia'
export const useMainStore = defineStore('main', () => {
  const theme = localStorage.getItem("vueuse-color-scheme")
  const isDark = ref<boolean>(theme === 'dark')

  function changeTheme(): void {

    isDark.value = !isDark.value
  }

  let isFullScreen = ref<boolean>(false)
  function toggleFullScreen(): void {
    isFullScreen.value = !isFullScreen.value
  }

  const isCollapse = ref<boolean>(false)
  /* eslint-disable */
  let reload = inject<Ref<boolean>>("reload");
  function reloadApp(): void {
    if (reload) {
      reload.value = false
    }
    nextTick(() => {
      if (reload) {
        reload.value = true
      }
    })
  }
  function onTrigger(): void {
    if (reload) {
      reload.value = false
    }
    nextTick(() => {
      if (reload) {
        reload.value = true
      }
    })
    isCollapse.value = !isCollapse.value
  }
  return { isDark, changeTheme, isCollapse, onTrigger, reloadApp, isFullScreen, toggleFullScreen }
})