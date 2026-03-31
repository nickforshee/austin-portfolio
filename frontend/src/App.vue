<template>
  <div>
    <nav class="top-nav">
      <RouterLink class="brand" to="/">Austin Kimbell</RouterLink>
      <div class="nav-links">
        <RouterLink to="/shows">Shows</RouterLink>
        <RouterLink to="/accomplishments">Accomplishments</RouterLink>
        <RouterLink to="/work">Work</RouterLink>
        <RouterLink to="/blog">Blog</RouterLink>
        <RouterLink to="/gallery">Gallery</RouterLink>
      </div>
      <RouterLink class="admin-link" to="/admin">Admin</RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
</script>
