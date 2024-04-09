<template>
    <div id="login-form">
      <h2>Login</h2>
      <form @submit.prevent="loginUser">
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="formData.email" required>
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="formData.password" required>
        </div>
        <div>
          <button type="submit">Login</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        formData: {
          email: '',
          password: ''
        }
      };
    },
    methods: {
      async loginUser() {
        try {
          const response = await axios.post('http://localhost:5000/login', this.formData, {
            headers: {
              'Content-Type': 'application/json',
            },
            withCredentials: true // Include cookies in the request
          });
  
          if (response.status !== 200) {
            throw new Error('Login failed');
          }
  
          console.log('Login successful');
  
          // Fetch session data to confirm login success and handle session cookies
          const sessionResponse = await axios.get('http://localhost:5000/session', {
            withCredentials: true // Include cookies in the request
          });
  
          // Redirect the user to the profile page after successful login
          this.$router.push('/profile');
        } catch (error) {
          console.error('Error logging in:', error);
          // Handle login error
        }
      }
    }
  };
  </script>
  
  <style scoped>
  #login-form {
    font-family: 'Arial', sans-serif;
    text-align: center;
    padding: 2rem;
    background-color: #fff; /* Set white background */
    border-radius: 10px; /* Add border radius */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add shadow */
  }
  
  h2 {
    font-size: 2rem;
    color: #007bff;
  }
  
  form {
    margin-top: 2rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  input {
    padding: 0.5rem;
    margin-bottom: 1rem;
    font-size: 1rem;
    border: 2px solid #007bff; /* Blue border */
    background-color: transparent; /* Transparent background */
    color: #007bff; /* Blue text color */
    border-radius: 5px;
    width: 100%;
    max-width: 300px; /* Adjust the maximum width as needed */
  }
  
  button {
    padding: 0.5rem 2rem;
    font-size: 1rem;
    border: none;
    border-radius: 10px;
    background-color: #007bff; /* Blue color for button */
    color: #fff; /* White text color */
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #0056b3; /* Darker blue on hover */
  }
  </style>
  