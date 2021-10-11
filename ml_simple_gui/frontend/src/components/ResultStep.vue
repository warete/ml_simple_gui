<template>
  <v-row>
    <v-col cols="12">
      <div v-if="resultLoading">
        <v-alert
          border="left"
          color="indigo"
          dark
        >
          Идет загрузка данных
        </v-alert>
        <v-skeleton-loader
            type="list-item-three-line, list-item-three-line, image, actions"
        ></v-skeleton-loader>
      </div>
      <template
          v-else
      >
        <v-simple-table>
          <template v-slot:default>
            <thead>
            <tr>
              <th class="text-left">
                Параметр
              </th>
              <th class="text-left">
                Результат
              </th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="metric in formattedMetrics"
                :key="metric.code"
            >
              <td>{{ metric.name }}</td>
              <td>
                <div v-html="metric.result"/>
              </td>
            </tr>
            </tbody>
          </template>
        </v-simple-table>
      </template>
    </v-col>
  </v-row>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import {map, isArray, isString, isObject} from 'lodash';

export default {
  name: "ResultStep",
  props: ['isOpened'],
  methods: {
    ...mapActions({
      'fetchResults': 'main/fetchResults',
    }),
  },
  computed: {
    ...mapGetters({
      'trainTestDataFile': 'main/trainTestDataFile',
      'learningEpochs': 'main/learningEpochs',
      'modelParams': 'main/modelParams',
      'metrics': 'main/result',
      'resultLoading': 'main/resultLoading',
    }),
    formattedMetrics() {
      return map(this.metrics, metric => {
        if (isString(metric.result)) {
          return metric;
        }
        if (isArray(metric.result)) {
          return {...metric, result: metric.result.join(', ')};
        }
        if (isObject(metric.result)) {
          return {
            ...metric,
            result: [...map(metric.result, (metricItem, metricItemKey) => `${metricItemKey}: ${metricItem}`)].join('<br>')
          };
        }
      })
    }
  },
  watch: {
    isOpened: function (val) {
      if (val) {
        this.fetchResults({
          file: this.trainTestDataFile,
          modelParams: this.modelParams,
        });
      }
    },
  },
}
</script>

<style scoped>

</style>
