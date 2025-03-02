<template>
    <div class="contact">
      <HeaderService />
      <div class="container">
        <div class="contact-text">
          <p>
            Если Вы владелец авторских прав, просим Вас учесть, что все плееры на сайте из сторонних API источников.
            Пишите напрямую по контактным данным этих видео-хостингов, для соблюдения DMCA. В 99% случаев они удаляют
            спорный контент в течение 24 часов. Плееры недоступные на первоисточнике априори не будут отображаться на
            ReYohoho. Или напишите на почту <a href="mailto:reyohoho@proton.me">reyohoho@proton.me</a> или в Телеграм 
            <a href="https://t.me/ReYohoho_support" target="_blank" rel="noopener noreferrer">https://t.me/ReYohoho_support</a>
          </p>
          <p>
            If you are a copyright owner, please note that all players on the site are from third-party API sources.
            Please write directly to the contact details of these video hosting sites to comply with the DMCA. In 99% of
            cases, they remove controversial content within 24 hours. Players that are not available on the original source
            will a priori not be displayed on ReYohoho. Or write to <a href="mailto:reyohoho@proton.me">reyohoho@proton.me</a> 
            or Telegram: <a href="https://t.me/ReYohoho_support" target="_blank" rel="noopener noreferrer">https://t.me/ReYohoho_support</a>
          </p>
          <p class="text-muted">
            <a href="mailto:reyohoho@proton.me">reyohoho@proton.me</a> | 
            <a href="https://t.me/ReYohoho_support" target="_blank" rel="noopener noreferrer">https://t.me/ReYohoho_support</a>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import HeaderService from '@/components/HeaderService.vue';
  
  export default {
    name: "ContactPage",
    components: {
      HeaderService,
    },
  };
  </script>
  
  <style scoped>
  .contact {
    font-family: Arial, sans-serif;
    color: #ffffff;
    margin: 0;
    padding: 0 20px 20px 20px;
  }
  
  .container {
    background-color: #333333;
    padding: 20px;
    border-radius: 5px;
    margin: 0 auto;
    max-width: 800px;
  }
  
  .contact-text {
    text-align: justify;
    margin-top: 20px;
    line-height: 1.6;
  }
  
  .contact-text a {
    color: #5bb8cc;
    text-decoration: none;
  }
  
  .contact-text a:hover {
    text-decoration: underline;
  }
  
  .text-muted {
    color: #ccc;
  }
  </style>