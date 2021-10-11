import axios from "axios";
import {API_DOMAIN} from "@/constants";
import Vue from 'vue';
import {keyBy, get} from 'lodash';

export const state = {
    trainTestDataFile: null,
    uploadedFiles: [],
    testPercent: 25.0,
    learningRate: 0.01,
    learningEpochs: 1000,
    resultLoading: false,
    result: {
        sensitivity: 0,
        specificity: 0,
        accuracy: 0,
    },
    modelParams: {},
    modelParamsLoading: false,
};

const TYPE_SET_TRAIN_TEST_FILE = 'SET_TRAIN_TEST_FILE';
const TYPE_SET_TEST_PERCENT = 'TEST_PERCENT';
const TYPE_SET_LEARNING_RATE = 'LEARNING_RATE';
const TYPE_SET_LEARNING_EPOCHS = 'LEARNING_EPOCHS';
const TYPE_SET_FETCH_RESULTS_START = 'FETCH_RESULTS_START';
const TYPE_SET_FETCH_RESULTS_END = 'FETCH_RESULTS_END';
const TYPE_SET_RESULTS = 'SET_RESULTS';
const TYPE_FETCH_MODEL_PARAMS_START = 'FETCH_MODEL_PARAMS_START';
const TYPE_FETCH_MODEL_PARAMS_END = 'FETCH_MODEL_PARAMS_END';
const TYPE_SET_MODEL_PARAMS = 'SET_MODEL_PARAMS';
const TYPE_SET_MODEL_PARAM_VALUE = 'SET_MODEL_PARAM_VALUE';
const TYPE_SET_UPLOADED_FILES = 'SET_UPLOADED_FILES';

export const mutations = {
    [TYPE_SET_TRAIN_TEST_FILE](state, payload) {
        state.trainTestDataFile = payload;
    },
    [TYPE_SET_TEST_PERCENT](state, payload) {
        state.testPercent = payload;
    },
    [TYPE_SET_LEARNING_RATE](state, payload) {
        state.learningRate = payload;
    },
    [TYPE_SET_LEARNING_EPOCHS](state, payload) {
        state.learningEpochs = payload;
    },
    [TYPE_SET_FETCH_RESULTS_START](state) {
        state.resultLoading = true;
    },
    [TYPE_SET_FETCH_RESULTS_END](state) {
        state.resultLoading = false;
    },
    [TYPE_SET_RESULTS](state, payload) {
        Vue.set(state, 'result', payload);
    },
    [TYPE_FETCH_MODEL_PARAMS_START](state) {
        state.modelParamsLoading = true;
    },
    [TYPE_FETCH_MODEL_PARAMS_END](state) {
        state.modelParamsLoading = false;
    },
    [TYPE_SET_MODEL_PARAMS](state, payload) {
        Vue.set(state, 'modelParams', payload);
    },
    [TYPE_SET_MODEL_PARAM_VALUE](state, {code, value}) {
        Vue.set(state.modelParams, code, {
            ...state.modelParams[code],
            value
        });
    },
    [TYPE_SET_UPLOADED_FILES](state, payload) {
        state.uploadedFiles = payload;
    }
};

export const actions = {
    async uploadFile({commit}, payload) {
        try {
            if (typeof payload.name === 'undefined') {
                throw new Error('Empty file');
            }
            const form = new FormData();
            form.append('file', payload);
            const response = await axios.post(`${API_DOMAIN}/upload_data/`,
                form,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            )
                .then(result => result.data || {})
                .catch(function () {
                    console.log('FAILURE!!');
                });
            if (response.status === 'success') {
                await commit(TYPE_SET_TRAIN_TEST_FILE, response.result);
            } else {
                console.log(response.result.message || 'error');
            }
        } catch (e) {
            console.log(e.message);
        }
    },
    setTestPercent({commit}, payload) {
        commit(TYPE_SET_TEST_PERCENT, Number(payload));
    },
    setLearningRate({commit}, payload) {
        commit(TYPE_SET_LEARNING_RATE, Number(payload));
    },
    setLearningEpochs({commit}, payload) {
        commit(TYPE_SET_LEARNING_EPOCHS, Number(payload));
    },
    async fetchResults({commit}, payload) {
        try {
            await commit(TYPE_SET_FETCH_RESULTS_START);
            const response = await axios.post(`${API_DOMAIN}/fit_predict/`,
                payload
            )
                .then(result => result.data || {})
                .catch(function () {
                    console.log('FAILURE!!');
                });
            if (response.status === 'success') {
                await commit(TYPE_SET_RESULTS, response.result);
                await commit(TYPE_SET_FETCH_RESULTS_END);
            } else {
                await commit(TYPE_SET_FETCH_RESULTS_END);
                console.log(response.result.message || 'error');
            }
        } catch (e) {
            await commit(TYPE_SET_FETCH_RESULTS_END);
            console.log(e.message);
        }
    },
    async fetchModelParams({commit}, payload) {
        try {
            await commit(TYPE_FETCH_MODEL_PARAMS_START);
            const response = await axios.get(`${API_DOMAIN}/model_params`,
                payload
            )
                .then(result => result.data || {})
                .catch(function () {
                    console.log('FAILURE!!');
                });
            if (response.status === 'success') {
                await commit(TYPE_SET_MODEL_PARAMS, keyBy(get(response, ['result', 'params'], []), 'code'));
                await commit(TYPE_FETCH_MODEL_PARAMS_END);
            } else {
                await commit(TYPE_FETCH_MODEL_PARAMS_END);
                console.log(response.result.message || 'error');
            }
        } catch (e) {
            await commit(TYPE_FETCH_MODEL_PARAMS_END);
            console.log(e.message);
        }
    },
    setModelParam({commit}, {code, value}) {
        commit(TYPE_SET_MODEL_PARAM_VALUE, {code, value})
    },
    async fetchUploadedFiles({commit}) {
        try {
            const response = await axios.get(`${API_DOMAIN}/get_files/`,
                {}
            )
                .then(result => result.data || {})
                .catch(function () {
                    console.log('FAILURE!!');
                });
            if (response.status === 'success') {
                await commit(TYPE_SET_UPLOADED_FILES, get(response, ['result'], []));
            } else {
                console.log(response.result.message || 'error');
            }
        } catch (e) {
            console.log(e.message);
        }
    },
    async setTrainTestFile({commit}, file) {
        await commit(TYPE_SET_TRAIN_TEST_FILE, {file_path: file});
    }
};

export const getters = {
    trainTestDataFile: state => state.trainTestDataFile,
    isTrainTestDataFileValid: state => !!state.trainTestDataFile,
    testPercent: state => state.testPercent,
    learningRate: state => state.learningRate,
    learningEpochs: state => state.learningEpochs,
    result: state => state.result,
    resultLoading: state => state.resultLoading,
    modelParams: state => state.modelParams,
    modelParamsLoading: state => state.modelParamsLoading,
    uploadedFiles: state => state.uploadedFiles,
};
