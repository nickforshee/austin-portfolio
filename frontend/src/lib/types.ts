export type SectionKey = 'shows' | 'accomplishments' | 'work' | 'blog' | 'gallery';

export interface Profile {
  fullName: string;
  title: string;
  bio: string;
  programStatement: string;
  heroImageUrl: string | null;
  email: string | null;
}

export interface ContentItem {
  id: number;
  section: SectionKey;
  title: string;
  subtitle: string | null;
  summary: string | null;
  body: string | null;
  imageUrl: string | null;
  externalUrl: string | null;
  eventDate: string | null;
  tags: string | null;
  published: boolean;
  createdAt: string | null;
  updatedAt: string | null;
}

export interface EditableItem {
  id?: number;
  section: SectionKey;
  title: string;
  subtitle: string;
  summary: string;
  body: string;
  imageUrl: string;
  externalUrl: string;
  eventDate: string;
  tags: string;
  published: boolean;
}

export const sectionLabels: Record<SectionKey, string> = {
  shows: 'Past Shows',
  accomplishments: 'Accomplishments',
  work: 'Teaching Work',
  blog: 'Blog',
  gallery: 'Photo Gallery',
};
