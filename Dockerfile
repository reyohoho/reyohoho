# Используем официальный образ Node.js версии 22.14.0 на основе Alpine (легковесный)
FROM node:22.14.0-alpine as build-stage

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем package.json и yarn.lock
COPY package.json yarn.lock ./

# Устанавливаем зависимости с помощью Yarn
RUN yarn install --frozen-lockfile

# Копируем все файлы проекта
COPY . .

# Собираем проект
RUN yarn build

# Используем легковесный образ Nginx для serving статики
FROM nginx:stable-alpine as production-stage

# Копируем собранные файлы из предыдущего этапа в Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]