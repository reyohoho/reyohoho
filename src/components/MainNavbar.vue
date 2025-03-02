<template>
  <div id="app">
    <!-- Кнопка-бургер -->
    <button @click="toggleNavbar" class="burger-btn" :class="{ 'burger-btn-visible': isNavbarVisible }">
      <span v-if="isNavbarVisible">&#10005;</span> <!-- Крестик -->
      <span v-else>&#9776;</span> <!-- Символ бургера -->
    </button>

    <!-- Панель навигации -->
    <div :class="['navbar', { 'navbar-visible': isNavbarVisible }]">
      <ul>
        <!-- Внутренние ссылки -->
        <li>
          <router-link to="/" class="nav-link" @click="closeNavbar">
            <i class="fas fa-home"></i> Главная
          </router-link>
        </li>
        <li>
          <router-link to="/contact" class="nav-link" @click="closeNavbar">
            <i class="fas fa-info-circle"></i> Copyright
          </router-link>
        </li>
        <!-- Новый пункт для Топ 100 -->
        <li>
          <router-link to="/top" class="nav-link" @click="closeNavbar">
            <i class="fas fa-star"></i> Топ 100
          </router-link>
        </li>
        <!-- Внешние ссылки -->
        <li>
          <a href="https://t.me/ReYohoho/126" class="nav-link" target="_blank" rel="noopener noreferrer" @click="closeNavbar">
            <i class="fab fa-telegram"></i> Приложение
          </a>
        </li>
        <li>
          <a href="https://github.com/reyohoho/reyohoho-chrome-ff-ext/blob/master/README.MD" class="nav-link" target="_blank" rel="noopener noreferrer" @click="closeNavbar">
            <i class="fab fa-github"></i> Расширение
          </a>
        </li>
        <li>
          <a href="https://t.me/ReYohoho_Donut_Bot" class="nav-link" target="_blank" rel="noopener noreferrer" @click="closeNavbar">
            <i class="fas fa-cookie"></i> Поддержать
          </a>
        </li>
        <li>
          <a href="https://gist.github.com/reyohoho/93d835ada55bb1175b4249cbf1f1bf20" class="nav-link" target="_blank" rel="noopener noreferrer" @click="closeNavbar">
            <i class="fas fa-heart"></i> Благодарность
          </a>
        </li>
        <li>
          <a href="https://github.com/reyohoho/reyohoho" class="nav-link" target="_blank" rel="noopener noreferrer" @click="closeNavbar">
            <i class="fab fa-github"></i> Github
          </a>
        </li>
        <li>
          <a href="https://t.me/ReYohoho" class="nav-link" target="_blank" rel="noopener noreferrer" @click="closeNavbar">
            <i class="fab fa-telegram"></i> Telegram
          </a>
        </li>
        <li>
          <a href="http://45.136.199.126:3001/status/reyohoho" class="nav-link" target="_blank" rel="noopener noreferrer" @click="closeNavbar">
            <i class="fas fa-tachometer-alt"></i> Статус
          </a>
        </li>
      </ul>
    </div>

    <!-- Основной контент -->
    <div>
      <router-view></router-view> <!-- Ваш основной контент -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainNavbar',
  data() {
    return {
      isNavbarVisible: false, // Состояние видимости панели
    };
  },
  methods: {
    toggleNavbar() {
      this.isNavbarVisible = !this.isNavbarVisible; // Переключение видимости панели
    },
    closeNavbar() {
      this.isNavbarVisible = false; // Закрытие меню при клике на пункт
    }
  },
};
</script>

<style scoped>
/* Общие стили */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #ffffff; /* Белый фон */
  color: #000000; /* Черный текст */
}

/* Кнопка-бургер */
.burger-btn {
  font-size: 18px;
  background: rgba(30, 30, 30, 0.6);
  color: #ffffff; /* Белый текст */
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1001;
  transition: background-color 0.3s ease;
  border: 1px solid #ccc;
}

.burger-btn:hover {
  background-color: #555555; /* Серый при наведении */
  color: #ffffff;
}

.burger-btn-visible {
  background-color: #ffffff; /* Измененный стиль при видимости */
  color: #000000;
}

/* Панель навигации */
.navbar {
  display: flex;
  position: fixed;
  top: 0;
  left: -290px;
  height: 100%;
  width: 250px;
  background: rgba(30, 30, 30, 0.6);
  padding: 20px;
  flex-direction: column;
  box-shadow: 4px 0 8px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  transition: transform 0.3s ease;
}

.navbar-visible {
  transform: translateX(290px);
}

/* Стиль для списка навигации */
.navbar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  padding-top: 60px;
  font-size: 18px;
}

.navbar ul li {
  margin: 15px 0;
}

.navbar ul li a {
  color: #ffffff; /* Белый текст */
  text-decoration: none;
  display: flex;
  align-items: center;
  transition: color 0.3s ease;
}

.navbar ul li a:hover {
  color: #cccccc; /* Светло-серый при наведении */
}

.navbar ul li a i {
  margin-right: 10px;
}

/* Стиль для ссылок */
.nav-link {
  color: #ffffff; /* Белый текст */
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #cccccc; /* Светло-серый при наведении */
}
</style>