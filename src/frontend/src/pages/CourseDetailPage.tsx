import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { Course, Topic } from '../types';

export const CourseDetailPage = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const [course, setCourse] = useState<Course | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTopic, setEditingTopic] = useState<Topic | null>(null);
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
      
      // Only load topics if enrolled or professor
      if (courseData.is_enrolled) {
        try {
          const topicsData = await apiClient.getTopicsByCourse(id);
          setTopics(topicsData);
        } catch (err) {
          console.log('Could not load topics:', err);
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
      loadCourseData(course.id);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to enroll');
    }
  };

  const handleDeleteTopic = async (topicId: number, topicTitle: string) => {
    if (!confirm(`Are you sure you want to delete "${topicTitle}"? This will also delete all notes within it.`)) {
      return;
    }
    try {
      await apiClient.deleteTopic(topicId);
      alert('Topic deleted successfully');
      if (course) loadCourseData(course.id);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete topic');
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
            {showCreateForm ? 'Cancel' : 'Create Topic'}
          </button>
        )}
      </div>

      {!isProfessor && !course.is_enrolled && (
        <div className="enrollment-prompt">
          <p>You need to enroll in this course to view topics and study notes.</p>
          <button className="btn btn-primary" onClick={handleEnroll}>
            Enroll in Course
          </button>
        </div>
      )}

      {showCreateForm && (
        <CreateTopicForm
          courseId={course.id}
          onSuccess={() => {
            setShowCreateForm(false);
            loadCourseData(course.id);
          }}
        />
      )}

      {editingTopic && (
        <EditTopicForm
          topic={editingTopic}
          onSuccess={() => {
            setEditingTopic(null);
            loadCourseData(course.id);
          }}
          onCancel={() => setEditingTopic(null)}
        />
      )}

      {course.is_enrolled && (
        <>
          <h3>Topics</h3>
          <div className="topics-list">
            {topics.map((topic) => (
              <div key={topic.id} className="topic-item-wrapper" style={{marginBottom: '10px', background: '#f9f9f9', padding: '10px', borderRadius: '5px'}}>
                <Link
                  to={`/topics/${topic.id}`}
                  className="topic-item"
                  style={{display: 'block', textDecoration: 'none', color: '#333'}}
                >
                  <h4 style={{margin: '0 0 5px'}}>{topic.title}</h4>
                  {topic.description && <p style={{margin: '0', fontSize: '0.9em', color: '#666'}}>{topic.description}</p>}
                </Link>
                {isProfessor && (
                  <div className="topic-actions" style={{marginTop: '10px'}}>
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={(e) => {
                        e.preventDefault();
                        setEditingTopic(topic);
                      }}
                      style={{marginRight: '5px'}}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={(e) => {
                        e.preventDefault();
                        handleDeleteTopic(topic.id, topic.title);
                      }}
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>

          {topics.length === 0 && (
            <div className="empty-state">
              <p>No topics yet.</p>
              {isProfessor && <p>Create the first topic!</p>}
            </div>
          )}
        </>
      )}
    </div>
  );
};

const CreateTopicForm = ({
  courseId,
  onSuccess,
}: {
  courseId: number;
  onSuccess: () => void;
}) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.createTopic({
        title,
        description,
        course_id: courseId,
      });
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create topic');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form">
      <h3>Create New Topic</h3>
      <div className="form-group">
        <label htmlFor="title">Topic Title</label>
        <input
          id="title"
          className="form-control"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          className="form-control"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
        />
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Creating...' : 'Create Topic'}
        </button>
      </div>
    </form>
  );
};

const EditTopicForm = ({
  topic,
  onSuccess,
  onCancel,
}: {
  topic: Topic;
  onSuccess: () => void;
  onCancel: () => void;
}) => {
  const [title, setTitle] = useState(topic.title);
  const [description, setDescription] = useState(topic.description || '');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.updateTopic(topic.id, {
        title,
        description,
        course_id: topic.course_id,
      });
      alert('Topic updated successfully');
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update topic');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form" style={{background: '#f0f0f0', padding: '15px', borderRadius: '5px', marginBottom: '20px'}}>
      <h3>Edit Topic</h3>
      <div className="form-group">
        <label htmlFor="editTitle">Topic Title</label>
        <input
          id="editTitle"
          className="form-control"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="editDescription">Description</label>
        <textarea
          id="editDescription"
          className="form-control"
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
