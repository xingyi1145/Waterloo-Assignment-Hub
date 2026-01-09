import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import { ProtectedRoute } from './ProtectedRoute';
import { Navbar } from './components/Navbar';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { CoursesPage } from './pages/CoursesPage';
import { CourseDetailPage } from './pages/CourseDetailPage';
import { TopicDetailPage } from './pages/TopicDetailPage';
import { NoteDetailPage } from './pages/NoteDetailPage';
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
                path="/topics/:topicId"
                element={
                  <ProtectedRoute>
                    <TopicDetailPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/notes/:noteId"
                element={
                  <ProtectedRoute>
                    <NoteDetailPage />
                  </ProtectedRoute>
                }
              />
              <Route path="*" element={<Navigate to="/courses" replace />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
