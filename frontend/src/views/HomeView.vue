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

      <section v-for="section in sections" :key="section.key" class="card section-block">
        <div class="section-heading">
          <h2>{{ section.label }}</h2>
          <span class="count">{{ items[section.key].length }} entries</span>
        </div>

        <p v-if="!items[section.key].length" class="empty">New work will appear here soon.</p>

        <div v-else :class="['grid', section.key === 'gallery' ? 'gallery-grid' : 'standard-grid']">
          <article v-for="item in items[section.key]" :key="item.id" class="entry">
            <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.title" loading="lazy" />
            <div class="entry-content">
              <p v-if="item.eventDate" class="entry-date">{{ formatDate(item.eventDate) }}</p>
              <h3>{{ item.title }}</h3>
              <p v-if="item.subtitle" class="entry-subtitle">{{ item.subtitle }}</p>
              <p v-if="item.summary" class="entry-summary">{{ item.summary }}</p>
              <p v-if="section.key === 'blog' && item.body" class="entry-body">{{ item.body }}</p>
              <a v-if="item.externalUrl" class="entry-link" :href="item.externalUrl" target="_blank" rel="noreferrer">
                View Resource
              </a>
            </div>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { getProfile, getPublicItems } from '../lib/api';
import { sectionLabels, type ContentItem, type Profile, type SectionKey } from '../lib/types';

const fallbackBio =
  'Theatre teacher, director, and mentor dedicated to creating brave rehearsal rooms and meaningful student performance experiences.';
const fallbackStatement =
  'This portfolio documents production leadership, classroom practice, and creative outcomes as part of Austin\'s graduate study application.';

const sectionKeys: SectionKey[] = ['shows', 'accomplishments', 'work', 'blog', 'gallery'];

const profile = ref<Profile | null>(null);
const items = reactive<Record<SectionKey, ContentItem[]>>({
  shows: [],
  accomplishments: [],
  work: [],
  blog: [],
  gallery: [],
});

const sections = sectionKeys.map((key) => ({ key, label: sectionLabels[key] }));

const heroStyle = computed(() => ({
  backgroundImage: profile.value?.heroImageUrl
    ? `linear-gradient(120deg, rgba(21, 9, 9, 0.82), rgba(26, 43, 56, 0.88)), url('${profile.value.heroImageUrl}')`
    : 'linear-gradient(120deg, #3a1614, #1e2f40)',
}));

function formatDate(value: string) {
  if (!value) return '';
  const dt = new Date(value);
  if (Number.isNaN(dt.getTime())) return value;
  return dt.toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' });
}

async function loadPage() {
  try {
    profile.value = await getProfile();
  } catch (error) {
    console.error(error);
  }

  await Promise.all(
    sectionKeys.map(async (sectionKey) => {
      try {
        items[sectionKey] = await getPublicItems(sectionKey);
      } catch (error) {
        console.error(error);
      }
    }),
  );
}

onMounted(loadPage);
</script>
