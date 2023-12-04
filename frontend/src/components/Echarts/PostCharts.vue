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



</script>