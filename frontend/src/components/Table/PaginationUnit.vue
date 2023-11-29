<!-- 
  分页组件
 -->
<template>
  <div class="pagination-container">
    <el-pagination style="justify-content: center;" background :disabled="total === 0 ? true : false"
      @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40, 50]" layout="total, sizes, prev, pager, next, jumper" :total="total">
    </el-pagination>
  </div>
</template>
<script lang="ts" setup>
defineProps({
  currentPage: { //当前页码
    type: Number,
    default: 1,
  },
  total: { //数据总量
    type: Number,
    default: 0,
  }
})
const emits = defineEmits(['handleSizeChange', 'handleCurrentChange'])
const handleSizeChange = (value: number) => {
  emits("handleSizeChange", value)
}
const handleCurrentChange = (value: number) => {
  emits("handleCurrentChange", value)
}
</script>
<style lang="less" scoped>
.pagination-container {
  padding: 8px 0;
  --el-table-bg-color: var(--el-fill-color-blank);
  background-color: var(--el-table-bg-color);
  --el-table-border-color: var(--el-border-color-lighter);
  --el-table-border: 1px solid var(--el-table-border-color);
  border: var(--el-table-border);
}
</style>