<!-- 
  全局table组件，单头菜单，
  必传参数：表头数据columns，表格数据list
  支持溢出隐藏(overflow)，
  链接展示（isLink）使用链接展示时，需要传入linkFun方法，该方法返回点击该条数据，
  标签展示（isTag）使用标签时，该字段需要是一个对象，对象的code字段（1，2，3，其它）表示成功，危险，警告，默认，desc字段表示改字段的字符描述，
  固定表头（fixed）
  多选（isSelection）使用emits（handleSelectionChange）传递数据
 -->
<template>
  <div class="table-container">
    <el-table v-if="isReload" :stripe="stripe" :height="tableHeight" @selection-change="handleSelectionChange"
      v-loading="loading" :data="list" :border="true" fit>
      <el-table-column v-if="isSelection" align="center" type="selection" width="50">
      </el-table-column>
      <el-table-column v-if="isIndex" type="index" width="50" label="序号" align="center" :index="indexMethod">
      </el-table-column>
      <el-table-column v-for="(item, index) in columns" :key="index" :fixed="item.fixed" :align="item.align"
        :label="item.title" :width="item.width">
        <template #default="scope">
          <span v-if="item.dataIndex !== 'operate'">
            <el-button v-if="item.isLink" link type="primary" @click="linkFun(scope.row)">
              {{ scope.row[item.dataIndex] }}
            </el-button>
            <div v-else-if="item.overflow" style="max-width: 300px;">
              <el-tooltip effect="light" placement="top">
                <template #content>
                  <div style="max-width: 450px;">
                    {{ scope.row[item.dataIndex] }}
                  </div>
                </template>
                <span>{{ scope.row[item.dataIndex] }}</span>
              </el-tooltip>
            </div>
            <span v-else-if="item.isTag">
              <el-tag type="success" v-if="scope.row[item.dataIndex] && scope.row[item.dataIndex]['code'] === 1">
                {{ scope.row[item.dataIndex]['value'] }}
              </el-tag>
              <el-tag type="warning" v-else-if="scope.row[item.dataIndex] && scope.row[item.dataIndex]['code'] === 2">
                {{ scope.row[item.dataIndex]['value'] }}
              </el-tag>
              <el-tag type="danger" v-else-if="scope.row[item.dataIndex] && scope.row[item.dataIndex]['code'] === 3">
                {{ scope.row[item.dataIndex]['value'] }}
              </el-tag>
              <el-tag type="info" v-else-if="scope.row[item.dataIndex] && scope.row[item.dataIndex]['code'] === 4">
                {{ scope.row[item.dataIndex]['value'] }}
              </el-tag>
              <el-tag>
                {{ scope.row[item.dataIndex]['value'] }}
              </el-tag>
            </span>
            <span v-else>{{ scope.row[item.dataIndex] }} </span>
          </span>
          <template v-else>
            <slot :record="scope.row"></slot>
          </template>
        </template>
      </el-table-column>
    </el-table>
    <div :style="`height: ${tableHeight}px;`" class="toggleTableView" v-else>
      <el-icon class="icon">
        <Loading />
      </el-icon>
      <p class="text">
        系统视图切换，请稍候...
      </p>
    </div>
  </div>
</template>
<script lang="ts" setup>
/* eslint-disable */
import { PropType, ref, onMounted, onUnmounted } from 'vue';
const props = defineProps({
  columns: { //表头信息
    type: Array as PropType<any[]>,
    default: () => []

  },
  list: { //表格数据
    type: Array as PropType<any[]>,
    default: () => []
  },
  loading: { //是否使用loading
    type: Boolean,
    default: false
  },
  stripe: { //是否使用隔行变色
    type: Boolean,
    default: true
  },
  isSelection: { //是否显示多选框
    type: Boolean,
    default: false
  },
  isSetHeight: { //是否设置了表格高度
    type: Boolean,
    default: false
  },
  height: { //表格高度
    type: [Number, String],
    default: 0
  },
  isIndex: { //是否显示表格数据索引
    type: Boolean,
    default: false
  }
})
const emits = defineEmits(['linkFun', 'handleSelectionChange'])
let isReload = ref(true)
let tableHeight = ref(props.height)
onMounted(() => {
  if (!props.height) {
    tableHeight.value = window.innerHeight - 240
  }
})
let timer: null | any = null
let previousHeight: number = 0
const onResize = () => {
  var currentHeight = window.innerHeight;
  if (timer || currentHeight === previousHeight) return
  timer = setTimeout(() => {
    isReload.value = false
    let fullScreenTimer: null | any = null
    fullScreenTimer = setTimeout(() => {
      tableHeight.value = window.innerHeight - 240
      previousHeight = currentHeight
      isReload.value = true
      if (fullScreenTimer) {
        clearTimeout(fullScreenTimer)
      }
    }, 1000);
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  }, 500);
}
window.addEventListener("resize", onResize);
onUnmounted(() => {
  window.removeEventListener("resize", onResize)
})
const handleSelectionChange = (value: any) => {
  emits('handleSelectionChange', value)
}
const linkFun = (value: any) => {
  emits('linkFun', value)
}
const indexMethod = (index: number) => {
  return index + 1;
}

</script>
<style lang="less" scoped>
@keyframes rotate {
  to {
    transform: rotate(360deg);
  }
}

.toggleTableView {
  --el-table-border-color: var(--el-border-color-lighter);
  --el-table-border: 1px solid var(--el-table-border-color);
  border: var(--el-table-border);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  color: #409eff;

  .icon {
    animation: rotate 2s forwards infinite linear;
    font-size: 20px;
  }

  .text {
    padding-top: 10px;
  }
}
</style>