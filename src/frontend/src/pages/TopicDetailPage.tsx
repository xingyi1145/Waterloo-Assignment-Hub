import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { Topic, StudyNote, ResourceType } from '../types';

export const TopicDetailPage = () => {
  const { topicId } = useParams<{ topicId: string }>();
  const [topic, setTopic] = useState<Topic | null>(null);
  const [notes, setNotes] = useState<StudyNote[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const { user } = useAuth(); // All users can create notes

  useEffect(() => {
    if (topicId) {
      loadTopicData(parseInt(topicId));
    }
  }, [topicId]);

  const loadTopicData = async (id: number) => {
    try {
      const [topicData, notesData] = await Promise.all([
        apiClient.getTopic(id),
        apiClient.getNotesByTopic(id),
      ]);
      setTopic(topicData);
      setNotes(notesData);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to load topic');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteNote = async (noteId: number, noteTitle: string) => {
    if (!confirm(`Are you sure you want to delete "${noteTitle}"?`)) {
      return;
    }
    try {
      await apiClient.deleteNote(noteId);
      alert('Note deleted successfully');
      if (topic) loadTopicData(topic.id);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete note');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!topic) return <div className="error-message">Topic not found</div>;

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h2>{topic.title}</h2>
          {topic.description && <p>{topic.description}</p>}
        </div>
        <button
          className="btn btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancel' : 'Create Note'}
        </button>
      </div>

      {showCreateForm && (
        <CreateNoteForm
          topicId={topic.id}
          onSuccess={() => {
            setShowCreateForm(false);
            loadTopicData(topic.id);
          }}
        />
      )}

      <h3>Study Notes</h3>
      <div className="notes-list">
        {notes.map((note) => (
          <div key={note.id} className="note-item-wrapper">
             {/* Styling wrapper similar to previous questions/solutions */}
             <div className="note-card" style={{padding: '1rem', border: '1px solid #eee', marginBottom: '1rem', borderRadius: '8px', background: 'white'}}>
               <Link to={`/notes/${note.id}`} style={{textDecoration: 'none', color: 'inherit', display: 'block'}}>
                <div className="note-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <h4 style={{margin: 0, color: '#3498db'}}>{note.title}</h4>
                  <span className="badge" style={{background: '#ecf0f1', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem'}}>{note.resource_type}</span>
                </div>
                {note.summary && <p style={{color: '#666', fontSize: '0.9rem', marginBottom: '0.5rem'}}>{note.summary}</p>}
                <div className="note-meta" style={{fontSize: '0.8rem', color: '#888', marginTop: '0.5rem'}}>
                    ❤️ {note.likes_count} • {new Date(note.created_at).toLocaleDateString()}
                </div>
               </Link>
                {(user?.id === note.author_id || user?.identity === 'professor') && (
                  <div className="note-actions" style={{marginTop: '0.5rem'}}>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={(e) => {
                        e.stopPropagation(); // Prevent Link click
                        handleDeleteNote(note.id, note.title)
                      }}
                    >
                      Delete
                    </button>
                  </div>
                )}
             </div>
          </div>
        ))}
      </div>

      {notes.length === 0 && (
        <div className="empty-state">
          <p>No notes yet.</p>
          <p>Be the first to share a resource!</p>
        </div>
      )}
    </div>
  );
};

const CreateNoteForm = ({
  topicId,
  onSuccess,
}: {
  topicId: number;
  onSuccess: () => void;
}) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [summary, setSummary] = useState('');
  const [resourceType, setResourceType] = useState<ResourceType>('Summary');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.createNote({
        topic_id: topicId,
        title,
        content,
        summary,
        resource_type: resourceType,
      });
      setTitle('');
      setContent('');
      setSummary('');
      onSuccess();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create note');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-form">
      <h3>Create New Note</h3>
      <div className="form-group">
        <label htmlFor="title">Title</label>
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
        <label htmlFor="resourceType">Type</label>
        <select
          id="resourceType"
          className="form-control"
          value={resourceType}
          onChange={(e) => setResourceType(e.target.value as ResourceType)}
        >
          <option value="CheatSheet">Cheat Sheet</option>
          <option value="Summary">Summary</option>
          <option value="Guide">Guide</option>
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="summary">Summary (Optional)</label>
        <input
          id="summary"
          className="form-control"
          type="text"
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
          placeholder="Brief description"
        />
      </div>
      <div className="form-group">
        <label htmlFor="content">Content (Markdown)</label>
        <textarea
          id="content"
          className="form-control"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={10}
          required
          placeholder="# Hello World&#10;&#10;Write your note here using Markdown..."
          style={{fontFamily: 'monospace'}}
        />
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Creating...' : 'Create Note'}
        </button>
      </div>
    </form>
  );
};
