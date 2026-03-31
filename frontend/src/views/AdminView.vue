<template>
  <div class="admin-page">
    <header class="admin-header">
      <h1>Portfolio Admin</h1>
      <RouterLink class="back-link" to="/">Back to Portfolio</RouterLink>
    </header>

    <section v-if="!token" class="admin-card login-card">
      <h2>Sign in</h2>
      <p>Use the admin credentials configured in the Flask backend.</p>
      <form @submit.prevent="handleLogin" class="form-grid">
        <label>
          Username
          <input v-model="credentials.username" type="text" required />
        </label>
        <label>
          Password
          <input v-model="credentials.password" type="password" required />
        </label>
        <button type="submit">Log In</button>
      </form>
    </section>

    <div v-else class="admin-layout">
      <section class="admin-card profile-card">
        <div class="title-row">
          <h2>Profile</h2>
          <button class="ghost" @click="logout">Log Out</button>
        </div>

        <form class="form-grid" @submit.prevent="saveProfile">
          <label>
            Full Name
            <input v-model="profileForm.fullName" required />
          </label>
          <label>
            Title
            <input v-model="profileForm.title" required />
          </label>
          <label>
            Contact Email
            <input v-model="profileForm.email" type="email" />
          </label>
          <label>
            Hero Image URL
            <input v-model="profileForm.heroImageUrl" type="url" />
          </label>
          <label>
            Bio
            <textarea v-model="profileForm.bio" rows="4" required></textarea>
          </label>
          <label>
            Program Statement
            <textarea v-model="profileForm.programStatement" rows="4" required></textarea>
          </label>
          <button type="submit">Save Profile</button>
        </form>
      </section>

      <section class="admin-card content-card">
        <div class="title-row">
          <h2>Content Manager</h2>
          <select v-model="activeSection" @change="loadAdminItems">
            <option v-for="option in sections" :key="option" :value="option">
              {{ sectionLabels[option] }}
            </option>
          </select>
        </div>

        <form class="form-grid" @submit.prevent="saveItem">
          <label>
            Title
            <input v-model="itemForm.title" required />
          </label>
          <label>
            Subtitle
            <input v-model="itemForm.subtitle" />
          </label>
          <label>
            Event Date
            <input v-model="itemForm.eventDate" type="date" />
          </label>
          <label>
            Image URL
            <input v-model="itemForm.imageUrl" type="url" />
          </label>
          <label>
            External URL
            <input v-model="itemForm.externalUrl" type="url" />
          </label>
          <label>
            Tags
            <input v-model="itemForm.tags" placeholder="comma, separated" />
          </label>
          <label>
            Summary
            <textarea v-model="itemForm.summary" rows="3"></textarea>
          </label>
          <label>
            Body
            <textarea v-model="itemForm.body" rows="5"></textarea>
          </label>
          <label class="checkbox-row">
            <input v-model="itemForm.published" type="checkbox" />
            Published
          </label>
          <div class="button-row">
            <button type="submit">{{ editingId ? 'Update Entry' : 'Create Entry' }}</button>
            <button v-if="editingId" type="button" class="ghost" @click="resetItemForm">Cancel Edit</button>
          </div>
        </form>

        <ul class="content-list">
          <li v-for="item in adminItems" :key="item.id">
            <div>
              <p class="item-title">{{ item.title }}</p>
              <p class="item-meta">{{ item.eventDate || 'No date' }} � {{ item.published ? 'Published' : 'Draft' }}</p>
            </div>
            <div class="list-actions">
              <button class="ghost" @click="editItem(item)">Edit</button>
              <button class="danger" @click="removeItem(item.id)">Delete</button>
            </div>
          </li>
        </ul>
      </section>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { createItem, deleteItem, getAdminItems, getProfile, login, updateItem, updateProfile } from '../lib/api';
import { TOKEN_KEY } from '../lib/auth';
import { sectionLabels, type ContentItem, type EditableItem, type Profile, type SectionKey } from '../lib/types';

const sections: SectionKey[] = ['shows', 'accomplishments', 'work', 'blog', 'gallery'];

