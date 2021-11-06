<template>
    <v-stepper v-model="mainStepperProgress">
        <v-stepper-header>
            <template
                    v-for="(step, stepNumber) in steps"
            >
                <v-stepper-step
                        :key="`${step.id}-step`"
                        :complete="mainStepperProgress > stepNumber"
                        :step="stepNumber"
                >
                    {{ step.name }}
                    <v-divider></v-divider>
                </v-stepper-step>
                <v-divider :key="`${step.id}-divider`"></v-divider>
            </template>

        </v-stepper-header>

        <v-stepper-items>
            <v-stepper-content v-for="(step, stepNumber) in steps" :key="step.id" :step="stepNumber">
                <v-card
                        class="mb-12"
                >
                    <component :is="step.component" :is-opened="mainStepperProgress === Number(stepNumber)" v-bind="step.propsData"></component>
                </v-card>

                <v-row justify="space-between">
                    <v-col class="my-1">
                        <v-btn
                                v-if="stepNumber > minStepNumber"
                                @click="previousStep">
                            Назад
                        </v-btn>
                    </v-col>
                    <v-col class="text-end my-1">
                        <v-btn
                                v-if="stepNumber < maxStepNumber"
                                color="primary"
                                :disabled="isNextButtonDisabled"
                                @click="nextStep"
                        >
                            Вперед
                        </v-btn>
                    </v-col>
                </v-row>
            </v-stepper-content>
        </v-stepper-items>
    </v-stepper>
</template>

<script>
    import {last, first} from 'lodash';
    import UploadFilesStep from "./UploadFilesStep";
    import SelectParamsStep from "./SelectParamsStep";
    import ResultStep from "./ResultStep";
    import {mapGetters} from "vuex";    
    import {TYPE_SET_TRAIN_TEST_FILE, TYPE_SET_PREDICT_FILE} from '../store/modules/main';

    export default {
        name: "MainSteps",
        components: {UploadFilesStep, SelectParamsStep, ResultStep},
        data() {
            return {                
                mainStepperProgress: 1,
                steps: {
                    1: {
                        id: 'loadFile',
                        name: 'Загрузка данных',
                        component: 'upload-files-step',
                        propsData: {type: TYPE_SET_TRAIN_TEST_FILE}
                    },
                    2: {
                        id: 'selectParams',
                        name: 'Настройка параметров модели',
                        component: 'select-params-step',
                        propsData: {}
                    },
                    3: {
                        id: 'results',
                        name: 'Результаты',
                        component: 'result-step',
                        propsData: {}
                    },
                    4: {
                        id: 'loadFileForPredict',
                        name: 'Загрузка данных для получения проверки',
                        component: 'upload-files-step',
                        propsData: {type: TYPE_SET_PREDICT_FILE}
                    },
                    5: {
                        id: 'predictResults',
                        name: 'Результаты проверки',
                        component: 'result-step',
                        propsData: {}
                    },
                },
            }
        },
        computed: {
            ...mapGetters({
                'isTrainTestDataFileValid': 'main/isTrainTestDataFileValid',
            }),
            maxStepNumber() {
                return last(Object.keys(this.steps));
            },
            minStepNumber() {
                return first(Object.keys(this.steps));
            },
            isNextButtonDisabled() {
                return !this[`${this.steps[this.mainStepperProgress].id}Valid`];
            },
            //Методы для проверки доступности кнопки перехода к следующим шагам
            selectParamsValid() {
                return true;
            },
            loadFileValid() {
                return this.isTrainTestDataFileValid;
            },
            loadFileForPredictValid() {
                return this.isTrainTestDataFileValid;
            },
            resultsValid() {
                return true;
            },
        },
        methods: {
            nextStep() {
                this.mainStepperProgress++;
            },
            previousStep() {
                this.mainStepperProgress--;
            },
        }
    }
</script>

<style scoped>

</style>
