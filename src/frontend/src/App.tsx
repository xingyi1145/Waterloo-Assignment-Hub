import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import { ProtectedRoute } from './ProtectedRoute';
import { Navbar } from './components/Navbar';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { CoursesPage } from './pages/CoursesPage';
import { CourseDetailPage } from './pages/CourseDetailPage';
import { AssignmentDetailPage } from './pages/AssignmentDetailPage';
import { QuestionDetailPage } from './pages/QuestionDetailPage';
import { SolutionDetailPage } from './pages/SolutionDetailPage';
import './App.css';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="app">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Navigate to="/courses" replace />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route
                path="/courses"
                element={
                  <ProtectedRoute>
                    <CoursesPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/courses/:courseId"
                element={
                  <ProtectedRoute>
                    <CourseDetailPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/assignments/:assignmentId"
                element={
                  <ProtectedRoute>
                    <AssignmentDetailPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/questions/:questionId"
                element={
                  <ProtectedRoute>
                    <QuestionDetailPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/solutions/:solutionId"
                element={
                  <ProtectedRoute>
                    <SolutionDetailPage />
                  </ProtectedRoute>
                }
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
