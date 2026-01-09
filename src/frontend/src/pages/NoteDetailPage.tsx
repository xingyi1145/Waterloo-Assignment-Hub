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
  const [toc, setToc] = useState<{level: number, text: string}[]>([]);
  
  const { user } = useAuth();

  useEffect(() => {
    if (noteId) {
      loadNoteData(parseInt(noteId));
    }
  }, [noteId]);

  useEffect(() => {
    if (note) {
      // Simple regex-based ToC generator
      const headers = note.content.split('\n')
        .filter(line => line.match(/^#{1,3}\s/))
        .map(line => {
          const match = line.match(/^(#{1,3})\s+(.+)$/);
          if (match) {
            return { level: match[1].length, text: match[2] };
          }
          return null;
        })
        .filter((item): item is {level: number, text: string} => item !== null);
      setToc(headers);
    }
  }, [note]);

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
      setNote({ ...note, likes: result.likes });
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

  const getTypeColor = (type: string) => {
    switch (type) {
        case 'Summary': return '#3498db'; // Blue
        case 'Lecture': return '#e67e22'; // Orange
        case 'Code': return '#2ecc71'; // Green
        case 'Other': return '#95a5a6'; // Gray
        default: return '#3498db';
    }
  };

  return (
    <div className="container note-detail-page">
      <div className="note-header-section" style={{marginBottom: '2rem', borderBottom: '1px solid #eee', paddingBottom: '1rem'}}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
            <div>
                <span className="badge" style={{background: getTypeColor(note.note_type), color: 'white', padding: '0.25rem 0.75rem', borderRadius: '20px', fontSize: '0.8rem', marginBottom: '0.5rem', display: 'inline-block', fontWeight: 500}}>
                    {note.note_type}
                </span>
                <h1 style={{marginTop: '0.5rem', marginBottom: '0.5rem', color: '#2c3e50'}}>{note.title}</h1>
                <div className="meta" style={{color: '#7f8c8d', fontSize: '0.9rem'}}>
                    By User #{note.author_id} • Posted on {new Date(note.created_at).toLocaleDateString()}
                    {note.summary && <div style={{marginTop: '0.5rem', fontSize: '1.1rem', color: '#546e7a'}}>{note.summary}</div>}
                </div>
            </div>
            <div className="actions">
                <button 
                    onClick={handleLike}
                    className="btn btn-outline-primary"
                    style={{display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 1rem', borderRadius: '20px', border: '2px solid #3498db', color: '#3498db', background: 'transparent', cursor: 'pointer', fontSize: '1rem', fontWeight: 600}}
                >
                    ❤️ <span>{note.likes} Likes</span>
                </button>
            </div>
        </div>
      </div>

      <div className="note-body-layout" style={{display: 'flex', gap: '2rem', alignItems: 'flex-start'}}>
        {/* Main Content */}
        <div className="note-content-section" style={{flex: 3, background: 'white', padding: '2rem', borderRadius: '8px', border: '1px solid #e0e0e0', minHeight: '300px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)'}}>
            <div className="markdown-body" style={{lineHeight: '1.7', fontSize: '1rem', color: '#333'}}>
                <ReactMarkdown>{note.content}</ReactMarkdown>
            </div>
        </div>

        {/* Sidebar (Table of Contents) */}
        {toc.length > 0 && (
            <div className="note-sidebar" style={{flex: 1, position: 'sticky', top: '2rem', background: '#f8f9fa', padding: '1.5rem', borderRadius: '8px', border: '1px solid #eee'}}>
                <h4 style={{marginTop: 0, marginBottom: '1rem', color: '#2c3e50', borderBottom: '2px solid #3498db', paddingBottom: '0.5rem', display: 'inline-block'}}>Table of Contents</h4>
                <ul style={{listStyle: 'none', padding: 0, margin: 0}}>
                    {toc.map((item, index) => (
                        <li key={index} style={{marginBottom: '0.5rem', paddingLeft: `${(item.level - 1) * 1}rem`}}>
                            <a href="#" style={{textDecoration: 'none', color: '#555', fontSize: '0.9rem', display: 'block', padding: '2px 0'}} onClick={(e) => e.preventDefault()}>
                                {item.text}
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        )}
      </div>

      <div className="comments-section" style={{marginTop: '4rem', maxWidth: '800px'}}>
        <h3 style={{borderBottom: '1px solid #eee', paddingBottom: '0.5rem'}}>Comments</h3>
        
        <div className="comments-list" style={{marginBottom: '2rem'}}>
          {comments.map((comment) => (
            <div key={comment.id} className="comment" style={{background: '#f8f9fa', padding: '1rem', borderRadius: '8px', marginBottom: '1rem'}}>
              <div className="comment-meta" style={{fontSize: '0.8rem', color: '#888', marginBottom: '0.5rem', display: 'flex', justifyContent: 'space-between'}}>
                <strong>User #{comment.user_id}</strong>
                <span>{new Date(comment.created_at).toLocaleString()}</span>
              </div>
              <div className="comment-content" style={{color: '#444'}}>{comment.content}</div>
            </div>
          ))}
          {comments.length === 0 && <p style={{color: '#888', fontStyle: 'italic'}}>No comments yet. Be the first to share your thoughts!</p>}
        </div>

        {user && (
            <form onSubmit={handleAddComment} className="comment-form" style={{background: 'white', border: '1px solid #ddd', padding: '1.5rem', borderRadius: '8px'}}>
            <h5 style={{marginTop: 0}}>Add a Comment</h5>
            <div className="form-group">
                <textarea
                className="form-control"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Write your comment here..."
                rows={3}
                required
                style={{width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', marginBottom: '1rem'}}
                />
            </div>
            <button type="submit" className="btn btn-primary" style={{background: '#2c3e50', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer'}}>
                Post Comment
            </button>
            </form>
        )}
      </div>
    </div>
  );
};
