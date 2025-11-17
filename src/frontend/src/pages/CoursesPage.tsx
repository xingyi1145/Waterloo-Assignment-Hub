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
  const [editingCourse, setEditingCourse] = useState<Course | null>(null);
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
      // Reload courses to update enrollment status
      loadCourses();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to enroll');
    }
  };

  const handleDelete = async (courseId: number, courseName: string) => {
    if (!confirm(`Are you sure you want to delete "${courseName}"? This will also delete all assignments, questions, and solutions.`)) {
      return;
    }
    try {
      await apiClient.deleteCourse(courseId);
      alert('Course deleted successfully');
      loadCourses();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete course');
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

      {editingCourse && (
        <EditCourseForm
          course={editingCourse}
          onSuccess={() => {
            setEditingCourse(null);
            loadCourses();
          }}
          onCancel={() => setEditingCourse(null)}
        />
      )}

      <div className="courses-grid">
        {courses.map((course) => (
          <div key={course.id} className="course-card">
            <h3>{course.course_code}</h3>
            <h4>{course.course_name}</h4>
            {course.description && <p>{course.description}</p>}
            {course.is_enrolled && (
              <span className="enrollment-badge">✓ Enrolled</span>
            )}
            <div className="card-actions">
              <Link to={`/courses/${course.id}`} className="btn btn-primary">
                View Course
              </Link>
              {!isProfessor && !course.is_enrolled && (
                <button
                  className="btn btn-secondary"
                  onClick={() => handleEnroll(course.id)}
                >
                  Enroll
                </button>
              )}
              {isProfessor && (
                <>
                  <button
                    className="btn btn-secondary"
                    onClick={() => setEditingCourse(course)}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(course.id, course.course_name)}
                  >
                    Delete
                  </button>
                </>
              )}
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

const EditCourseForm = ({
  course,
  onSuccess,
  onCancel,
}: {
  course: Course;
  onSuccess: () => void;
  onCancel: () => void;
}) => {
  const [courseCode, setCourseCode] = useState(course.course_code);
  const [courseName, setCourseName] = useState(course.course_name);
  const [description, setDescription] = useState(course.description || '');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.updateCourse(course.id, {
        course_code: courseCode,
        course_name: courseName,
        description,
      });
      alert('Course updated successfully');
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update course');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form">
      <h3>Edit Course</h3>
      <div className="form-group">
        <label htmlFor="editCourseCode">Course Code</label>
        <input
          id="editCourseCode"
          type="text"
          value={courseCode}
          onChange={(e) => setCourseCode(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="editCourseName">Course Name</label>
        <input
          id="editCourseName"
          type="text"
          value={courseName}
          onChange={(e) => setCourseName(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="editDescription">Description</label>
        <textarea
          id="editDescription"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
        />
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save Changes'}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
};
