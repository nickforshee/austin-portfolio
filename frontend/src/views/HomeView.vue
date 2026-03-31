<template>
  <div class="page">
    <header class="hero" :style="heroStyle">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <p class="eyebrow">Austin Kimbell Portfolio</p>
        <h1>{{ profile?.fullName || 'Austin Kimbell' }}</h1>
        <p class="hero-title">{{ profile?.title || 'Theatre Educator' }}</p>
        <p class="hero-bio">{{ profile?.bio || fallbackBio }}</p>
      </div>
    </header>

    <main class="content-wrap">
      <section class="statement card">
        <h2>Graduate Program Statement</h2>
        <p>{{ profile?.programStatement || fallbackStatement }}</p>
      </section>

      <section class="card section-block">
        <div class="section-heading">
          <h2>Explore Portfolio Sections</h2>
        </div>

        <div class="section-nav-grid">
          <RouterLink v-for="link in sectionLinks" :key="link.to" class="section-link-card" :to="link.to">
            <h3>{{ link.title }}</h3>
            <p>{{ link.description }}</p>
          </RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { getProfile } from '../lib/api';
import type { Profile } from '../lib/types';

const fallbackBio =
  'Theatre teacher, director, and mentor dedicated to creating brave rehearsal rooms and meaningful student performance experiences.';
const fallbackStatement =
  'This portfolio documents production leadership, classroom practice, and creative outcomes as part of Austin\'s graduate study application.';

const profile = ref<Profile | null>(null);

const sectionLinks = [
  {
    to: '/shows',
    title: 'Past Shows',
    description: 'Selected productions with artistic goals, process notes, and student impact.',
  },
  {
    to: '/accomplishments',
    title: 'Accomplishments',
    description: 'Recognition, leadership milestones, and outcomes tied to program growth.',
  },
  {
    to: '/work',
    title: 'Teaching Work',
    description: 'Curriculum samples, rehearsal structures, and evidence of instructional design.',
  },
  {
    to: '/blog',
    title: 'Blog',
    description: 'Reflective writing on pedagogy, rehearsal culture, and student development.',
  },
  {
    to: '/gallery',
    title: 'Photo Gallery',
    description: 'Visual documentation from performances, tech week, and rehearsal spaces.',
  },
];

const heroStyle = computed(() => ({
  backgroundImage: profile.value?.heroImageUrl
    ? `linear-gradient(120deg, rgba(21, 9, 9, 0.82), rgba(26, 43, 56, 0.88)), url('${profile.value.heroImageUrl}')`
    : 'linear-gradient(120deg, #3a1614, #1e2f40)',
}));

onMounted(async () => {
  try {
    profile.value = await getProfile();
  } catch (error) {
    console.error(error);
  }
});
</script>
