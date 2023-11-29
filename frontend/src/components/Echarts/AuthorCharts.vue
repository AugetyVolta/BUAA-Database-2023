<script lang="ts" setup>
import { onMounted, watch, computed, ref, PropType } from 'vue';
import * as echarts from 'echarts';
import { useMainStore } from '@/store/index';
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
const mainStore = useMainStore()
let dark = computed(() => mainStore.isDark)
watch(dark, (_, next) => {
  initCharts(next)
});
let myChart: any;
let lineCharts = ref<HTMLElement | null>();
const initCharts = (isDark: boolean) => {
  type EChartsOption = echarts.EChartsOption;
  const chartsTheme = isDark ? "light" : "dark";
  if (myChart) {
    myChart.dispose()
  }

  myChart = echarts.init(lineCharts.value, chartsTheme);
  var option: EChartsOption;
  option = {
    title: {
      text: '朝代作者数量统计（个）',
      top: 10,
      left: 10,
    },
    tooltip: {
      trigger: 'axis',
      formatter(params: any) {
        return `
        朝代：${params[0].name} </br> 
        作者数量：${params[0].value}个
        `;
      },
      axisPointer: {
        type: 'shadow',
      },
    },
    // grid: {
    //   left: '20',
    //   right: '20',
    //   bottom: '10',
    //   containLabel: true
    // },
    xAxis: {
      type: 'category',
      data: props.category,
      // axisLabel: {
      //   formatter: function (params) {
      //     let maxLen = 8
      //     if (params.length > maxLen) {
      //       let val = params.substr(0, maxLen) + '...';
      //       return val;
      //     } else {
      //       return params;
      //     }
      //   },
      //   interval: 0,
      //   // rotate: 45
      // },
      axisTick: {
        show: false
      },
      axisLine: {
        show: false
      },
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: props.countData,
        type: 'bar',
        barWidth: "30",
        name: "作者总量",
        label: {
          show: true,
          position: 'top',
          formatter: '{c}',
        },
        itemStyle: {
          // borderType: 'solid',
          // borderColor: '#fff',
          // shadowColor: '#fff',
        },
      }
    ]
  }



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