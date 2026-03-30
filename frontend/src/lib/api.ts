import type { ContentItem, EditableItem, Profile, SectionKey } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

function headers(token?: string) {
  const result: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    result.Authorization = `Bearer ${token}`;
  }

  return result;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const message = payload.error || `Request failed (${response.status})`;
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export async function login(username: string, password: string): Promise<string> {
  const data = await request<{ accessToken: string }>('/auth/login', {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ username, password }),
  });

  return data.accessToken;
}

export function getProfile() {
  return request<Profile>('/profile');
}

export function updateProfile(token: string, payload: Profile) {
  return request<Profile>('/admin/profile', {
    method: 'PUT',
    headers: headers(token),
    body: JSON.stringify(payload),
  });
}

export function getPublicItems(section: SectionKey) {
  return request<ContentItem[]>(`/content/${section}`);
}

export function getAdminItems(token: string, section?: SectionKey) {
  const query = section ? `?section=${section}` : '';
  return request<ContentItem[]>(`/admin/content${query}`, {
    headers: headers(token),
  });
}

export function createItem(token: string, payload: EditableItem) {
  return request<ContentItem>('/admin/content', {
    method: 'POST',
    headers: headers(token),
    body: JSON.stringify(payload),
  });
}

export function updateItem(token: string, itemId: number, payload: EditableItem) {
  return request<ContentItem>(`/admin/content/${itemId}`, {
    method: 'PUT',
    headers: headers(token),
    body: JSON.stringify(payload),
  });
}

export function deleteItem(token: string, itemId: number) {
  return request<{ deleted: boolean }>(`/admin/content/${itemId}`, {
    method: 'DELETE',
    headers: headers(token),
  });
}
