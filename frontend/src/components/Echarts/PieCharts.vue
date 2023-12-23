<script lang="ts" setup>
import { onMounted, watch, computed, ref, PropType } from 'vue';
import * as echarts from 'echarts';
import { useMainStore } from '@/store/index';
const props = defineProps({
  countData: { //表格数据
    type: Array as PropType<any[]>,
    default: () => []
  },
})
const mainStore = useMainStore()
let dark = computed(() => mainStore.isDark)
watch(dark, (_, next) => {
  initCharts(next)
});
let myChart: any;
let pieCharts = ref<HTMLElement | null>();

const initCharts = (isDark: boolean) => {
  type EChartsOption = echarts.EChartsOption;
  const chartsTheme = isDark ? "light" : "dark";
  if (myChart) {
    myChart.dispose()
  }
  myChart = echarts.init(pieCharts.value, chartsTheme);
  var option: EChartsOption;
  option = {
    title: {
    text: '用户年龄饼图',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: '50%',
      // data: [
      //   { value: 1048, name: 'Search Engine' },
      //   { value: 735, name: 'Direct' },
      //   { value: 580, name: 'Email' },
      //   { value: 484, name: 'Union Ads' },
      //   { value: 300, name: 'Video Ads' }
      // ],
      data: props.countData,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
  };
  option && myChart.setOption(option);
}
onMounted(() => {
  setTimeout(() => {
           initCharts(!mainStore.isDark)
        }, 1000)
})



</script>
<template>
  <div ref="pieCharts" style="height: 100%;width: 100%;background-color: white;" id="main"></div>
</template>
<style lang='less' scoped></style>