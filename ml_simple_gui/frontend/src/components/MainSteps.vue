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
                    <component 
                    :is="step.component" 
                    :is-opened="mainStepperProgress === Number(stepNumber)" 
                    v-bind="step.propsData"
                    v-on:next-step="nextStep"
                    v-on:next-step-number="onSetNextStepNumber"
                    v-on:prev-step-number="onSetPrevStepNumber"
                    ></component>
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
    import {last, first, isNumber} from 'lodash';
    import UploadFilesStep from "./UploadFilesStep";
    import SelectParamsStep from "./SelectParamsStep";
    import ResultStep from "./ResultStep";
    import PredictResultsStep from "./PredictResultsStep";
    import SelectModelStep from "./SelectModelStep";
    import {mapGetters} from "vuex";    
    import {TYPE_SET_TRAIN_TEST_FILE, TYPE_SET_PREDICT_FILE} from '../store/modules/main';

    export default {
        name: "MainSteps",
        components: {UploadFilesStep, SelectParamsStep, ResultStep, PredictResultsStep, SelectModelStep},
        data() {
            return {            
                mainStepperProgress: 1,
                nextStepFromChild: null,
                prevStepFromChild: null,
                steps: {
                    1: {
                        id: 'selectModel',
                        name: 'Выбор действия',
                        component: 'select-model-step',
                        propsData: {}
                    },
                    2: {
                        id: 'loadFile',
                        name: 'Загрузка данных',
                        component: 'upload-files-step',
                        propsData: {type: TYPE_SET_TRAIN_TEST_FILE}
                    },
                    3: {
                        id: 'selectParams',
                        name: 'Настройка параметров модели',
                        component: 'select-params-step',
                        propsData: {}
                    },
                    4: {
                        id: 'results',
                        name: 'Результаты',
                        component: 'result-step',
                        propsData: {}
                    },
                    5: {
                        id: 'loadFileForPredict',
                        name: 'Загрузка данных для моделирования',
                        component: 'upload-files-step',
                        propsData: {type: TYPE_SET_PREDICT_FILE}
                    },
                    6: {
                        id: 'predictResults',
                        name: 'Результаты моделирования',
                        component: 'predict-results-step',
                        propsData: {}
                    },
                },
            }
        },
        computed: {
            ...mapGetters({
                'isTrainTestDataFileValid': 'main/isTrainTestDataFileValid',
                'isPredictDataFileValid': 'main/isPredictDataFileValid',
                'isSelectedModelValid': 'main/isSelectedModelValid',
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
                return this.isPredictDataFileValid;
            },
            resultsValid() {
                return true;
            },
            selectModelValid() {
                return this.isSelectedModelValid;
            },
        },
        methods: {
            nextStep() {
                if (isNumber(this.nextStepFromChild)) {
                    this.mainStepperProgress = this.nextStepFromChild;
                    this.nextStepFromChild = null;
                } else {
                    this.mainStepperProgress++;
                }
            },
            previousStep() {
                if (isNumber(this.prevStepFromChild)) {
                    this.mainStepperProgress = this.prevStepFromChild;
                    this.prevStepFromChild = null;
                } else {
                    this.mainStepperProgress--;
                }
            },
            onSetNextStepNumber(stepNumber) {
                this.nextStepFromChild = stepNumber;
            },
            onSetPrevStepNumber(stepNumber) {
                this.prevStepFromChild = stepNumber;
            },
        }
    }
</script>

<style scoped>

</style>
