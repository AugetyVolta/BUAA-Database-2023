<script lang="ts" setup>
import { onMounted, watch, computed, ref, PropType } from 'vue';
import * as echarts from 'echarts';
import { useMainStore } from '@/store/index';
const props = defineProps({
  countData: { //表格数据
    type: Array as PropType<any[]>,
    default: () => []
  },
  category: {
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
      text: '作者文章总量统计（篇）',
      subtext: '因数量过大，本数据已去除数量小于2的作者',
      top: 10,
      left: 10,
    },
    tooltip: {
      trigger: 'axis',
      formatter(params: any) {
        return `
        作者姓名：${params[0].name} </br> 
        文章数量：${params[0].value}篇
        `;
      },
      axisPointer: {
        type: 'shadow',
      },
    },
    grid: {
      left: '5%',
      right: '5%',
      top: '0.7%',
      bottom: "0.1%",
      containLabel: true
    },
    xAxis: {
      type: 'value',
      show: true,
    },
    yAxis: {
      type: 'category',
      data: props.category
    },
    series: [
      {
        name: '作文总数',
        type: 'bar',
        label: {
          show: true,
          position: 'right',
          formatter: '{c}',
        },
        itemStyle: {
          color: '#0dbc79'
        },
        data: props.countData,
      },

    ]
  };
  option && myChart.setOption(option);
}
onMounted(() => {
  initCharts(!mainStore.isDark)
})

</script>
<template>
  <div ref="pieCharts" style="height: 12000px;width: 100%;background-color: white;" id="main"></div>
</template>
<style lang='less' scoped></style>