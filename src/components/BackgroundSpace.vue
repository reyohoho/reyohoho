<template>
  <div>
    <!-- Фон с постером топ-1 фильма -->
    <div v-if="!isMobile" class="background-container" :style="backgroundStyle">
      <!-- Размытый и приглушённый фон -->
      <div class="blur-overlay"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

// Данные топ-1 фильма
const topMovie = ref(null);

// Стиль для фона
const backgroundStyle = computed(() => ({
  backgroundImage: `url(${topMovie.value?.cover})`,
}));

// Загрузка данных топ-1 фильма
const fetchTopMovie = async () => {
  try {
    // Запрос к API для получения топ-100 фильмов за 24 часа
    const response = await fetch('https://rh.aukus.su/top/24h', { priority: 'high' });
    const data = await response.json();
    if (data && data.length > 0) {
      // Берём первый фильм из списка (топ-1)
      topMovie.value = data[0];
      // Динамически добавляем preload для фонового изображения
      const preloadLink = document.createElement('link');
      preloadLink.rel = 'preload';
      preloadLink.href = topMovie.value.cover;
      preloadLink.as = 'image';
      document.head.appendChild(preloadLink);
    }
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
};

onMounted(() => {
  fetchTopMovie(); // Загружаем данные топ-1 фильма
});
</script>

<style scoped>
/* Убираем отступы и полосы прокрутки */
html, body {
  margin: 0;
  padding: 0;
  overflow: hidden; /* Убираем полосы прокрутки */
}

/* Контейнер для фона */
.background-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw; /* Ширина ровно по экрану */
  height: 100vh; /* Высота ровно по экрану */
  background-size: cover;
  background-position: center;
  z-index: -1;
}

/* Размытый и приглушённый оверлей */
.blur-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(20px); /* Увеличиваем размытие */
  background: rgba(0, 0, 0, 0.7); /* Усиливаем затемнение */
}
</style>