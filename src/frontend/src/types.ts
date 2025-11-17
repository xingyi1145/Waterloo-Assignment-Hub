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

export interface Assignment {
  id: number;
  assignment_name: string;
  description?: string;
  course_id: number;
  created_at: string;
}

export interface AssignmentCreate {
  assignment_name: string;
  description?: string;
  course_id: number;
}

export interface Question {
  id: number;
  title: string;
  description: string;
  difficulty?: 'easy' | 'medium' | 'hard';
  assignment_id: number;
  created_at: string;
}

export interface QuestionCreate {
  title: string;
  description: string;
  difficulty?: 'easy' | 'medium' | 'hard';
  assignment_id: number;
}

export interface Solution {
  id: number;
  question_id: number;
  submitter_id: number;
  code: string;
  language: string;
  status: string;
  likes: number;
  created_at: string;
}

export interface SolutionCreate {
  question_id: number;
  code: string;
  language: string;
}

export interface Comment {
  id: number;
  solution_id: number;
  user_id: number;
  content: string;
  created_at: string;
}

export interface CommentCreate {
  solution_id: number;
  content: string;
}
