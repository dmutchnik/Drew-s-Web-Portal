<template>
  <div id="profile-page">
    <h2>Your Profile</h2>
    <div>
      <label>Name:</label>
      <input type="text" v-model="user.name">
    </div>
    <div>
      <label>Email:</label>
      <input type="email" v-model="user.email">
    </div>
    <div>
      <label>Phone:</label>
      <input type="text" v-model="user.phone">
    </div>
    <div>
      <label>Profile Image:</label>
      <img :src="user.image" alt="Profile Image" style="max-width: 200px;">
      <div>
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
    </div>
    <div>
      <button @click="updateProfile">Save Changes</button>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      loading: false,
      images: [],
      searchQuery: '',
      selectedImage: null
    };
  },
  created() {
    // Fetch user data from the backend after login
    this.fetchUserData();
  },
  computed: {
    displayedImages() {
      return this.images.slice(0, 9); // Limit to only 9 images
    }
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await fetch('http://localhost:5000/profile', {
          method: 'GET',
          credentials: 'include' // Send cookies for authentication
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }

        const userData = await response.json();
        this.user = userData;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async updateProfile() {
      try {
        const response = await fetch('http://localhost:5000/profile', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.user.name,
            email: this.user.email,
            phone: this.user.phone,
            image: this.user.image // Include profile image in the update
          }),
          credentials: 'include' // Send cookies for authentication
        });

        if (!response.ok) {
          throw new Error('Failed to update profile');
        }

        console.log('Profile updated successfully');
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
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
      // Update user's profile image
      this.user.image = image.previewURL;
      this.selectedImage = image;
    },
    async logout() {
      try {
        const response = await fetch('http://localhost:5000/logout', {
          method: 'POST',
          credentials: 'include' // Send cookies for authentication
        });

        if (!response.ok) {
          throw new Error('Failed to logout');
        }

        // Redirect to login page after successful logout
        this.$router.push('/login');

        console.log('Logout successful');
      } catch (error) {
        console.error('Error logging out:', error);
      }
    }
  }
};
</script>

<style scoped>
#profile-page {
  font-family: 'Arial', sans-serif;
  text-align: center;
  padding: 2rem;
  background-color: #fff; /* Set white background */
  border-radius: 10px; /* Add border radius */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add shadow */
}

h2 {
  font-size: 2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input[type="text"],
input[type="email"],
input[type="password"] {
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
  margin: 0 1rem; /* Add margin to the buttons */
}

button:hover {
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
</style>
