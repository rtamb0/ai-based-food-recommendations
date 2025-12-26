<script setup>
import { computed, reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const form = reactive({
  Age: null,
  Height: null,
  Weight: null,
  FCVC: null,
  FAVC: "",
  NCP: null,
  CAEC: "",
  CH2O: null,
  FAF: null,
  TUE: null,
  SMOKE: "",
  CALC: "",
  SCC: "",
  MTRANS: "",
});

const touched = reactive({
  Age: false,
  Height: false,
  Weight: false,
  FCVC: false,
  FAVC: false,
  NCP: false,
  CAEC: false,
  CH2O: false,
  FAF: false,
  TUE: false,
  SMOKE: false,
  CALC: false,
  SCC: false,
  MTRANS: false,
});

const errors = computed(() => {
  const e = {};

  if (form.Age === null || form.Age < 1 || form.Age > 125) {
    e.Age = "Age must be between 1 and 125";
  }

  if (form.Height === null || form.Height < 0.5 || form.Height > 2.8) {
    e.Height = "Height must be between 0.5 and 2.8 meters";
  }

  if (form.Weight === null || form.Weight < 2 || form.Weight > 700) {
    e.Weight = "Weight must be between 2 and 700 kg";
  }

  if (![1, 2, 3].includes(form.FCVC)) {
    e.FCVC = "Invalid vegetable intake";
  }

  if (![1, 2, 3, 4].includes(form.NCP)) {
    e.NCP = "Invalid meal count";
  }

  if (form.CH2O === null || form.CH2O < 1 || form.CH2O > 3) {
    e.CH2O = "Invalid water intake";
  }

  if (form.FAF === null || form.FAF < 0 || form.FAF > 3) {
    e.FAF = "Invalid physical activity value";
  }

  if (form.TUE === null || form.TUE < 0 || form.TUE > 2) {
    e.TUE = "Invalid screen time value";
  }

  if (form.FAVC === "") {
    e.FAVC = "Please select an option for high-calorie food intake";
  }

  if (form.CAEC === "") {
    e.CAEC = "Please select an option for snacking between meals";
  }

  if (form.SMOKE === "") {
    e.SMOKE = "Please specify if you smoke";
  }

  if (form.CALC === "") {
    e.CALC = "Please select an option for alcohol consumption";
  }

  if (form.SCC === "") {
    e.SCC = "Please specify if you monitor calorie intake";
  }

  if (form.MTRANS === "") {
    e.MTRANS = "Please select your primary means of transportation";
  }

  return e;
});

const isValid = computed(() => Object.keys(errors.value).length === 0);

function markTouched(field) {
  touched[field] = true;
}

function submit() {
  if (!isValid.value) return;

  localStorage.setItem("userInput", JSON.stringify(form));
  router.push("/result");
}
</script>

<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Nutrition & Lifestyle Assessment</h1>

    <!-- Basic Information Section -->
    <section class="mb-5">
      <h2 class="h4 mb-3">Basic Information</h2>
      <div class="form-group mb-3">
        <label for="age">Age</label>
        <input
          class="form-control"
          id="age"
          v-model.number="form.Age"
          @blur="markTouched('Age')"
          type="number"
          placeholder="Age"
          min="1"
          max="125"
        />
        <div v-if="touched.Age && errors.Age" class="text-danger mt-2">
          {{ errors.Age }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="height">Height (meters)</label>
        <input
          class="form-control"
          id="height"
          v-model.number="form.Height"
          @blur="markTouched('Height')"
          type="number"
          min="0.5"
          max="2.8"
          step="0.01"
          placeholder="Height (m)"
        />
        <div v-if="touched.Height && errors.Height" class="text-danger mt-2">
          {{ errors.Height }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="weight">Weight (kg)</label>
        <input
          class="form-control"
          id="weight"
          v-model.number="form.Weight"
          @blur="markTouched('Weight')"
          min="2"
          max="700"
          type="number"
          placeholder="Weight (kg)"
        />
        <div v-if="touched.Weight && errors.Weight" class="text-danger mt-2">
          {{ errors.Weight }}
        </div>
      </div>
    </section>

    <!-- Diet Habits Section -->
    <section class="mb-5">
      <h2 class="h4 mb-3">Diet Habits</h2>
      <div class="form-group mb-3">
        <label for="fcvc">Vegetable Intake</label>
        <select
          class="form-control"
          id="fcvc"
          v-model.number="form.FCVC"
          @blur="markTouched('FCVC')"
        >
          <option disabled :value="null">Select one</option>
          <option :value="1">Low</option>
          <option :value="2">Moderate</option>
          <option :value="3">High</option>
        </select>
        <div v-if="touched.FCVC && errors.FCVC" class="text-danger mt-2">
          {{ errors.FCVC }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="favc">High-calorie foods frequently?</label>
        <select
          class="form-control"
          id="favc"
          v-model="form.FAVC"
          @blur="markTouched('FAVC')"
        >
          <option disabled value="">Select one</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
        <div v-if="touched.FAVC && errors.FAVC" class="text-danger mt-2">
          {{ errors.FAVC }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="ncp">Main meals per day</label>
        <select
          class="form-control"
          id="ncp"
          v-model.number="form.NCP"
          @blur="markTouched('NCP')"
        >
          <option disabled :value="null">Select one</option>
          <option :value="1">1</option>
          <option :value="2">2</option>
          <option :value="3">3</option>
          <option :value="4">4+</option>
        </select>
        <div v-if="touched.NCP && errors.NCP" class="text-danger mt-2">
          {{ errors.NCP }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="caec">Snacking between meals</label>
        <select
          class="form-control"
          id="caec"
          v-model="form.CAEC"
          @blur="markTouched('CAEC')"
        >
          <option disabled value="">Select one</option>
          <option value="no">No</option>
          <option value="Sometimes">Sometimes</option>
          <option value="Frequently">Frequently</option>
          <option value="Always">Always</option>
        </select>
        <div v-if="touched.CAEC && errors.CAEC" class="text-danger mt-2">
          {{ errors.CAEC }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="calc">Alcohol consumption</label>
        <select
          class="form-control"
          id="calc"
          v-model="form.CALC"
          @blur="markTouched('CALC')"
        >
          <option disabled value="">Select one</option>
          <option value="no">No</option>
          <option value="Sometimes">Sometimes</option>
          <option value="Frequently">Frequently</option>
          <option value="Always">Always</option>
        </select>
        <div v-if="touched.CALC && errors.CALC" class="text-danger mt-2">
          {{ errors.CALC }}
        </div>
      </div>
    </section>

    <!-- Lifestyle Section -->
    <section class="mb-5">
      <h2 class="h4 mb-3">Lifestyle</h2>
      <div class="form-group mb-3">
        <label for="ch2o">Daily water intake</label>
        <select
          class="form-control"
          id="ch2o"
          v-model.number="form.CH2O"
          @blur="markTouched('CH2O')"
        >
          <option disabled :value="null">Select one</option>
          <option :value="1">Low</option>
          <option :value="2">Moderate</option>
          <option :value="3">High</option>
        </select>
        <div v-if="touched.CH2O && errors.CH2O" class="text-danger mt-2">
          {{ errors.CH2O }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="faf">Physical activity</label>
        <select
          class="form-control"
          id="faf"
          v-model.number="form.FAF"
          @blur="markTouched('FAF')"
        >
          <option disabled :value="null">Select one</option>
          <option :value="0">None</option>
          <option :value="1">Low</option>
          <option :value="2">Moderate</option>
          <option :value="3">High</option>
        </select>
        <div v-if="touched.FAF && errors.FAF" class="text-danger mt-2">
          {{ errors.FAF }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="tue">Screen time</label>
        <select
          class="form-control"
          id="tue"
          v-model.number="form.TUE"
          @blur="markTouched('TUE')"
        >
          <option disabled :value="null">Select one</option>
          <option :value="0">Low</option>
          <option :value="1">Moderate</option>
          <option :value="2">High</option>
        </select>
        <div v-if="touched.TUE && errors.TUE" class="text-danger mt-2">
          {{ errors.TUE }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="smoke">Do you smoke?</label>
        <select
          class="form-control"
          id="smoke"
          v-model="form.SMOKE"
          @blur="markTouched('SMOKE')"
        >
          <option disabled value="">Select one</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
        <div v-if="touched.SMOKE && errors.SMOKE" class="text-danger mt-2">
          {{ errors.SMOKE }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="scc">Monitor calorie intake?</label>
        <select
          class="form-control"
          id="scc"
          v-model="form.SCC"
          @blur="markTouched('SCC')"
        >
          <option disabled value="">Select one</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
        <div v-if="touched.SCC && errors.SCC" class="text-danger mt-2">
          {{ errors.SCC }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="mtrans">Primary transportation</label>
        <select
          class="form-control"
          id="mtrans"
          v-model="form.MTRANS"
          @blur="markTouched('MTRANS')"
        >
          <option disabled value="">Select one</option>
          <option value="Public_Transportation">Public Transportation</option>
          <option value="Automobile">Automobile</option>
          <option value="Walking">Walking</option>
          <option value="Motorbike">Motorbike</option>
          <option value="Bicycle">Bicycle</option>
        </select>
        <div v-if="touched.MTRANS && errors.MTRANS" class="text-danger mt-2">
          {{ errors.MTRANS }}
        </div>
      </div>
    </section>

    <button
      @click="submit"
      :disabled="!isValid"
      class="btn btn-primary btn-block"
    >
      Analyse
    </button>
  </div>
</template>

<style scoped>
.text-danger {
  font-size: 0.875rem;
}
</style>
