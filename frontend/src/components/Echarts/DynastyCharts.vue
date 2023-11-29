<script lang="ts" setup>
import { onMounted, watch, computed, ref, PropType } from 'vue';
import * as echarts from 'echarts';
import { useMainStore } from '@/store/index';
const mainStore = useMainStore()
const props = defineProps({
  countData: { //表格数据
    type: Array as PropType<any[]>,
    default: () => []
  },
  category: { //表格数据
    type: Array as PropType<any[]>,
    default: () => []
  },
})
let dark = computed(() => mainStore.isDark)
watch(dark, (_, next) => {
  initCharts(next)
});
let myChart: any;
let lineCharts = ref<HTMLElement | null>();
const initCharts = (isDark: boolean) => {
  type EChartsOption = echarts.EChartsOption;
  let option: EChartsOption;
  const chartsTheme = isDark ? "light" : "dark";
  if (myChart) {
    myChart.dispose()
  }

  myChart = echarts.init(lineCharts.value, chartsTheme);

  // option
  option = {
    title: {
      text: '朝代文章总量统计（篇）',
      top: 10,
      left: 10,
    },
    tooltip: {
      trigger: 'axis',
      formatter(params: any) {
        return `
        朝代：${params[0].name} </br> 
        文章总量：${params[0].value}篇
        `;
      },
      axisPointer: {
        type: 'shadow',
      },
    },
    toolbox: {
      show: true,
      orient: 'horizontal',
      right: '25',
      top: 'top',
      feature: {
        mark: { show: true },
        // dataView: { show: true, readOnly: false },
        magicType: { show: true, type: ['line', 'bar'] },
        // restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    xAxis: {
      data: props.category,
      axisLine: {
        lineStyle: {
          color: '#ccc'
        }
      },
      splitLine: { show: false },
    },
    yAxis: {
      axisLine: {
        lineStyle: {
          color: '#ccc'
        }
      }
    },
    series: [
      {
        name: '文章总量',
        type: 'bar',
        barWidth: 10,
        itemStyle: {
          borderRadius: 5,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#14c8d4' },
            { offset: 1, color: '#43eec6' }
          ])
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}',
        },
        animationDuration: 3000,
        data: props.countData
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
  <div ref="lineCharts" style="height: 100%;width: 100%;background-color: white;" id="main">

  </div>
</template>
<style lang='less' scoped></style>