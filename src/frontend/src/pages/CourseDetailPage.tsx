import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { Course, Assignment } from '../types';

export const CourseDetailPage = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const [course, setCourse] = useState<Course | null>(null);
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const { isProfessor } = useAuth();

  useEffect(() => {
    if (courseId) {
      loadCourseData(parseInt(courseId));
    }
  }, [courseId]);

  const loadCourseData = async (id: number) => {
    try {
      const [courseData, assignmentsData] = await Promise.all([
        apiClient.getCourse(id),
        apiClient.getAssignmentsByCourse(id),
      ]);
      setCourse(courseData);
      setAssignments(assignmentsData);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to load course');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!course) return <div className="error-message">Course not found</div>;

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h2>{course.course_code}: {course.course_name}</h2>
          {course.description && <p className="course-description">{course.description}</p>}
        </div>
        {isProfessor && (
          <button
            className="btn btn-primary"
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            {showCreateForm ? 'Cancel' : 'Create Assignment'}
          </button>
        )}
      </div>

      {showCreateForm && (
        <CreateAssignmentForm
          courseId={course.id}
          onSuccess={() => {
            setShowCreateForm(false);
            loadCourseData(course.id);
          }}
        />
      )}

      <h3>Assignments</h3>
      <div className="assignments-list">
        {assignments.map((assignment) => (
          <Link
            key={assignment.id}
            to={`/assignments/${assignment.id}`}
            className="assignment-item"
          >
            <h4>{assignment.assignment_name}</h4>
            {assignment.description && <p>{assignment.description}</p>}
            <span className="assignment-date">
              Created: {new Date(assignment.created_at).toLocaleDateString()}
            </span>
          </Link>
        ))}
      </div>

      {assignments.length === 0 && (
        <div className="empty-state">
          <p>No assignments yet.</p>
          {isProfessor && <p>Create the first assignment!</p>}
        </div>
      )}
    </div>
  );
};

const CreateAssignmentForm = ({
  courseId,
  onSuccess,
}: {
  courseId: number;
  onSuccess: () => void;
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.createAssignment({
        assignment_name: name,
        description,
        course_id: courseId,
      });
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create assignment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form">
      <h3>Create New Assignment</h3>
      <div className="form-group">
        <label htmlFor="name">Assignment Name</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
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
        {loading ? 'Creating...' : 'Create Assignment'}
      </button>
    </form>
  );
};