const token = ref(localStorage.getItem(TOKEN_KEY) || '');
const error = ref('');
const message = ref('');
const activeSection = ref<SectionKey>('shows');
const adminItems = ref<ContentItem[]>([]);
const editingId = ref<number | null>(null);

const credentials = reactive({ username: '', password: '' });

const profileForm = reactive<Profile>({
  fullName: '',
  title: '',
  bio: '',
  programStatement: '',
  heroImageUrl: '',
  email: '',
});

const itemForm = reactive<EditableItem>({
  section: 'shows',
  title: '',
  subtitle: '',
  summary: '',
  body: '',
  imageUrl: '',
  externalUrl: '',
  eventDate: '',
  tags: '',
  published: true,
});

function clearNotices() {
  error.value = '';
  message.value = '';
}

function resetItemForm() {
  editingId.value = null;
  itemForm.section = activeSection.value;
  itemForm.title = '';
  itemForm.subtitle = '';
  itemForm.summary = '';
  itemForm.body = '';
  itemForm.imageUrl = '';
  itemForm.externalUrl = '';
  itemForm.eventDate = '';
  itemForm.tags = '';
  itemForm.published = true;
}

function logout() {
  token.value = '';
  localStorage.removeItem(TOKEN_KEY);
  adminItems.value = [];
  resetItemForm();
  clearNotices();
}

async function handleLogin() {
  clearNotices();
  try {
    token.value = await login(credentials.username, credentials.password);
    localStorage.setItem(TOKEN_KEY, token.value);
    await bootstrapAdmin();
    message.value = 'Logged in successfully.';
  } catch (err) {
    error.value = (err as Error).message;
  }
}

async function loadProfile() {
  const profile = await getProfile();
  profileForm.fullName = profile.fullName || '';
  profileForm.title = profile.title || '';
  profileForm.bio = profile.bio || '';
  profileForm.programStatement = profile.programStatement || '';
  profileForm.heroImageUrl = profile.heroImageUrl || '';
  profileForm.email = profile.email || '';
}

async function loadAdminItems() {
  if (!token.value) return;
  itemForm.section = activeSection.value;
  adminItems.value = await getAdminItems(token.value, activeSection.value);
}

async function bootstrapAdmin() {
  if (!token.value) return;
  await Promise.all([loadProfile(), loadAdminItems()]);
}

async function saveProfile() {
  clearNotices();
  if (!token.value) return;

  try {
    await updateProfile(token.value, profileForm);
    message.value = 'Profile saved.';
  } catch (err) {
    error.value = (err as Error).message;
  }
}

function editItem(item: ContentItem) {
  editingId.value = item.id;
  itemForm.section = item.section;
  activeSection.value = item.section;
  itemForm.title = item.title;
  itemForm.subtitle = item.subtitle || '';
  itemForm.summary = item.summary || '';
  itemForm.body = item.body || '';
  itemForm.imageUrl = item.imageUrl || '';
  itemForm.externalUrl = item.externalUrl || '';
  itemForm.eventDate = item.eventDate || '';
  itemForm.tags = item.tags || '';
  itemForm.published = item.published;
}

async function saveItem() {
  clearNotices();
  if (!token.value) return;

  try {
    if (editingId.value) {
      await updateItem(token.value, editingId.value, itemForm);
      message.value = 'Entry updated.';
    } else {
      itemForm.section = activeSection.value;
      await createItem(token.value, itemForm);
      message.value = 'Entry created.';
    }

    resetItemForm();
    await loadAdminItems();
  } catch (err) {
    error.value = (err as Error).message;
  }
}

async function removeItem(itemId: number) {
  clearNotices();
  if (!token.value) return;

  try {
    await deleteItem(token.value, itemId);
    if (editingId.value === itemId) {
      resetItemForm();
    }
    await loadAdminItems();
    message.value = 'Entry deleted.';
  } catch (err) {
    error.value = (err as Error).message;
  }
}

onMounted(async () => {
  if (!token.value) return;
  try {
    await bootstrapAdmin();
  } catch (err) {
    error.value = (err as Error).message;
    logout();
  }
});
</script>
