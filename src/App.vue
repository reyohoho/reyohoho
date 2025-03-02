<template>
  <div id="app">
    <!-- Фоновый компонент -->
    <BackgroundSpace />
    <MainNavbar />
  </div>
</template>

<script>
import BackgroundSpace from '@/components/BackgroundSpace.vue';
import MainNavbar from '@/components/MainNavbar.vue';

export default {
  name: 'App',
  components: {
    BackgroundSpace,
    MainNavbar,
  },
};
</script>

<style>
/* Стили для основного контента */
#app {
  position: relative;
  z-index: 1;
}

/* Подключение локального шрифта */
@font-face {
  font-family: 'MyCustomFont';
  src: url('@/assets/fonts/memSYaGs126MiZpBA-UvWbX2vVnXBbObj2OVZyOOSr4dVJWUgsjZ0C4n.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'MyCustomFont2';
  src: url('@/assets/fonts/q5uGsou0JOdh94bvug.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

/* Применение шрифтов в приложении */
body {
  font-family: 'MyCustomFont', sans-serif; /* Применяем шрифт по умолчанию */
  color: #fff;
  background-color: #000;
  margin: 0;
  padding: 0;
}

</style>
