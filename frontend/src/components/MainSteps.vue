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
                    {{step.name}}
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
                    {{step.content}}
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

    export default {
        name: "MainSteps",
        data() {
            return {
                mainStepperProgress: 1,
                steps: {
                    1: {
                        id: 'loadFile',
                        name: 'Загрузка данных',
                        content: '',
                    },
                    2: {
                        id: 'selectFields',
                        name: 'Определение параметров в выборке',
                        content: '',
                    },
                    3: {
                        id: 'selectParams',
                        name: 'Настройка параметров модели',
                        content: '',
                    },
                    4: {
                        id: 'results',
                        name: 'Результаты',
                        content: '',
                    },
                },
            }
        },
        computed: {
            maxStepNumber() {
                return last(Object.keys(this.steps));
            },
            minStepNumber() {
                return first(Object.keys(this.steps));
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