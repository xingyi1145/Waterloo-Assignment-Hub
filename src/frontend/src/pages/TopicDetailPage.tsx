import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMde from 'react-mde';
import * as Showdown from 'showdown';
import 'react-mde/lib/styles/css/react-mde-all.css';
import { apiClient } from '../api';
import { useAuth } from '../AuthContext';
import type { Topic, StudyNote, NoteType } from '../types';

const converter = new Showdown.Converter({
  tables: true,
  simplifiedAutoLink: true,
  strikethrough: true,
  tasklists: true
});

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
      <div className="notes-list" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
        {notes.map((note) => (
          <div key={note.id} className="note-card" style={{
            padding: '1.5rem', 
            border: '1px solid #e0e0e0', 
            borderRadius: '12px', 
            background: 'white',
            boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
            position: 'relative',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
             <Link to={`/notes/${note.id}`} style={{textDecoration: 'none', color: 'inherit', display: 'block', flexGrow: 1}}>
              <div className="note-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem'}}>
                <h4 style={{margin: 0, color: '#2c3e50', fontSize: '1.2rem', fontWeight: 600}}>{note.title}</h4>
                <span className={`badge badge-${note.note_type.toLowerCase()}`} style={{
                    background: '#e3f2fd', 
                    color: '#1565c0', 
                    padding: '0.25rem 0.75rem', 
                    borderRadius: '20px', 
                    fontSize: '0.75rem',
                    fontWeight: 500,
                    whiteSpace: 'nowrap',
                    marginLeft: '0.5rem'
                }}>
                    {note.note_type}
                </span>
              </div>
              
              {note.summary && (
                  <p style={{
                      color: '#546e7a', 
                      fontSize: '0.95rem', 
                      marginBottom: '1rem', 
                      lineHeight: '1.5',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: 'vertical'
                  }}>
                      {note.summary}
                  </p>
              )}
              
              <div className="note-meta" style={{
                  display: 'flex', 
                  alignItems: 'center', 
                  fontSize: '0.85rem', 
                  color: '#90a4ae',
                  marginTop: 'auto'
              }}>
                  <span style={{display: 'flex', alignItems: 'center', marginRight: '1rem'}}>
                      ❤️ {note.likes}
                  </span>
                  <span>{new Date(note.created_at).toLocaleDateString()}</span>
              </div>
             </Link>
             
              {(user?.id === note.author_id || user?.identity === 'professor') && (
                <div className="note-actions" style={{position: 'absolute', bottom: '1.5rem', right: '1.5rem'}}>
                  <button
                    className="btn btn-sm btn-icon"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteNote(note.id, note.title)
                    }}
                    style={{color: '#ef5350', background: 'none', border: 'none', cursor: 'pointer', padding: '0.25rem'}}
                    title="Delete Note"
                  >
                    🗑️
                  </button>
                </div>
              )}
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
  const [noteType, setNoteType] = useState<NoteType>('Summary');
  const [selectedTab, setSelectedTab] = useState<"write" | "preview">("write");
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
        note_type: noteType,
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
    <form onSubmit={handleSubmit} className="create-form" style={{background: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #ddd', marginBottom: '20px'}}>
      <h3 style={{marginTop: 0}}>Create New Note</h3>
      <div className="form-group" style={{marginBottom: '15px'}}>
        <label htmlFor="title" style={{display: 'block', marginBottom: '5px', fontWeight: 500}}>Title</label>
        <input
          id="title"
          className="form-control"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd'}}
        />
      </div>
      <div className="form-group" style={{marginBottom: '15px'}}>
        <label htmlFor="noteType" style={{display: 'block', marginBottom: '5px', fontWeight: 500}}>Type</label>
        <select
          id="noteType"
          className="form-control"
          value={noteType}
          onChange={(e) => setNoteType(e.target.value as NoteType)}
          style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd'}}
        >
          <option value="Summary">Summary</option>
          <option value="Lecture">Lecture</option>
          <option value="Code">Code</option>
          <option value="Other">Other</option>
        </select>
      </div>
      <div className="form-group" style={{marginBottom: '15px'}}>
        <label htmlFor="summary" style={{display: 'block', marginBottom: '5px', fontWeight: 500}}>Summary (Optional)</label>
        <input
          id="summary"
          className="form-control"
          type="text"
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
          placeholder="Brief description for the card view"
          style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd'}}
        />
      </div>
      <div className="form-group" style={{marginBottom: '15px'}}>
        <label style={{display: 'block', marginBottom: '5px', fontWeight: 500}}>Content (Markdown)</label>
        <div className="markdown-editor-wrapper" style={{border: '1px solid #ddd', borderRadius: '4px'}}>
          <ReactMde
            value={content}
            onChange={setContent}
            selectedTab={selectedTab}
            onTabChange={setSelectedTab}
            generateMarkdownPreview={markdown =>
              Promise.resolve(converter.makeHtml(markdown))
            }
            minEditorHeight={300}
            heightUnits="px"
          />
        </div>
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={loading} style={{padding: '10px 20px', background: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>
          {loading ? 'Creating...' : 'Create Note'}
        </button>
      </div>
    </form>
  );
};
