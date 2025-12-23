<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const form = reactive({
  Age: null,
  Height: null,
  Weight: null,
  FCVC: 2,
  FAVC: "no",
  NCP: 3,
  CAEC: "Sometimes",
  CH2O: 2,
  FAF: 1,
  TUE: 1,
  SMOKE: "no",
  CALC: "Sometimes",
  MTRANS: "Public_Transportation",
  SCC: "no",
});

function submit() {
  localStorage.setItem("userInput", JSON.stringify(form));
  router.push("/result");
}
</script>

<template>
  <div class="container">
    <h1>Nutrition & Lifestyle Assessment</h1>

    <!-- BODY -->
    <section>
      <h2>Basic Information</h2>
      <input
        v-model.number="form.Age"
        type="number"
        placeholder="Age"
        min="1"
        max="125"
      />
      <input
        v-model.number="form.Height"
        type="number"
        min="0.5"
        max="2.8"
        step="0.01"
        placeholder="Height (m)"
      />
      <input
        v-model.number="form.Weight"
        min="2"
        max="700"
        type="number"
        placeholder="Weight (kg)"
      />
    </section>

    <!-- DIET -->
    <section>
      <h2>Diet Habits</h2>

      <label>Vegetable Intake</label>
      <select v-model.number="form.FCVC">
        <option :value="1">Low</option>
        <option :value="2">Moderate</option>
        <option :value="3">High</option>
      </select>

      <label>High-calorie foods frequently?</label>
      <select v-model="form.FAVC">
        <option value="yes">Yes</option>
        <option value="no">No</option>
      </select>

      <label>Main meals per day</label>
      <select v-model.number="form.NCP">
        <option :value="1">1</option>
        <option :value="2">2</option>
        <option :value="3">3</option>
        <option :value="4">4+</option>
      </select>

      <label>Snacking between meals</label>
      <select v-model="form.CAEC">
        <option value="no">No</option>
        <option value="Sometimes">Sometimes</option>
        <option value="Frequently">Frequently</option>
        <option value="Always">Always</option>
      </select>

      <label>Alcohol consumption</label>
      <select v-model="form.CALC">
        <option value="no">No</option>
        <option value="Sometimes">Sometimes</option>
        <option value="Frequently">Frequently</option>
        <option value="Always">Always</option>
      </select>
    </section>

    <!-- LIFESTYLE -->
    <section>
      <h2>Lifestyle</h2>

      <label>Daily water intake</label>
      <select v-model.number="form.CH2O">
        <option :value="1">Low</option>
        <option :value="2">Moderate</option>
        <option :value="3">High</option>
      </select>

      <label>Physical activity</label>
      <select v-model.number="form.FAF">
        <option :value="0">None</option>
        <option :value="1">Low</option>
        <option :value="2">Moderate</option>
        <option :value="3">High</option>
      </select>

      <label>Screen time</label>
      <select v-model.number="form.TUE">
        <option :value="0">Low</option>
        <option :value="1">Moderate</option>
        <option :value="2">High</option>
      </select>

      <label>Do you smoke?</label>
      <select v-model="form.SMOKE">
        <option value="yes">Yes</option>
        <option value="no">No</option>
      </select>

      <label>Monitor calorie intake?</label>
      <select v-model="form.SCC">
        <option value="yes">Yes</option>
        <option value="no">No</option>
      </select>

      <label>Primary transportation</label>
      <select v-model="form.MTRANS">
        <option>Public_Transportation</option>
        <option>Automobile</option>
        <option>Walking</option>
        <option>Motorbike</option>
        <option>Bicycle</option>
      </select>
    </section>

    <button @click="submit">Analyse</button>
  </div>
</template>
