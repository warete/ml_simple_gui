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
              <th class="text-center">
                Результат
              </th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="metric in sortedMetrics"
                :key="metric.code"
            >
              <td>{{ metric.name }}</td>
              <td class="text-center">
                <div v-if="metric.result_type == 'scalar'">
                  {{ metric.result }}
                </div>
                <div v-else-if="metric.result_type == 'image'">
                  <img :src="metric.result">
                </div>
                <v-simple-table v-else-if="metric.result_type == 'table'">
                  <template v-slot:default>
                    <tbody>
                    <tr v-for="(val, key) in metric.result" :key="key">
                      <td>{{ key }}</td>
                      <td>{{ val }}</td>
                    </tr>
                    </tbody>
                  </template>
                </v-simple-table>
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
import {sortBy} from 'lodash';

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
    sortedMetrics: function () {
      return sortBy(this.metrics, ['result_type'])
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
