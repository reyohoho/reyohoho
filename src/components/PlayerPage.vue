<template>
  <div class="player-page">
    <!-- Фоновый постер с размытием -->
    <div class="background-poster" :style="posterStyle"></div>

    <!-- Основной контент -->
    <div class="content">
      <HeaderService />

      <!-- Сообщение об ошибке -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- Карточка с плеером и информацией -->
      <div v-if="movieInfo" class="movie-card">
        <!-- Название фильма -->
        <div class="movie-header">
          <h1 class="movie-title">{{ movieInfo.name_ru }}</h1>
          <p v-if="movieInfo.name_en" class="movie-subtitle">{{ movieInfo.name_en }}</p>
        </div>

        <!-- Выбор плеера -->
        <div class="players-list">
          <span>Плеер: </span>
          <select v-model="selectedPlayer" id="player-select">
            <option v-for="(player, index) in players" :key="index" :value="player">
              {{ player.translate }}
            </option>
          </select>
        </div>

        <!-- Плеер -->
        <div v-if="selectedPlayer" class="player-container">
          <div class="iframe-container">
            <iframe
              v-show="!iframeLoading"
              :src="selectedPlayer.iframe"
              frameborder="0"
              @load="onIframeLoad"
              allowfullscreen
              class="responsive-iframe"
            ></iframe>
          </div>
          <!-- Спиннер загрузки -->
          <div v-if="iframeLoading" class="spinner"></div>
        </div>

        <!-- Информация о фильме -->
        <div class="movie-info">
          <div class="movie-meta">
            <p v-if="movieInfo.year" class="meta-item">Год: {{ movieInfo.year }} г.</p>
            <p v-if="movieInfo.rating_kinopoisk" class="meta-item">Кинопоиск: {{ movieInfo.rating_kinopoisk }}/10</p>
            <p v-if="movieInfo.rating_imdb" class="meta-item">IMDb: {{ movieInfo.rating_imdb }}/10</p>
          </div>

          <p v-if="movieInfo.description" class="movie-description-text">{{ movieInfo.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref, onMounted, computed } from 'vue';
import HeaderService from '@/components/HeaderService.vue';

export default {
  name: 'PlayerPage',
  components: {
    HeaderService,
  },
  setup() {
    const route = useRoute();
    const movieId = ref(route.params.kp_id);
    const players = ref([]);
    const selectedPlayer = ref(null);
    const loading = ref(false);
    const iframeLoading = ref(false);
    const errorMessage = ref('');
    const movieInfo = ref(null);
    const apiUrl = import.meta.env.VITE_APP_API_URL;

    const onIframeLoad = () => {
      iframeLoading.value = false;
    };

    const sortPlayersAlphabetically = (players) => {
      return players.sort((a, b) => a.translate.localeCompare(b.translate));
    };

    const fetchMovieInfo = async () => {
      try {
        const response = await axios.get(`${apiUrl}/kp_info/${movieId.value}`);
        movieInfo.value = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке информации о фильме:', error);
      }
    };

    onMounted(async () => {
      loading.value = true;
      errorMessage.value = '';
      try {
        const response = await axios.post(`${apiUrl}/cache`, 
          new URLSearchParams({
            kinopoisk: movieId.value,
            type: 'movie',
          }),
          {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          }
        );

        const sortedPlayers = sortPlayersAlphabetically(Object.values(response.data));
        players.value = sortedPlayers;
        selectedPlayer.value = players.value[0];
        iframeLoading.value = true;
      } catch (error) {
        if (error.response && error.response.status === 403) {
          errorMessage.value = 'Упс, у нас это недоступно =(';
        } else {
          errorMessage.value = 'Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.';
        }
        console.error('Ошибка при загрузке плееров:', error);
      } finally {
        loading.value = false;
      }

      await fetchMovieInfo();
    });

    // Стиль для фонового постера
    const posterStyle = computed(() => {
      if (movieInfo.value?.poster_url) {
        return {
          backgroundImage: `url(${movieInfo.value.poster_url})`,
        };
      }
      return {};
    });

    return {
      players,
      selectedPlayer,
      loading,
      iframeLoading,
      errorMessage,
      onIframeLoad,
      movieId,
      movieInfo,
      posterStyle,
    };
  },
};
</script>

<style scoped>
.player-page {
  position: relative;
  min-height: 100vh;
  background-color: #0a0a0a;
  color: #fff;
  overflow: hidden;
}

.background-poster {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  filter: blur(20px) brightness(0.5);
  z-index: 1;
}

.content {
  position: relative;
  z-index: 2;
  padding: 0 4px 20px 4px;
  max-width: 1200px;
  margin: 0 auto;
}

.movie-card {
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  padding: 20px;
}

.movie-header {
  text-align: center;
  margin-bottom: 20px;
}

.movie-title {
  font-size: 36px;
  margin-bottom: 10px;
  margin-top: 0px;
}

.movie-subtitle {
  font-size: 20px;
  color: #bbb;
}

.players-list {
  width: 100%;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
}

#player-select {
  background-color: #333333;
  color: white;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: background-color 0.3s;
}

#player-select:hover {
  background-color: #333333;
}

#player-select:focus {
  border-color: #3498db;
}

.player-container {
  position: relative;
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
}

.iframe-container {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  height: 0;
  overflow: hidden;
}

.responsive-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.movie-info {
  color: #fff;
}

.movie-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.meta-item {
  font-size: 16px;
  color: #ddd;
}

.movie-description-text {
  font-size: 16px;
  line-height: 1.6;
  color: #ccc;
}

.error-message {
  color: #ff4444;
  background-color: rgba(255, 230, 230, 0.1);
  padding: 10px;
  border-radius: 5px;
  margin: 20px auto;
  max-width: 400px;
  border: 1px solid #ff4444;
}

@media (max-width: 600px) {
  .movie-card{
    padding: 10px;
  }

  .movie-title {
    font-size: 28px;
  }

  .movie-subtitle {
    font-size: 16px;
  }

  .movie-meta {
    flex-direction: column;
    gap: 10px;
  }

  .meta-item {
    font-size: 14px;
    padding: 0;
    margin: 0;
  }

  .movie-description-text {
    font-size: 14px;
  }

#player-select {
  width: 100%;
}

.player-container {
  position: relative;
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
}

.iframe-container {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  height: 0;
  overflow: hidden;
}

.responsive-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}
}
</style>