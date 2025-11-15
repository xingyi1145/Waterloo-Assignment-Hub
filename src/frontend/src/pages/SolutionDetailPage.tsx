import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { apiClient } from '../api';
import type { Solution, Comment } from '../types';

export const SolutionDetailPage = () => {
  const { solutionId } = useParams<{ solutionId: string }>();
  const [solution, setSolution] = useState<Solution | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (solutionId) {
      loadSolutionData(parseInt(solutionId));
    }
  }, [solutionId]);

  const loadSolutionData = async (id: number) => {
    try {
      const [solutionData, commentsData] = await Promise.all([
        apiClient.getSolution(id),
        apiClient.getComments(id),
      ]);
      setSolution(solutionData);
      setComments(commentsData);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to load solution');
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async () => {
    if (!solution) return;
    try {
      const result = await apiClient.likeSolution(solution.id);
      setSolution({ ...solution, likes: result.likes });
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to like solution');
    }
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!solution || !newComment.trim()) return;

    try {
      await apiClient.addComment(solution.id, {
        solution_id: solution.id,
        content: newComment,
      });
      setNewComment('');
      loadSolutionData(solution.id);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to add comment');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!solution) return <div className="error-message">Solution not found</div>;

  return (
    <div className="container">
      <div className="solution-detail">
        <div className="solution-header">
          <h2>Solution</h2>
          <div className="solution-meta">
            <span className="solution-language">{solution.language}</span>
            <span className={`solution-status status-${solution.status}`}>
              {solution.status}
            </span>
            <button onClick={handleLike} className="btn-like">
              ❤️ {solution.likes}
            </button>
          </div>
        </div>

        <div className="solution-code">
          <pre>
            <code>{solution.code}</code>
          </pre>
        </div>

        <div className="solution-info">
          <span>Submitted: {new Date(solution.created_at).toLocaleString()}</span>
        </div>

        <div className="comments-section">
          <h3>Comments ({comments.length})</h3>
          
          <form onSubmit={handleAddComment} className="comment-form">
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Add a comment..."
              rows={3}
            />
            <button type="submit" className="btn btn-primary">
              Post Comment
            </button>
          </form>

          <div className="comments-list">
            {comments.map((comment) => (
              <div key={comment.id} className="comment-item">
                <div className="comment-header">
                  <span className="comment-author">User #{comment.user_id}</span>
                  <span className="comment-date">
                    {new Date(comment.created_at).toLocaleString()}
                  </span>
                </div>
                <p className="comment-content">{comment.content}</p>
              </div>
            ))}
          </div>

          {comments.length === 0 && (
            <div className="empty-state">
              <p>No comments yet. Be the first to comment!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
