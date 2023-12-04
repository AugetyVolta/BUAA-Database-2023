<script lang="ts" setup>
import { onMounted, watch, computed, ref, PropType } from 'vue';
import * as echarts from 'echarts';
import { useMainStore } from '@/store/index';
import {useRoute, useRouter} from "vue-router";
import {getIdOfBook} from "@/apis/home";
const router = useRouter()
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
const linkFun = (id) => {
  router.push({path: '/library/books/book', query: {id: id}})
}
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
  myChart.on('click', async (params: any) => {
    const bookName = params.name;
    //console.log(params.data);
    const data = await getIdOfBook({"bookName": bookName});
    //console.log(data)
    linkFun(data.data.data)
  });
  // option
  option = {
    title: {
      text: '十佳图书榜',
      top: 10,
      left: 10,
    },
    tooltip: {
      trigger: 'axis',
      formatter(params: any) {
        return `
        书名：${params[0].name} </br>
        综合评分：${params[0].value}
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