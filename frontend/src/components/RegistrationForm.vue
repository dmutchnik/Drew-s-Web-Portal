<template>
  <div id="registration-form">
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="formData.name" required>
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="formData.email" required>
        <p v-if="emailExists" class="error-message">Email already exists. Please use a different email.</p>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="formData.password" required>
      </div>
      <div class="form-group">
        <label for="phone">Phone:</label>
        <input type="text" id="phone" v-model="formData.phone">
      </div>
      <div class="form-group">
        <label for="search">Search Pixabay Images:</label>
        <input type="text" id="search" v-model="searchQuery" @input="searchImages" placeholder="Enter search query">
      </div>
      <div class="pixabay-images">
        <div
          v-for="image in displayedImages"
          :key="image.id"
          @click="selectImage(image)"
          :class="{ 'selected': image === selectedImage }"
        >
          <img :src="image.previewURL" alt="Pixabay Image">
        </div>
      </div>
      <div class="form-group">
        <button type="submit" class="submit-button">Register</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: '',
        phone: '',
        image: null
      },
      loading: false,
      images: [],
      searchQuery: '',
      selectedImage: null,
      emailExists: false
    };
  },
  computed: {
    displayedImages() {
      return this.images.slice(0, 9);
    }
  },
  methods: {
    async searchImages() {
      if (this.searchQuery.length > 0) {
        try {
          this.loading = true;
          const response = await fetch(`https://pixabay.com/api/?key=43280780-f8b60b2735b8aef78f0215ac4&q=${encodeURIComponent(this.searchQuery)}`);
          const data = await response.json();
          this.images = data.hits;
          this.loading = false;
        } catch (error) {
          console.error('Error fetching images:', error);
          this.loading = false;
        }
      } else {
        this.images = [];
      }
    },
    async registerUser() {
      try {
        const formData = new FormData();
        formData.append('name', this.formData.name);
        formData.append('email', this.formData.email);
        formData.append('password', this.formData.password);
        formData.append('phone', this.formData.phone);
        formData.append('image', this.formData.image);

        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          this.emailExists = true;
          return;
        }

        this.formData = {
          name: '',
          email: '',
          password: '',
          phone: '',
          image: null
        };

        this.$router.push('/login');

        console.log('User registered successfully');
      } catch (error) {
        console.error('Error registering user:', error);
      }
    }
  }
};
</script>

<style scoped>
#registration-form {
  font-family: 'Arial', sans-serif;
  text-align: center;
  padding: 2rem;
  background-color: #fff;
  color: #333;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #007bff;
}

.form-group {
  margin-bottom: 1rem;
  text-align: center;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input {
  padding: 0.5rem;
  font-size: 1rem;
  border: 2px solid #007bff;
  border-radius: 5px;
  width: 30%;
  box-sizing: border-box;
}

input[type="submit"],
.submit-button {
  padding: 0.5rem 2rem;
  font-size: 1rem;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border: none;
  border-radius: 10px;
}

input[type="submit"]:hover,
.submit-button:hover {
  background-color: #0056b3;
}

.pixabay-images {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.pixabay-images img {
  width: 50%;
  max-height: 100px;
  object-fit: cover;
  cursor: pointer;
}

.pixabay-images .selected img {
  border: 2px solid blue;
}

.error-message {
  color: red;
  margin-top: 0.5rem;
}
</style>