<template>
  <div id="app">
    <HeaderService />

    <!-- Кнопки выбора типа поиска -->
    <div class="search-type-buttons">
      <button
        :class="{ active: searchType === 'title' }"
        @click="setSearchType('title')"
      >
        Название
      </button>
      <button
        :class="{ active: searchType === 'kinopoisk' }"
        @click="setSearchType('kinopoisk')"
      >
        ID Кинопоиск
      </button>
      <button
        :class="{ active: searchType === 'shikimori' }"
        @click="setSearchType('shikimori')"
      >
        ID Shikimori
      </button>
    </div>

    <!-- Поиск -->
    <div class="search-container">
      <input
        v-model="searchTerm"
        :placeholder="getPlaceholder()"
        class="search-input"
        @keydown.enter="search"
      />
      <button @click="search" class="search-button">
        <i class="fas fa-search"></i>
      </button>
      <button @click="resetSearch" class="reset-button">Сброс</button>
    </div>

    <!-- Контейнер для истории и результатов -->
    <div class="content-container">
      <!-- История просмотра -->
      <div v-if="!searchTerm && history.length > 0">
        <h2>История просмотра</h2>
        <transition-group name="fade" tag="div" class="cards-container">
          <div
            v-for="movie in history"
            :key="movie.id"
            class="movie-card"
            @click="goToMoviePage(movie)"
          >
            <div class="movie-poster-container">
              <img
                :src="movie.poster"
                alt="Постер"
                class="movie-poster"
              />
              <!-- Кнопка удаления из истории -->
              <button
                class="remove-button"
                @click.stop="removeFromHistory(movie.id)"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="movie-details">
              <div class="movie-header">
                <h3>{{ removeYearFromTitle(movie.title) }}</h3>
                <span class="year">{{ movie.year }}</span>
              </div>
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Результаты поиска -->
      <div v-if="searchPerformed">
        <h2>Результаты поиска</h2>
        <div class="cards-container">
          <div
            v-for="movie in movies"
            :key="movie.id"
            class="movie-card"
            @click="goToMoviePage(movie)"
          >
            <div class="movie-poster-container">
              <img
                :src="movie.poster"
                alt="Постер"
                class="movie-poster"
              />
            </div>
            <div class="movie-details">
              <div class="movie-header">
                <h3>{{ removeYearFromTitle(movie.title) }}</h3>
                <span class="year">{{ movie.year }}</span>
              </div>
            </div>
          </div>
          <div v-if="movies.length === 0 && !loading" class="no-results">
            Ничего не найдено
          </div>
        </div>
      </div>

      <!-- Подсказка, когда ничего не введено в поиске -->
      <div v-if="searchTerm && !searchPerformed && !loading" class="search-prompt">
        Нажмите кнопку "Поиск" или Enter для поиска
      </div>
    </div>

    <!-- Спиннер -->
    <div v-if="loading" class="spinner"></div>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderService from '@/components/HeaderService.vue';
import { useRouter } from 'vue-router';
const apiUrl = import.meta.env.VITE_APP_API_URL;

export default {
  name: 'MovieSearch',
  components: {
    HeaderService,
  },

  data() {
    return {
      searchTerm: '',
      searchType: 'title', // По умолчанию поиск по названию
      movies: [],
      loading: false,
      history: [],
      searchPerformed: false, // Флаг, указывающий, был ли выполнен поиск
    };
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  mounted() {
    this.loadHistory();
  },

  methods: {
    // Удаление года из названия фильма
    removeYearFromTitle(title) {
      return title.replace(/\s*\(\d{4}\)\s*$/, ''); // Удаляем год в формате "(1999)"
    },

    // Установка типа поиска
    setSearchType(type) {
      this.searchType = type;
      this.resetSearch(); // Сбрасываем поиск при изменении типа
    },

    // Получение плейсхолдера для поля ввода
    getPlaceholder() {
      switch (this.searchType) {
        case 'title':
          return 'Введите название фильма';
        case 'kinopoisk':
          return 'Введите ID Кинопоиск';
        case 'shikimori':
          return 'Введите ID Shikimori';
        default:
          return 'Введите название фильма';
      }
    },

    async search() {
      if (!this.searchTerm) return;

      this.loading = true;
      this.searchPerformed = true; // Устанавливаем флаг, что поиск выполнен

      try {
        if (this.searchType === 'kinopoisk') {
          // Если поиск по ID Кинопоиск, перенаправляем на страницу фильма
          this.router.push({ name: 'player-page', params: { kp_id: this.searchTerm } });
        } else if (this.searchType === 'shikimori') {
          // Если поиск по ID Shikimori, перенаправляем на страницу фильма
          this.router.push({ name: 'player-page', params: { kp_id: `shiki${this.searchTerm}` } });
        } else {
          // Поиск по названию
          const response = await axios.get(`${apiUrl}/search/${this.searchTerm}`);
          this.movies = response.data;
        }
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.router.push('/400'); // Перенаправление на страницу ошибки 400
        } else {
          console.error('Ошибка при поиске фильмов:', error);
          alert('Произошла ошибка при поиске. Пожалуйста, попробуйте позже.');
        }
      } finally {
        this.loading = false;
      }
    },

    loadHistory() {
      const savedHistory = this.$cookies.get('movie-history');
      if (savedHistory) {
        try {
          this.history = JSON.parse(savedHistory);
        } catch (e) {
          console.error('Ошибка загрузки истории:', e);
          this.history = [];
        }
      }
    },

    saveHistory() {
      this.$cookies.set('movie-history', JSON.stringify(this.history), '30d');
    },

    goToMoviePage(movie) {
      if (!this.history.some(m => m.id === movie.id)) {
        this.history = [movie, ...this.history.slice(0, 9)]; // Ограничиваем историю 10 последними
        this.saveHistory();
      }
      this.router.push({ name: 'player-page', params: { kp_id: movie.id } });
    },

    removeFromHistory(movieId) {
      this.history = this.history.filter(movie => movie.id !== movieId);
      this.saveHistory();
    },

    resetSearch() {
      this.searchTerm = '';
      this.movies = [];
      this.searchPerformed = false; // Сбрасываем флаг при сбросе поиска
    },
  },
};
</script>

