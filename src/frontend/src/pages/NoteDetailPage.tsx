import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { StudyNote, Comment } from '../types';

export const NoteDetailPage = () => {
  const { noteId } = useParams<{ noteId: string }>();
  const [note, setNote] = useState<StudyNote | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    if (noteId) {
      loadNoteData(parseInt(noteId));
    }
  }, [noteId]);

  const loadNoteData = async (id: number) => {
    try {
      const [noteData, commentsData] = await Promise.all([
        apiClient.getNote(id),
        apiClient.getComments(id),
      ]);
      setNote(noteData);
      setComments(commentsData);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to load note');
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async () => {
    if (!note) return;
    try {
      const result = await apiClient.likeNote(note.id);
      setNote({ ...note, likes_count: result.likes });
    } catch (err) {
      if (err instanceof Error && err.message.includes("already liked")) {
          alert("You have already liked this note");
      } else {
          alert(err instanceof Error ? err.message : 'Failed to like note');
      }
    }
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!note || !newComment.trim()) return;

    try {
      const comment = await apiClient.addComment(note.id, {
        note_id: note.id,
        content: newComment,
      });
      setComments([...comments, comment]);
      setNewComment('');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to add comment');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!note) return <div className="error-message">Note not found</div>;

  return (
    <div className="container note-detail-page">
      <div className="note-header-section" style={{marginBottom: '2rem', borderBottom: '1px solid #eee', paddingBottom: '1rem'}}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
            <div>
                <span className={`badge badge-${note.resource_type.toLowerCase()}`} style={{background: '#3498db', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem', marginBottom: '0.5rem', display: 'inline-block'}}>
                    {note.resource_type}
                </span>
                <h1 style={{marginTop: '0.5rem', marginBottom: '0.5rem'}}>{note.title}</h1>
                <div className="meta" style={{color: '#666', fontSize: '0.9rem'}}>
                    Posted on {new Date(note.created_at).toLocaleDateString()}
                    {note.summary && <div style={{marginTop: '0.5rem', fontStyle: 'italic'}}>{note.summary}</div>}
                </div>
            </div>
            <div className="actions">
                <button 
                    onClick={handleLike}
                    className="btn btn-outline-primary"
                    style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}
                >
                    ❤️ <span>{note.likes_count} Likes</span>
                </button>
            </div>
        </div>
      </div>

      <div className="note-content-section" style={{background: '#f8f9fa', padding: '2rem', borderRadius: '8px', minHeight: '300px'}}>
        <div className="markdown-body" style={{lineHeight: '1.6'}}>
            <ReactMarkdown>{note.content}</ReactMarkdown>
        </div>
      </div>

      <div className="comments-section" style={{marginTop: '3rem'}}>
        <h3>Comments</h3>
        
        <div className="comments-list" style={{marginBottom: '2rem'}}>
          {comments.map((comment) => (
            <div key={comment.id} className="comment" style={{background: 'white', border: '1px solid #eee', padding: '1rem', borderRadius: '8px', marginBottom: '1rem'}}>
              <div className="comment-meta" style={{fontSize: '0.8rem', color: '#888', marginBottom: '0.5rem'}}>
                User #{comment.user_id} • {new Date(comment.created_at).toLocaleString()}
              </div>
              <div className="comment-content">{comment.content}</div>
            </div>
          ))}
          {comments.length === 0 && <p style={{color: '#888'}}>No comments yet.</p>}
        </div>

        <form onSubmit={handleAddComment} className="comment-form">
          <div className="form-group">
            <textarea
              className="form-control"
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Add a comment..."
              rows={3}
              required
            />
          </div>
          <button type="submit" className="btn btn-secondary" style={{marginTop: '0.5rem'}}>
            Post Comment
          </button>
        </form>
      </div>
    </div>
  );
};
