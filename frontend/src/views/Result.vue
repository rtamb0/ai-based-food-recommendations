<script setup>
import { onMounted, ref } from "vue";

const result = ref(null);
const loading = ref(true);

onMounted(async () => {
  const input = JSON.parse(localStorage.getItem("userInput"));

  const res = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });

  result.value = await res.json();
  loading.value = false;
});
</script>

<template>
  <div>
    <h1>Result</h1>

    <p v-if="loading">Analysing...</p>

    <div v-else>
      <p><strong>Nutrition Risk:</strong> {{ result.nutrition_risk }}</p>

      <ul>
        <li v-for="n in result.nutrient_risks" :key="n">
          {{ n }}
        </li>
      </ul>
    </div>
  </div>
</template>
