// API client for backend communication

import type {
  AuthResponse,
  LoginRequest,
  SignupRequest,
  User,
  Course,
  CourseCreate,
  Topic,
  TopicCreate,
  StudyNote,
  StudyNoteCreate,
  Comment,
  CommentCreate,
} from './types';

const API_BASE_URL = 'http://localhost:8000/api';

class ApiClient {
  private getAuthHeader(): HeadersInit {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...this.getAuthHeader(),
          ...options.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return response.json();
    } catch (error) {
      // Network errors, CORS errors, or backend down
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Cannot connect to server. Please ensure the backend is running on http://localhost:8000');
      }
      throw error;
    }
  }

  // Auth
  async signup(data: SignupRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/auth/me');
  }

  // Courses
  async getCourses(): Promise<Course[]> {
    return this.request<Course[]>('/courses/');
  }

  async getCourse(id: number): Promise<Course> {
    return this.request<Course>(`/courses/${id}`);
  }

  async createCourse(data: CourseCreate): Promise<Course> {
    return this.request<Course>('/courses/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async enrollInCourse(courseId: number): Promise<{ message: string }> {
    return this.request(`/courses/${courseId}/enroll`, { method: 'POST' });
  }

  async updateCourse(id: number, data: Partial<CourseCreate>): Promise<Course> {
    return this.request<Course>(`/courses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteCourse(id: number): Promise<{ message: string }> {
    return this.request(`/courses/${id}`, { method: 'DELETE' });
  }

  // Topics (formerly Assignments)
  async getTopicsByCourse(courseId: number): Promise<Topic[]> {
    return this.request<Topic[]>(`/topics/course/${courseId}`);
  }

  async getTopic(id: number): Promise<Topic> {
    return this.request<Topic>(`/topics/${id}`);
  }

  async createTopic(data: TopicCreate): Promise<Topic> {
    return this.request<Topic>('/topics/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateTopic(id: number, data: Partial<TopicCreate>): Promise<Topic> {
    return this.request<Topic>(`/topics/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteTopic(id: number): Promise<{ message: string }> {
    return this.request(`/topics/${id}`, { method: 'DELETE' });
  }

  // Study Notes (formerly Questions/Solutions)
  async getNotesByTopic(topicId: number): Promise<StudyNote[]> {
    return this.request<StudyNote[]>(`/notes/topic/${topicId}`);
  }

  async getNote(id: number): Promise<StudyNote> {
    return this.request<StudyNote>(`/notes/${id}`);
  }

  async createNote(data: StudyNoteCreate): Promise<StudyNote> {
    return this.request<StudyNote>('/notes/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  
  async likeNote(id: number): Promise<{ message: string; likes: number }> {
    return this.request<{ message: string; likes: number }>(`/notes/${id}/like`, { method: 'POST' });
  }
  
  async deleteNote(id: number): Promise<{ message: string }> {
    return this.request(`/notes/${id}`, { method: 'DELETE' });
  }

  // Comments
  async getComments(noteId: number): Promise<Comment[]> {
    return this.request<Comment[]>(`/notes/${noteId}/comments`);
  }

  async addComment(noteId: number, data: CommentCreate): Promise<Comment> {
    return this.request<Comment>(`/notes/${noteId}/comments`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient();
