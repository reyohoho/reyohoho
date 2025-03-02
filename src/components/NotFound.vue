<template>
  <div class="error-page">
    <!-- Заголовок -->
    <HeaderService />

    <!-- Контент страницы ошибки -->
    <div class="error-content">
      <h1>400 — Ошибка запроса</h1>
      <p>Что-то пошло не так. Проверьте введенные данные и попробуйте снова.</p>
      <button @click="goToHome" class="home-button">На главную</button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import HeaderService from '@/components/HeaderService.vue'; // Импортируем заголовок

export default {
  name: 'RedirectError400',
  components: {
    HeaderService, // Регистрируем заголовок
  },
  setup() {
    const router = useRouter();

    // Функция для перехода на главную страницу
    const goToHome = () => {
      router.push('/');
    };

    return {
      goToHome,
    };
  },
};
</script>

<style scoped>
/* Общие стили для страницы ошибки */
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #000; /* Черный фон */
  color: #fff; /* Белый текст */
  text-align: center;
}

/* Контент страницы ошибки */
.error-content {
  max-width: 600px;
  padding: 20px;
  background-color: #1a1a1a; /* Темно-серый фон для контента */
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.error-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #fff; /* Белый текст */
}

.error-content p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #ccc; /* Светло-серый текст */
}

/* Стили для кнопки "На главную" */
.home-button {
  background-color: #333; /* Темно-серый фон */
  color: #fff; /* Белый текст */
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.home-button:hover {
  background-color: #555; /* Серый фон при наведении */
}
</style>