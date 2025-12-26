<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const result = ref(null);
const loading = ref(true);

const router = useRouter();

const fetchResults = async (forceRefresh = false) => {
  const input = JSON.parse(localStorage.getItem("userInput"));

  if (!forceRefresh) {
    if (localStorage.getItem("cachedResult") && localStorage.getItem("cachedUserInput")) {
      const previousUserInput = JSON.parse(localStorage.getItem("cachedUserInput"));

      if (JSON.stringify(input) === JSON.stringify(previousUserInput)) {
        result.value = JSON.parse(localStorage.getItem("cachedResult"));
        loading.value = false;
        return;
      }
    }
  }

  loading.value = true;

  const res = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });

  result.value = await res.json();
  loading.value = false;

  localStorage.setItem("cachedResult", JSON.stringify(result.value));
  localStorage.setItem("cachedUserInput", JSON.stringify(input));
};

onMounted(() => {
  fetchResults();
});

const refreshResults = async () => {
  localStorage.removeItem("cachedResult");
  localStorage.removeItem("cachedUserInput");
  await fetchResults(true);
};

</script>

<template>
  <div class="container my-5">
    <!-- Back Button -->
    <div class="mb-3 d-flex gap-2">
      <button class="btn btn-outline-secondary" @click="router.push('/')">
        ← Back
      </button>

      <button class="btn btn-outline-primary"   :disabled="loading"
      @click="refreshResults">
        ⟳ Refresh
      </button>
    </div>

    <h1 class="text-center mb-4">Nutrition Analysis Results</h1>

    <!-- Loading Indicator -->
    <div v-if="loading">
      <p class="text-center">
        <span class="spinner-border text-primary" role="status" aria-hidden="true"></span>
        <strong> Analysing...</strong>
      </p>
    </div>

    <!-- Content -->
    <div v-else>
      <!-- Overview Section -->
      <div class="mb-5">
        <h2 class="mb-3 text-primary">Overview</h2>
        <div class="card shadow-sm p-4">
          <p>
            <strong>Nutrition Risk:</strong>
            <span
              class="badge bg-danger text-white"
              >{{ result.nutrition_risk }}</span
            >
          </p>
          <h5 class="text-secondary mt-3">Nutrient Risks</h5>
          <ul class="list-group list-group-flush">
            <li
              class="list-group-item"
              v-for="n in result.nutrient_risks"
              :key="n"
            >
              <div class="ms-3 mt-2 mb-2">{{ n }}</div>
            </li>
          </ul>
        </div>
      </div>

      <!-- AI Suggestions Section -->
      <div class="mb-5">
        <h2 class="mb-3 text-primary">AI Suggestions</h2>
        <div class="row row-cols-1 row-cols-md-2 g-4">
          <!-- Explanation -->
          <div class="col">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title text-secondary">Explanation</h5>
                <p class="card-text">{{ result.ai.explanation }}</p>
              </div>
            </div>
          </div>

          <!-- Recommended Nutrients -->
          <div class="col">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title text-secondary">Recommended Nutrients</h5>
                <ul class="list-group list-group-flush">
                  <li v-for="nutrient in result.ai.nutrients" :key="nutrient" class="list-group-item">
                   <div class="ms-3 mt-2 mb-2">{{ nutrient }}</div> 
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Food Groups -->
      <div class="col-12 mb-5">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title text-secondary mb-3">
              Recommended Food Groups
            </h5>
            <div
              class="accordion accordion-flush"
              id="foodGroupsAccordion"
            >
              <div
                v-for="group in result.ai.food_groups"
                :key="group.meal_type"
                class="accordion-item"
              >
                <h2 class="accordion-header" :id="group.meal_type">
                  <button
                    class="accordion-button text-capitalize"
                    type="button"
                    data-bs-toggle="collapse"
                    :data-bs-target="'#collapse' + group.meal_type"
                    aria-expanded="true"
                    :aria-controls="'collapse' + group.meal_type"
                  >
                    {{ group.meal_type }}
                  </button>
                </h2>
                <div
                  :id="'collapse' + group.meal_type"
                  class="accordion-collapse collapse show"
                  :aria-labelledby="group.meal_type"
                  data-bs-parent="#foodGroupsAccordion"
                >
                  <div class="accordion-body">
                    <ul>
                      <li
                        v-for="ingredient in group.ingredients"
                        :key="ingredient.name"
                        class="text-muted"
                      >
                        <strong>{{ ingredient.name }}:</strong
                        >
                        {{ ingredient.reason }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recipes Section with Pagination per Category -->
      <div class="mb-5">
        <h2 class="mb-3 text-primary">Suggested Recipes</h2>
        <div v-for="recipeCategory in result.ai.spoonacular" :key="recipeCategory.meal_type" class="mb-5">
          <h4 class="text-capitalize">{{ recipeCategory.meal_type }}</h4>
          <div
            class="carousel slide carousel-dark"
            :id="'carousel-' + recipeCategory.meal_type"
            data-bs-ride="carousel"
          >
            <div class="carousel-inner">
              <div
                v-for="(recipe, index) in recipeCategory.recipes"
                :key="recipe.id"
                :class="['carousel-item', { active: index === 0 }]"
              >
                <div class="card h-100 shadow-sm">
                  <div class="row g-0">
                    <div class="col-md-4">
                      <img
                        :src="recipe.image"
                        class="img-fluid"
                        :alt="recipe.title"
                      />
                    </div>
                    <div class="col-md-8">
                      <div class="card-body">
                        <h5 class="card-title">{{ recipe.title }}</h5>
                        <p class="card-text">
                          <strong>Ingredients You'll Need:</strong>
                          <ul>
                            <li
                              v-for="ingredient in [...recipe.usedIngredients, ...recipe.missedIngredients]"
                              :key="ingredient.id"
                            >
                              {{ ingredient.name }} - {{ ingredient.amount || '' }} {{
                                ingredient.unit || ''
                              }}
                            </li>
                          </ul>
                        </p>
                        <a
                          class="btn btn-outline-primary btn-sm"
                          target="_blank"
                          :href="'https://spoonacular.com/recipes/' + recipe.title + '-' + recipe.id"
                        >View Recipe</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Carousel Controls -->
            <button
              class="carousel-control-prev"
              type="button"
              :data-bs-target="'#carousel-' + recipeCategory.meal_type"
              data-bs-slide="prev"
            >
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous</span>
            </button>
            <button
              class="carousel-control-next"
              type="button"
              :data-bs-target="'#carousel-' + recipeCategory.meal_type"
              data-bs-slide="next"
            >
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Next</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-primary {
  color: #007bff;
}

.text-secondary {
  color: #6c757d;
}

.card {
  border: none;
}

.card .card-title {
  font-weight: 600;
}

ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

ul li {
  border-bottom: 1px solid #f1f1f1;
  padding: 5px 0;
}
</style>