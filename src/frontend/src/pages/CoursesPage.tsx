import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { Course } from '../types';

export const CoursesPage = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const { isProfessor } = useAuth();

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const data = await apiClient.getCourses();
      setCourses(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async (courseId: number) => {
    try {
      await apiClient.enrollInCourse(courseId);
      alert('Successfully enrolled in course!');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to enroll');
    }
  };

  if (loading) return <div className="loading">Loading courses...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="container">
      <div className="page-header">
        <h2>Courses</h2>
        {isProfessor && (
          <button
            className="btn btn-primary"
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            {showCreateForm ? 'Cancel' : 'Create Course'}
          </button>
        )}
      </div>

      {showCreateForm && <CreateCourseForm onSuccess={loadCourses} />}

      <div className="courses-grid">
        {courses.map((course) => (
          <div key={course.id} className="course-card">
            <h3>{course.course_code}</h3>
            <h4>{course.course_name}</h4>
            {course.description && <p>{course.description}</p>}
            <div className="card-actions">
              <Link to={`/courses/${course.id}`} className="btn btn-primary">
                View Course
              </Link>
              <button
                className="btn btn-secondary"
                onClick={() => handleEnroll(course.id)}
              >
                Enroll
              </button>
            </div>
          </div>
        ))}
      </div>

      {courses.length === 0 && (
        <div className="empty-state">
          <p>No courses available yet.</p>
          {isProfessor && <p>Create the first course to get started!</p>}
        </div>
      )}
    </div>
  );
};

const CreateCourseForm = ({ onSuccess }: { onSuccess: () => void }) => {
  const [courseCode, setCourseCode] = useState('');
  const [courseName, setCourseName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.createCourse({ course_code: courseCode, course_name: courseName, description });
      setCourseCode('');
      setCourseName('');
      setDescription('');
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create course');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form">
      <h3>Create New Course</h3>
      <div className="form-group">
        <label htmlFor="courseCode">Course Code</label>
        <input
          id="courseCode"
          type="text"
          value={courseCode}
          onChange={(e) => setCourseCode(e.target.value)}
          placeholder="e.g., CS137"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="courseName">Course Name</label>
        <input
          id="courseName"
          type="text"
          value={courseName}
          onChange={(e) => setCourseName(e.target.value)}
          placeholder="e.g., Programming Principles"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
        />
      </div>
      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? 'Creating...' : 'Create Course'}
      </button>
    </form>
  );
};
