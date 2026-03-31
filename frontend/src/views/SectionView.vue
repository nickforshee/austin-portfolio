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
      <section class="card section-block section-surface">
        <div class="section-heading">
          <p class="section-count-label">{{ items.length }} entries</p>
          <RouterLink v-if="adminAuthenticated" class="inline-admin-link" to="/admin">Edit in Admin</RouterLink>
        </div>

        <p v-if="!items.length" class="empty">No entries yet. Add content from the admin page.</p>

        <div v-else :class="['grid', section === 'gallery' ? 'gallery-grid' : 'standard-grid']">
          <article
            v-for="item in items"
            :key="item.id"
            class="entry"
            :class="{ 'entry-gallery': section === 'gallery' }"
          >
            <button
              v-if="item.imageUrl && section === 'gallery'"
              class="image-button"
              type="button"
              @click="openLightbox(item)"
            >
              <img :src="item.imageUrl" :alt="item.title" loading="lazy" />
            </button>
            <img v-else-if="item.imageUrl" :src="item.imageUrl" :alt="item.title" loading="lazy" />
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

    <div
      v-if="lightboxItem"
      class="lightbox"
      role="dialog"
      aria-modal="true"
      :aria-label="lightboxItem.title"
      @click.self="closeLightbox"
    >
      <button class="lightbox-close" type="button" @click="closeLightbox">Close</button>
      <figure class="lightbox-figure">
        <img :src="lightboxItem.imageUrl || ''" :alt="lightboxItem.title" />
        <figcaption>
          <h3>{{ lightboxItem.title }}</h3>
          <p v-if="lightboxItem.subtitle">{{ lightboxItem.subtitle }}</p>
        </figcaption>
      </figure>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { RouterLink } from 'vue-router';
import { getPublicItems } from '../lib/api';
import { isAdminAuthenticated } from '../lib/auth';
import { sectionLabels, type ContentItem, type SectionKey } from '../lib/types';

const props = defineProps<{ section: SectionKey }>();

const items = ref<ContentItem[]>([]);
const lightboxItem = ref<ContentItem | null>(null);
const adminAuthenticated = ref(false);

const sectionDescriptions: Record<SectionKey, string> = {
  shows: 'Productions Austin has directed, taught, or staged with student ensembles.',
  accomplishments: 'Awards, milestones, and outcomes that reflect measurable student growth.',
  work: 'Lesson design, rehearsal frameworks, and instructional artifacts from the classroom.',
  blog: 'Short reflections on theatre pedagogy, collaboration, and process-driven learning.',
  gallery: 'Production photos and rehearsal moments that capture ensemble storytelling.',
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

function openLightbox(item: ContentItem) {
  lightboxItem.value = item;
}

function closeLightbox() {
  lightboxItem.value = null;
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    closeLightbox();
  }
}

function syncAdminAuth() {
  adminAuthenticated.value = isAdminAuthenticated();
}

watch(() => props.section, loadItems);
onMounted(loadItems);
onMounted(syncAdminAuth);
onMounted(() => window.addEventListener('keydown', onKeydown));
onMounted(() => window.addEventListener('storage', syncAdminAuth));
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown));
onBeforeUnmount(() => window.removeEventListener('storage', syncAdminAuth));
</script>
