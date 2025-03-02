<template>
  <div class="top-100-page">
    <!-- Компонент HeaderService -->
    <HeaderService />

    <!-- Меню с фильтрами и настройками -->
    <div class="controls">
      <!-- Первая строка: фильтры по времени -->
      <div class="filters">
        <button
          v-for="(button, index) in timeFilters"
          :key="index"
          :class="{ active: activeTimeFilter === button.apiUrl }"
          @click="changeTimeFilter(button.apiUrl)"
        >
          {{ button.label }}
        </button>
      </div>

      <!-- Вторая строка: выбор "Фильмы" или "Сериалы" -->
      <div class="type-filter">
        <select v-model="typeFilter" @change="fetchMovies" class="custom-select">
          <option value="all">Все</option>
          <option value="movie">Фильмы</option>
          <option value="series">Сериалы</option>
        </select>
      </div>

      <!-- Настройки колонок (скрыты на мобильных) -->
      <div class="grid-settings" v-if="!isMobile">
        <span>Колонок:</span>
        <button
          v-for="cols in [3, 4, 5]"
          :key="cols"
          :class="{ active: gridColumns === cols }"
          @click="gridColumns = cols"
        >
          {{ cols }}
        </button>
      </div>
    </div>

    <!-- Лоадер -->
    <div v-if="loading" class="loading">
      <span>Загрузка...</span>
      <div class="loader"></div>
    </div>

    <!-- Сетка фильмов -->
    <div class="grid" :style="{ 'grid-template-columns': `repeat(${gridColumns}, 1fr)` }" v-if="!loading">
      <div v-for="movie in movies" :key="movie.kp_id" class="movie" @click="goToMoviePage(movie)">
        <div class="movie-poster-container">
          <img :src="movie.cover" :alt="movie.title" class="movie-poster" />
          <div class="ratings-overlay">
            <span v-if="movie.rating_kp" class="rating-kp">КП: {{ movie.rating_kp }}</span>
            <span v-if="movie.rating_imdb" class="rating-imdb">IMDb: {{ movie.rating_imdb }}</span>
          </div>
        </div>
        <div class="movie-details">
          <div class="movie-header">
            <h3 :title="movie.title">{{ movie.title }}</h3>
            <span class="year">{{ movie.year }}</span>
          </div>
          <div class="meta">
            <span class="type">{{ movie.type.replace("🎬", "") }}</span>
          </div>
          <div class="views">
            <span class="eye-icon">👁️</span>
            <span>{{ formatViews(movie.views_count) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import HeaderService from "@/components/HeaderService.vue"; // Импорт компонента HeaderService
import { useRouter } from "vue-router"; // Импорт роутера
const apiUrl = import.meta.env.VITE_APP_API_URL;

// Состояния
const movies = ref([]);
const loading = ref(false);
const activeTimeFilter = ref("all");
const typeFilter = ref("all");
const gridColumns = ref(4); // По умолчанию 4 колонки
const history = ref([]); // История просмотров
const router = useRouter(); // Роутер

// Фильтры по времени
const timeFilters = [
  { label: "Всё время", apiUrl: "all" },
  { label: "30 дней", apiUrl: "30d" },
  { label: "7 дней", apiUrl: "7d" },
  { label: "24 часа", apiUrl: "24h" },
];

// Определение мобильного устройства
const isMobile = computed(() => window.innerWidth <= 768);

// Функция для получения фильмов
const fetchMovies = async () => {
  loading.value = true;
  try {
    const url = `${apiUrl}/top/${activeTimeFilter.value}?type=${typeFilter.value}`;
    const response = await fetch(url);
    const data = await response.json();
    movies.value = data;
  } catch (error) {
    console.error("Ошибка при загрузке фильмов:", error);
  } finally {
    loading.value = false;
  }
};

// Функция для изменения фильтра по времени
const changeTimeFilter = (apiUrl) => {
  activeTimeFilter.value = apiUrl;
  fetchMovies();
};

// Функция для форматирования просмотров
const formatViews = (views) => {
  if (views >= 1000000) {
    return `${(views / 1000000).toFixed(1)}M`;
  }
  if (views >= 1000) {
    return `${(views / 1000).toFixed(1)}K`;
  }
  return views;
};

// Загрузка истории из cookies
const loadHistory = () => {
  const savedHistory = localStorage.getItem("movie-history");
  if (savedHistory) {
    try {
      history.value = JSON.parse(savedHistory);
    } catch (e) {
      console.error("Ошибка загрузки истории:", e);
      history.value = [];
    }
  }
};

// Сохранение истории в cookies
const saveHistory = () => {
  localStorage.setItem("movie-history", JSON.stringify(history.value));
};

// Переход на страницу фильма и добавление в историю
const goToMoviePage = (movie) => {
  if (!history.value.some((m) => m.kp_id === movie.kp_id)) {
    history.value = [movie, ...history.value.slice(0, 9)]; // Ограничиваем историю 10 последними
    saveHistory();
  }
  router.push({ name: "player-page", params: { kp_id: movie.kp_id } });
};

// Загрузка фильмов и истории при монтировании компонента
onMounted(() => {
  fetchMovies();
  loadHistory();
});
</script>

<style scoped>
.top-100-page {
  font-family: Arial, sans-serif;
  color: #ffffff;
  padding: 0px 4px 20px 4px;
  max-width: 1200px;
  margin: 0 auto;
}

.controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
  align-items: center;
  justify-content: center;
}

.filters {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.type-filter {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: center;
  max-width: 367.5px;
  width: 100%;
}

.grid-settings {
  display: flex;
  gap: 15px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

button {
  padding: 8px 16px;
  border: 1px solid #444;
  background-color: #1e1e1e;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

button.active {
  background-color: #fff;
  color: #000;
}

button:hover {
  background-color: #444;
}

.custom-select {
  padding: 8px 16px;
  border: 1px solid #444;
  background-color: #1e1e1e;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
  width: 100%;
}

.custom-select:hover {
  border-color: #666;
}

.loading {
  text-align: center;
  margin-top: 20px;
}

.loader {
  border: 4px solid #444;
  border-top: 4px solid #fff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.grid {
  display: grid;
  gap: 15px; /* Уменьшенный промежуток между карточками */
}

.movie {
  background: rgba(30, 30, 30, 0.6);
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  max-width: 320px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

.movie:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.movie-poster-container {
  position: relative;
}

.movie-poster {
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
}

.ratings-overlay {
  position: absolute;
  bottom: 10px;
  left: 10px;
  display: flex;
  gap: 10px;
  background: rgba(0, 0, 0, 0.7);
  padding: 5px 10px;
  border-radius: 5px;
}

.rating-kp,
.rating-imdb {
  font-size: 1.2em;
  color: #fff;
}

.movie-details {
  padding: 15px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.movie-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* Выравнивание по верхнему краю */
  margin-bottom: 10px;
}

.movie-header h3 {
  font-size: 1.2em;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* Ограничение на 3 строки */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2; /* Уменьшенный межстрочный интервал */
  max-height: 3.6em; /* Ограничение высоты */
}

.year {
  font-size: 0.9em;
  color: #bbb;
  margin-left: 10px; /* Отступ от заголовка */
}

.meta {
  margin-bottom: 10px;
}

.type {
  font-size: 0.9em;
  color: #bbb;
}

.views {
  font-size: 0.9em;
  color: #bbb;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.eye-icon {
  font-size: 1em;
  color: #bbb;
}

/* Мобильная версия */
@media (max-width: 550px) {
  .grid {
    grid-template-columns: 1fr !important;
    gap: 10px;
  }

  .movie {
    flex-direction: row;
    align-items: flex-start;
    max-width: 100%;
    height: 210px; /* Высота карточки увеличена */
  }

  .movie-poster-container {
    width: 140px; /* Ширина постера увеличена */
  }

  .movie-poster {
    width: 140px;
    aspect-ratio: 2 / 3;
    border-radius: 10px 0 0 10px;
  }

  .ratings-overlay {
    bottom: 5px;
    left: 5px;
    padding: 4px 8px;
    font-size: 1em;
  }

  .movie-details {
    padding: 10px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .movie-header h3 {
    font-size: 1.2em; /* Увеличенный шрифт */
    -webkit-line-clamp: 2; /* Ограничение на 2 строки для мобильных */
    max-height: 2.4em; /* Ограничение высоты */
  }

  .year,
  .type,
  .views {
    font-size: 1em; /* Увеличенный шрифт */
  }

  .eye-icon {
    font-size: 1.2em; /* Увеличенный шрифт */
  }
}
</style>