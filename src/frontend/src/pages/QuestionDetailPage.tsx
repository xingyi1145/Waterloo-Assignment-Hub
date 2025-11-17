import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { Question, Solution, User } from '../types';

export const QuestionDetailPage = () => {
  const { questionId } = useParams<{ questionId: string }>();
  const [question, setQuestion] = useState<Question | null>(null);
  const [solutions, setSolutions] = useState<Solution[]>([]);
  const [showSubmitForm, setShowSubmitForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const { user, isProfessor } = useAuth();

  useEffect(() => {
    if (questionId) {
      loadQuestionData(parseInt(questionId));
    }
  }, [questionId]);

  const loadQuestionData = async (id: number) => {
    try {
      const [questionData, solutionsData] = await Promise.all([
        apiClient.getQuestion(id),
        apiClient.getSolutionsByQuestion(id),
      ]);
      setQuestion(questionData);
      setSolutions(solutionsData);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to load question');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSolution = async (solutionId: number) => {
    if (!confirm('Are you sure you want to delete this solution? This will also delete all comments.')) {
      return;
    }
    try {
      await apiClient.deleteSolution(solutionId);
      alert('Solution deleted successfully');
      if (question) loadQuestionData(question.id);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete solution');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!question) return <div className="error-message">Question not found</div>;

  return (
    <div className="container">
      <div className="question-detail">
        <div className="question-header">
          <h2>{question.title}</h2>
          {question.difficulty && (
            <span className={`badge badge-${question.difficulty}`}>
              {question.difficulty}
            </span>
          )}
        </div>
        <div className="question-description">
          <pre>{question.description}</pre>
        </div>

        <div className="action-buttons">
          <button
            className="btn btn-primary"
            onClick={() => setShowSubmitForm(!showSubmitForm)}
          >
            {showSubmitForm ? 'Cancel' : 'Submit Solution'}
          </button>
        </div>

        {showSubmitForm && (
          <SubmitSolutionForm
            questionId={question.id}
            onSuccess={() => {
              setShowSubmitForm(false);
              loadQuestionData(question.id);
            }}
          />
        )}

        <h3>Solutions ({solutions.length})</h3>
        <div className="solutions-list">
          {solutions.map((solution) => (
            <div key={solution.id} className="solution-item-wrapper">
              <Link
                to={`/solutions/${solution.id}`}
                className="solution-item"
              >
                <div className="solution-header">
                  <span className="solution-language">{solution.language}</span>
                  <span className={`solution-status status-${solution.status}`}>
                    {solution.status}
                  </span>
                  <span className="solution-likes">❤️ {solution.likes}</span>
                </div>
                <code className="solution-preview">
                  {solution.code.substring(0, 100)}...
                </code>
                <span className="solution-date">
                  {new Date(solution.created_at).toLocaleString()}
                </span>
              </Link>
              {(isProfessor || (user && solution.submitter_id === user.id)) && (
                <div className="solution-actions">
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={(e) => {
                      e.preventDefault();
                      handleDeleteSolution(solution.id);
                    }}
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

        {solutions.length === 0 && (
          <div className="empty-state">
            <p>No solutions submitted yet. Be the first!</p>
          </div>
        )}
      </div>
    </div>
  );
};

const SubmitSolutionForm = ({
  questionId,
  onSuccess,
}: {
  questionId: number;
  onSuccess: () => void;
}) => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.submitSolution({
        question_id: questionId,
        code,
        language,
      });
      setCode('');
      onSuccess();
      alert('Solution submitted successfully!');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to submit solution');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="submit-solution-form">
      <h3>Submit Your Solution</h3>
      <div className="form-group">
        <label htmlFor="language">Language</label>
        <select
          id="language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
          <option value="javascript">JavaScript</option>
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="code">Code</label>
        <textarea
          id="code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          rows={15}
          className="code-editor"
          placeholder="// Enter your code here..."
          required
        />
      </div>
      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? 'Submitting...' : 'Submit Solution'}
      </button>
    </form>
  );
};
