<template>
    <div id="profile-app">
      <header>
        <img src="./assets/logo.jpeg" alt="Company Logo" class="logo" />
        <h1>Drew's Web Portal</h1>
      </header>
      <main>
        <div class="button-container">
          <router-link to="/register" class="button">Register</router-link>
          <router-link to="/login" class="button">Login</router-link>
        </div>
        <router-view></router-view>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ProfileApp'
  }
  </script>
  
  <style scoped>
  #profile-app {
    font-family: 'Arial', sans-serif;
    text-align: center;
    padding: 1rem;
    background-color: rgb(255, 255, 255);
    color: #333;
  }
  
  header {
    margin-bottom: 0.5rem;
  }
  
  .logo {
    width: 120px;
    height: auto;
  }
  
  h1 {
    font-size: 2rem;
    font-weight: bold;
    color: #007bff;
  }
  
  .button-container {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
  }
  
  .button {
    padding: 1rem 2rem;
    margin: 0 1rem;
    font-size: 1rem;
    border: 2px solid #007bff;
    border-radius: 20px;
    background-color: transparent;
    color: #007bff;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease;
  }
  
  .button:hover {
    background-color: #007bff;
    color: #fff;
    transform: scale(1.05);
  }
  
  .router-link-active {
    font-weight: bold;
    text-decoration: underline;
  }
  </style>
