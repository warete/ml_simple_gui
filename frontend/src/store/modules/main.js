import axios from "axios";
import {API_DOMAIN} from "@/constants";
import Vue from 'vue';

export const state = {
  trainTestDataFile: null,
  testPercent: 25.0,
  learningRate: 0.01,
  learningEpochs: 1000,
  resultLoading: false,
  result: {
    sensitivity: 0,
    specificity: 0,
    accuracy: 0,
  }
};

const TYPE_SET_TRAIN_TEST_FILE = 'SET_TRAIN_TEST_FILE';
const TYPE_SET_TEST_PERCENT = 'TEST_PERCENT';
const TYPE_SET_LEARNING_RATE = 'LEARNING_RATE';
const TYPE_SET_LEARNING_EPOCHS = 'LEARNING_EPOCHS';
const TYPE_SET_FETCH_RESULTS_START = 'FETCH_RESULTS_START';
const TYPE_SET_FETCH_RESULTS_END = 'FETCH_RESULTS_END';
const TYPE_SET_RESULTS = 'SET_RESULTS';

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
}
