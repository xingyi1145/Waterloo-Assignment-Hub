// API client for backend communication

import type {
  AuthResponse,
  LoginRequest,
  SignupRequest,
  User,
  Course,
  CourseCreate,
  Assignment,
  AssignmentCreate,
  Question,
  QuestionCreate,
  Solution,
  SolutionCreate,
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

  // Assignments
  async getAssignmentsByCourse(courseId: number): Promise<Assignment[]> {
    return this.request<Assignment[]>(`/assignments/course/${courseId}`);
  }

  async getAssignment(id: number): Promise<Assignment> {
    return this.request<Assignment>(`/assignments/${id}`);
  }

  async createAssignment(data: AssignmentCreate): Promise<Assignment> {
    return this.request<Assignment>('/assignments/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateAssignment(id: number, data: Partial<AssignmentCreate>): Promise<Assignment> {
    return this.request<Assignment>(`/assignments/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteAssignment(id: number): Promise<{ message: string }> {
    return this.request(`/assignments/${id}`, { method: 'DELETE' });
  }

  // Questions
  async getQuestionsByAssignment(assignmentId: number): Promise<Question[]> {
    return this.request<Question[]>(`/questions/assignment/${assignmentId}`);
  }

  async getQuestion(id: number): Promise<Question> {
    return this.request<Question>(`/questions/${id}`);
  }

  async createQuestion(data: QuestionCreate): Promise<Question> {
    return this.request<Question>('/questions/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateQuestion(id: number, data: Partial<QuestionCreate>): Promise<Question> {
    return this.request<Question>(`/questions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteQuestion(id: number): Promise<{ message: string }> {
    return this.request(`/questions/${id}`, { method: 'DELETE' });
  }

  // Solutions
  async getSolutionsByQuestion(questionId: number): Promise<Solution[]> {
    return this.request<Solution[]>(`/solutions/question/${questionId}`);
  }

  async getSolution(id: number): Promise<Solution> {
    return this.request<Solution>(`/solutions/${id}`);
  }

  async submitSolution(data: SolutionCreate): Promise<Solution> {
    return this.request<Solution>('/solutions/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async likeSolution(solutionId: number): Promise<{ message: string; likes: number }> {
    return this.request(`/solutions/${solutionId}/like`, { method: 'POST' });
  }

  async deleteSolution(id: number): Promise<{ message: string }> {
    return this.request(`/solutions/${id}`, { method: 'DELETE' });
  }

  async getComments(solutionId: number): Promise<Comment[]> {
    return this.request<Comment[]>(`/solutions/${solutionId}/comments`);
  }

  async addComment(solutionId: number, data: CommentCreate): Promise<Comment> {
    return this.request<Comment>(`/solutions/${solutionId}/comments`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient();
