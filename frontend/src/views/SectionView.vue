<template>
  <div class="page">
    <header class="section-hero">
      <div class="hero-content compact">
        <p class="eyebrow">Austin Kimbell Portfolio</p>
        <h1>{{ sectionLabels[section] }}</h1>
        <p class="hero-bio">{{ sectionDescriptions[section] }}</p>
      </div>
    </header>

    <main class="content-wrap section-page-wrap">
      <section class="card section-block">
        <div class="section-heading">
          <h2>{{ sectionLabels[section] }}</h2>
          <span class="count">{{ items.length }} entries</span>
        </div>

        <p v-if="!items.length" class="empty">No entries yet. Add content from the admin page.</p>

        <div v-else :class="['grid', section === 'gallery' ? 'gallery-grid' : 'standard-grid']">
          <article v-for="item in items" :key="item.id" class="entry">
            <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.title" loading="lazy" />
            <div class="entry-content">
              <p v-if="item.eventDate" class="entry-date">{{ formatDate(item.eventDate) }}</p>
              <h3>{{ item.title }}</h3>
              <p v-if="item.subtitle" class="entry-subtitle">{{ item.subtitle }}</p>
              <p v-if="item.summary" class="entry-summary">{{ item.summary }}</p>
              <p v-if="section === 'blog' && item.body" class="entry-body">{{ item.body }}</p>
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
import { onMounted, ref, watch } from 'vue';
import { getPublicItems } from '../lib/api';
import { sectionLabels, type ContentItem, type SectionKey } from '../lib/types';

const props = defineProps<{ section: SectionKey }>();

const items = ref<ContentItem[]>([]);

const sectionDescriptions: Record<SectionKey, string> = {
  shows: 'Direction and production work from recent school theatre seasons.',
  accomplishments: 'Awards, recognitions, and measurable program outcomes.',
  work: 'Curriculum design, classroom strategies, and creative teaching artifacts.',
  blog: 'Reflections on theatre pedagogy, rehearsal process, and student growth.',
  gallery: 'Visual highlights from productions, rehearsals, and backstage moments.',
};

function formatDate(value: string) {
  if (!value) return '';
  const dt = new Date(value);
  if (Number.isNaN(dt.getTime())) return value;
  return dt.toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' });
}

async function loadItems() {
  try {
    items.value = await getPublicItems(props.section);
  } catch (error) {
    console.error(error);
    items.value = [];
  }
}

watch(() => props.section, loadItems);
onMounted(loadItems);
</script>
