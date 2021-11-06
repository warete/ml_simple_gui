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
        Результат можно получить по ссылке <a :href="`${apiDomain}/${predictResult.filePath}`" target="_blank">{{ `${apiDomain}/${predictResult.filePath}` }}</a>
      </template>
    </v-col>
  </v-row>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import {API_DOMAIN} from "@/constants";

export default {
  name: "PredictResultsStep",
  props: ['isOpened'],
  data() {
      return {
          apiDomain: API_DOMAIN
      }
  },
  methods: {
    ...mapActions({
      'fetchResults': 'main/fetchPredictResults',
      'resetPredictResult': 'main/resetPredictResult',
    }),
  },
  computed: {
    ...mapGetters({
      'predictDataFile': 'main/predictDataFile',
      'predictResult': 'main/predictResult',
      'resultLoading': 'main/predictResultLoading',
    })
  },
  watch: {
    isOpened: function (val) {
      if (val) {
        this.resetPredictResult();
        this.fetchResults({
          file: this.predictDataFile,
        });
      }
    },
  },
}
</script>

<style scoped>

</style>
