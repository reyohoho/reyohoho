<template>
  <div v-if="movieInfo" class="movie-info">
    <div class="movie-details">
      <!-- Постер фильма -->
      <div class="movie-poster">
        <img :src="movieInfo.poster_url" :alt="movieInfo.name_ru" class="poster-image" />
      </div>

      <!-- Описание фильма -->
      <div class="movie-description">
        <h1 class="movie-title">{{ movieInfo.name_ru }}</h1>
        <p v-if="movieInfo.name_en" class="movie-subtitle">{{ movieInfo.name_en }}</p>

        <div class="movie-meta">
          <p v-if="movieInfo.year" class="meta-item">Год: {{ movieInfo.year }} г.</p>
          <p v-if="movieInfo.rating_kinopoisk" class="meta-item">Рейтинг Кинопоиск: {{ movieInfo.rating_kinopoisk }}/10</p>
          <p v-if="movieInfo.rating_imdb" class="meta-item">Рейтинг IMDb: {{ movieInfo.rating_imdb }}/10</p>
        </div>

        <p v-if="movieInfo.description" class="movie-description-text">{{ movieInfo.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const apiUrl = import.meta.env.VITE_APP_API_URL;

export default {
  name: 'MovieInfo',
  props: {
    movieId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      movieInfo: null,
    };
  },
  async mounted() {
    try {
      const response = await axios.get(`${apiUrl}/kp_info/${this.movieId}`);
      this.movieInfo = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке информации о фильме:', error);
    }
  },
};
</script>

<style scoped>
.movie-info {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  margin: 20px auto;
  max-width: 1200px;
}

.movie-details {
  display: flex;
  align-items: flex-start;
  gap: 40px;
  width: 100%;
  flex-wrap: wrap;
}

.movie-poster {
  max-width: 300px;
  width: 100%;
  height: auto;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.poster-image {
  width: 100%;
  height: auto;
  display: block;
}

.movie-description {
  flex: 1;
  color: #f5f5f5;
  max-width: 800px;
}

.movie-title {
  margin: 0 0 10px 0;
  font-size: 32px;
  font-weight: bold;
  color: #fff;
}

.movie-subtitle {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #bbb;
}

.movie-meta {
  margin-bottom: 25px;
}

.meta-item {
  margin: 8px 0;
  font-size: 18px;
  color: #ddd;
}

.movie-description-text {
  font-size: 18px;
  line-height: 1.6;
  color: #ccc;
  margin: 0;
}

/* Адаптивные стили для маленьких экранов */
@media (max-width: 768px) {
  .movie-details {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .movie-poster {
    max-width: 100%;
    margin-bottom: 20px;
  }

  .movie-description {
    text-align: center;
  }

  .movie-title {
    font-size: 28px;
  }

  .movie-subtitle {
    font-size: 18px;
  }

  .meta-item {
    font-size: 16px;
  }

  .movie-description-text {
    font-size: 16px;
  }
}
</style>