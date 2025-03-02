<template>
  <header class="site-header">
    <router-link to="/" class="home-link">
      <h1>Reyohoho</h1>
      <img src="@/assets/basedge.png" alt="Base Edge" class="header-image" />
    </router-link>
  </header>
</template>

<script>
export default {
  name: 'HeaderService',
};
</script>

<style scoped>
/* Заголовок */
.site-header {
  display: flex;
  align-items: center; /* Выравнивание по вертикали */
  justify-content: center;
  padding: 5px 27px 27px 27px;
  color: #fff;
}

/* Картинка и заголовок как ссылка */
.home-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit; /* Убираем стандартное подчеркивание и цвет ссылки */
}

/* Картинка слева */
.header-image {
  width: 70px; /* Размер картинки */
  height: auto;
  margin-left: 20px; /* Отступ между картинкой и заголовком */
}

/* Стили для заголовка */
.site-header h1 {
  font-family: 'MyCustomFont2', sans-serif;
  font-size: 64px;
  margin: 0;
}

/* Адаптивность */
@media (max-width: 768px) {
  .site-header {
    flex-direction: column; /* Ставим заголовок и картинку вертикально */
    padding: 20px 15px 15px 15px;
  }

  .site-header h1 {
    font-size: 48px; /* Уменьшаем размер заголовка для мобильных */
  }

  .header-image {
    width: 50px; /* Уменьшаем размер картинки */
    margin-left: 0;
    margin-top: 10px;
  }
}

@media (max-width: 480px) {
  .site-header h1 {
    font-size: 36px; /* Еще больше уменьшаем заголовок */
  }

  .header-image {
    width: 40px; /* Уменьшаем картинку для маленьких экранов */
  }
}
</style>
