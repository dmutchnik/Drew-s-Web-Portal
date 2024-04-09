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
        <button type="submit" class="button">Register</button>
      </div>
    </form>
  </div>
</template>

<script>
import mandrill from 'mandrill-api/Mandrill';

export default {
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: '',
        phone: '',
        image: null // Hold the selected Pixabay image URL
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
      return this.images.slice(0, 9); // Limit to only 9 images
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
        // Reset images when search query is empty
        this.images = [];
      }
    },
    selectImage(image) {
      // Handle image selection
      console.log('Selected image:', image);
      // Update form data with selected image
      this.formData.image = image.previewURL;
      this.selectedImage = image;
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
          body: formData // Send form data directly
        });

        if (!response.ok) {
          this.emailExists = true;
          return;
        }

        // Clear form data after successful registration
        this.formData = {
          name: '',
          email: '',
          password: '',
          phone: '',
          image: null
        };

        // Redirect user to login page after successful registration
        this.$router.push('/login');

        console.log('User registered successfully');
      } catch (error) {
        console.error('Error registering user:', error);
        // Handle error
      }
    }
  }
};
</script>

<style scoped>
#registration-form {
  font-family: 'Arial', sans-serif;
  text-align: center;
  padding: 1rem;
  background-color: #fff; /* Set white background */
  color: #333; /* Set dark text color */
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); /* Add shadow for depth */
}

h2 {
  font-size: 2rem; /* Smaller font size */
  margin-bottom: 2rem; /* Add space below the title */
  color: #007bff; /* Blue color for the title */
}

.form-group {
  margin-bottom: 1rem; /* Add space between form elements */
  text-align: center; /* Align form labels to the left */
}

label {
  display: block; /* Display labels as block elements */
  margin-bottom: 0.5rem; /* Add space below labels */
}

input {
  padding: 0.5rem; /* Reduce input padding */
  font-size: 1rem; /* Smaller font size for inputs */
  border: 2px solid #007bff; /* Blue border */
  border-radius: 5px; /* Rounded corners */
  color: #007bff; /* Blue text color */
  width: 30%; /* Full width */
  box-sizing: border-box; /* Include padding in the width */
}

.button {
  padding: 0.5rem 2rem; /* Adjust button padding */
  font-size: 1rem; /* Smaller font size for button */
  border: none;
  border-radius: 10px;
  background-color: #007bff; /* Blue color for submit button */
  color: #fff; /* White text color */
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}

.pixabay-images {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.pixabay-images img {
  width: 50%;
  max-height: 100px; /* Limit the height */
  object-fit: cover; /* Maintain aspect ratio */
  cursor: pointer;
}

.pixabay-images .selected img {
  border: 2px solid blue;
}

.button-container {
  display: flex;
  justify-content: center;
}

.error-message {
  color: red;
  margin-top: 0.5rem;
}
</style>