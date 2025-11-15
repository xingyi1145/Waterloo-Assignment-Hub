import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { Assignment, Question } from '../types';

export const AssignmentDetailPage = () => {
  const { assignmentId } = useParams<{ assignmentId: string }>();
  const [assignment, setAssignment] = useState<Assignment | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const { isProfessor } = useAuth();

  useEffect(() => {
    if (assignmentId) {
      loadAssignmentData(parseInt(assignmentId));
    }
  }, [assignmentId]);

  const loadAssignmentData = async (id: number) => {
    try {
      const [assignmentData, questionsData] = await Promise.all([
        apiClient.getAssignment(id),
        apiClient.getQuestionsByAssignment(id),
      ]);
      setAssignment(assignmentData);
      setQuestions(questionsData);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to load assignment');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!assignment) return <div className="error-message">Assignment not found</div>;

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h2>{assignment.assignment_name}</h2>
          {assignment.description && <p>{assignment.description}</p>}
        </div>
        {isProfessor && (
          <button
            className="btn btn-primary"
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            {showCreateForm ? 'Cancel' : 'Create Question'}
          </button>
        )}
      </div>

      {showCreateForm && (
        <CreateQuestionForm
          assignmentId={assignment.id}
          onSuccess={() => {
            setShowCreateForm(false);
            loadAssignmentData(assignment.id);
          }}
        />
      )}

      <h3>Questions</h3>
      <div className="questions-list">
        {questions.map((question) => (
          <Link
            key={question.id}
            to={`/questions/${question.id}`}
            className="question-item"
          >
            <div className="question-header">
              <h4>{question.title}</h4>
              {question.difficulty && (
                <span className={`badge badge-${question.difficulty}`}>
                  {question.difficulty}
                </span>
              )}
            </div>
            <p className="question-preview">{question.description.substring(0, 150)}...</p>
          </Link>
        ))}
      </div>

      {questions.length === 0 && (
        <div className="empty-state">
          <p>No questions yet.</p>
          {isProfessor && <p>Create the first question!</p>}
        </div>
      )}
    </div>
  );
};

const CreateQuestionForm = ({
  assignmentId,
  onSuccess,
}: {
  assignmentId: number;
  onSuccess: () => void;
}) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.createQuestion({
        title,
        description,
        difficulty,
        assignment_id: assignmentId,
      });
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create question');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form">
      <h3>Create New Question</h3>
      <div className="form-group">
        <label htmlFor="title">Question Title</label>
        <input
          id="title"
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
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={6}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="difficulty">Difficulty</label>
        <select
          id="difficulty"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value as 'easy' | 'medium' | 'hard')}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? 'Creating...' : 'Create Question'}
      </button>
    </form>
  );
};