<style scoped>
/* Общие стили */
.search-type-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 10px;
  padding-top: 10px;
}

.search-type-buttons button {
  padding: 5px 10px;
  font-size: 16px;
  border: none;
  background: none;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.search-type-buttons button::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 100%;
  height: 2px;
  background-color: transparent;
  transition: background-color 0.3s ease;
}

.search-type-buttons button.active::after {
  background-color: #ffffff; /* Цвет подчеркивания для активной кнопки */
}

.search-type-buttons button:hover {
  color: #ffffff;
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 0px 20px 20px 20px;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background: rgba(30, 30, 30, 0.8);
  color: #fff;
  max-width: 800px;
}

.search-input:focus {
  background: rgba(30, 30, 30, 0.8);
}

.search-button {
  padding: 10px;
  font-size: 16px;
  border: none;
  background: rgba(30, 30, 30, 0.8);
  color: #fff;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border: 1px solid #ccc;
}

.search-button:hover {
  background-color: #464646;
}

.reset-button {
  padding: 10px;
  font-size: 16px;
  border: none;
  background: rgba(30, 30, 30, 0.8);
  color: #fff;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid #ccc;
}

.reset-button:hover {
  background-color: #464646;
}

/* Контейнер для истории и результатов */
.content-container {
  margin: 20px;
  color: #fff;
}

h2 {
  display: flex;
  font-size: 20px;
  margin-bottom: 20px;
  justify-content: center;
}

/* Контейнер для карточек */
.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

/* Карточка фильма */
.movie-card {
  font-family: Arial, sans-serif;
  width: 210px;
  text-align: center;
  background: rgba(30, 30, 30, 0.6);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  cursor: pointer;
  transition: transform 0.3s ease;
  position: relative;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-poster-container {
  position: relative;
}

.movie-poster {
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
}

/* Кнопка удаления из истории */
.remove-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(0, 0, 0, 0.7);
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.movie-card:hover .remove-button {
  opacity: 1;
}

.remove-button:hover {
  background-color: rgba(255, 0, 0, 0.7);
}

.movie-details {
  display: flex;
  padding: 15px;
  text-align: left;
  flex-direction: column;
}

.movie-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* Выравнивание по верхнему краю */
  margin-bottom: 10px;
}

.movie-header h3 {
  font-size: 1.1em;
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
  white-space: nowrap; /* Год не переносится */
}

/* Спиннер */
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Сообщение "Ничего не найдено" */
.no-results {
  width: 100%;
  text-align: center;
  color: #fff;
  font-size: 18px;
  margin-top: 20px;
}

/* Подсказка для поиска */
.search-prompt {
  text-align: center;
  color: #fff;
  font-size: 18px;
  margin-top: 20px;
}

/* Адаптация для мобильных устройств */
@media (max-width: 476px) {
  .movie-card {
    width: 100%;
    height: 180px;
    display: flex;
  }

  .movie-poster-container {
    width: 120px; /* Ширина постера увеличена */
  }

  .movie-poster {
    width: 120px;
    aspect-ratio: 2 / 3;
    border-radius: 10px 0 0 10px;
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

  .year {
    font-size: 1em;
  }
}
</style>