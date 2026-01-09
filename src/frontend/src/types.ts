// API Types matching backend schemas

export interface User {
  id: number;
  username: string;
  email: string;
  identity: 'student' | 'professor';
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest {
  username: string;
  email: string;
  password: string;
  identity: 'student' | 'professor';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Course {
  id: number;
  course_code: string;
  course_name: string;
  description?: string;
  creator_id: number;
  created_at: string;
  is_enrolled?: boolean;
}

export interface CourseCreate {
  course_code: string;
  course_name: string;
  description?: string;
}

export interface Topic {
  id: number;
  title: string;
  description?: string;
  course_id: number;
  created_at: string;
}

export interface TopicCreate {
  title: string;
  description?: string;
  course_id: number;
}

export type NoteType = 'Summary' | 'Lecture' | 'Code' | 'Other';

export interface StudyNote {
  id: number;
  title: string;
  content: string; // Markdown
  summary?: string;
  note_type: NoteType;
  topic_id: number;
  author_id: number;
  likes: number;
  created_at: string;
}

export interface StudyNoteCreate {
  topic_id: number;
  title: string;
  content: string;
  summary?: string;
  note_type: NoteType;
}

export interface Comment {
  id: number;
  note_id: number;
  user_id: number;
  content: string;
  created_at: string;
}

export interface CommentCreate {
  note_id: number;
  content: string;
}
