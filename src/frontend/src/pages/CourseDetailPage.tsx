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
  const [editingAssignment, setEditingAssignment] = useState<Assignment | null>(null);
  const [error, setError] = useState('');
  const { isProfessor } = useAuth();

  useEffect(() => {
    if (courseId) {
      loadCourseData(parseInt(courseId));
    }
  }, [courseId]);

  const loadCourseData = async (id: number) => {
    try {
      const courseData = await apiClient.getCourse(id);
      setCourse(courseData);
      
      // Only load assignments if enrolled or professor
      if (courseData.is_enrolled) {
        try {
          const assignmentsData = await apiClient.getAssignmentsByCourse(id);
          setAssignments(assignmentsData);
        } catch (err) {
          // If not enrolled, this will error - that's expected
          console.log('Could not load assignments:', err);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load course');
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async () => {
    if (!course) return;
    try {
      await apiClient.enrollInCourse(course.id);
      alert('Successfully enrolled in course!');
      // Reload course data
      loadCourseData(course.id);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to enroll');
    }
  };

  const handleDeleteAssignment = async (assignmentId: number, assignmentName: string) => {
    if (!confirm(`Are you sure you want to delete "${assignmentName}"? This will also delete all questions and solutions.`)) {
      return;
    }
    try {
      await apiClient.deleteAssignment(assignmentId);
      alert('Assignment deleted successfully');
      if (course) loadCourseData(course.id);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete assignment');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!course) return <div className="error-message">Course not found</div>;

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h2>{course.course_code}: {course.course_name}</h2>
          {course.description && <p className="course-description">{course.description}</p>}
          {course.is_enrolled && !isProfessor && (
            <span className="enrollment-badge">✓ Enrolled</span>
          )}
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

      {/* Show enroll button for students not enrolled */}
      {!isProfessor && !course.is_enrolled && (
        <div className="enrollment-prompt">
          <p>You need to enroll in this course to view assignments and submit solutions.</p>
          <button className="btn btn-primary" onClick={handleEnroll}>
            Enroll in Course
          </button>
        </div>
      )}

      {showCreateForm && (
        <CreateAssignmentForm
          courseId={course.id}
          onSuccess={() => {
            setShowCreateForm(false);
            loadCourseData(course.id);
          }}
        />
      )}

      {editingAssignment && (
        <EditAssignmentForm
          assignment={editingAssignment}
          onSuccess={() => {
            setEditingAssignment(null);
            loadCourseData(course.id);
          }}
          onCancel={() => setEditingAssignment(null)}
        />
      )}

      {/* Only show assignments if enrolled or professor */}
      {course.is_enrolled && (
        <>
          <h3>Assignments</h3>
          <div className="assignments-list">
            {assignments.map((assignment) => (
              <div key={assignment.id} className="assignment-item-wrapper">
                <Link
                  to={`/assignments/${assignment.id}`}
                  className="assignment-item"
                >
                  <h4>{assignment.assignment_name}</h4>
                  {assignment.description && <p>{assignment.description}</p>}
                  <span className="assignment-date">
                    Created: {new Date(assignment.created_at).toLocaleDateString()}
                  </span>
                </Link>
                {isProfessor && (
                  <div className="assignment-actions">
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={(e) => {
                        e.preventDefault();
                        setEditingAssignment(assignment);
                      }}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={(e) => {
                        e.preventDefault();
                        handleDeleteAssignment(assignment.id, assignment.assignment_name);
                      }}
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>

          {assignments.length === 0 && (
            <div className="empty-state">
              <p>No assignments yet.</p>
              {isProfessor && <p>Create the first assignment!</p>}
            </div>
          )}
        </>
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

const EditAssignmentForm = ({
  assignment,
  onSuccess,
  onCancel,
}: {
  assignment: Assignment;
  onSuccess: () => void;
  onCancel: () => void;
}) => {
  const [name, setName] = useState(assignment.assignment_name);
  const [description, setDescription] = useState(assignment.description || '');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.updateAssignment(assignment.id, {
        assignment_name: name,
        description,
        course_id: assignment.course_id,
      });
      alert('Assignment updated successfully');
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update assignment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form">
      <h3>Edit Assignment</h3>
      <div className="form-group">
        <label htmlFor="editName">Assignment Name</label>
        <input
          id="editName"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
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
