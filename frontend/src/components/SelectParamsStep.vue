<template>
  <v-row>
    <v-col>
      <v-text-field
          v-model="testPercent"
          label="Процент тестовой выборки"
          required
      ></v-text-field>
    </v-col>
    <v-col>
        <v-text-field
          v-model="learningRate"
          label="Скорость обучения"
          required
      ></v-text-field>
    </v-col>
    <v-col>
        <v-text-field
            v-model="learningEpochs"
            label="Количество эпох"
            required
        ></v-text-field>
    </v-col>
  </v-row>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "SelectParamsStep",
  data: () => ({
    testPercent: 25.0,
    learningRate: 0.01,
    learningEpochs: 1000,
  }),
  methods: {
    ...mapActions({
      'setTestPercent': 'main/setTestPercent',
      'setLearningRate': 'main/setLearningRate',
      'setLearningEpochs': 'main/setLearningEpochs',
    })
  },
  watch: {
    testPercent: function(val) {
      this.setTestPercent(val);
    },
    learningRate: function(val) {
      this.setLearningRate(val);
    },
    learningEpochs: function(val) {
      this.setLearningEpochs(val);
    },
  }
}
</script>

<style scoped>

</style>
