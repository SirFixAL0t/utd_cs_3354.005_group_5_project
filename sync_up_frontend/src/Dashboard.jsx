import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import './dashboard.css';
import './Calendar.css';
import Calendar from './Calendar.jsx';

function injectFontAwesome() {
  if (typeof document === 'undefined') return;
  if (document.getElementById('fa-cdn')) return;
  const link = document.createElement('link');
  link.id = 'fa-cdn';
  link.rel = 'stylesheet';
  link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
  link.crossOrigin = 'anonymous';
  document.head.appendChild(link);
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);
  const [eventData, setEventData] = useState({
    title: "",
    description: "",
    date: "",
    startTime: "",
    endTime: "",
    invitedFriends: [],
  });
  const [polls, setPolls] = useState([]);
  const [showPollModal, setShowPollModal] = useState(false);
  const [pollForm, setPollForm] = useState({ question: '', options: ['',''] });

  const friendsList = ["Frabina", "Fred", "Evan", "Fahim", "Hasti", "Henry"];

  useEffect(() => {
    injectFontAwesome();
  }, []);

  useEffect(() => {
    // fetch polls from backend
    const fetchPolls = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/polls/');
        if (!res.ok) throw new Error('Failed to fetch polls');
        const data = await res.json();
        setPolls(data);
      } catch (err) {
        console.error('Error loading polls', err);
      }
    };
    fetchPolls();
  }, []);

  const handleVote = async (pollId, optionId) => {
    // For now the backend requires authentication to vote; this call will
    // fail with 401 if not logged in. We keep this here so when auth is wired
    // the UI will call correctly.
    try {
      const res = await fetch(`http://127.0.0.1:8000/polls/${pollId}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ poll_option_id: optionId }),
      });
      if (res.status === 401) {
        alert('Please log in to vote.');
        return;
      }
      if (!res.ok) {
        const err = await res.json();
        alert('Vote failed: ' + (err.detail || res.statusText));
        return;
      }
      // refresh polls after voting
      const refreshed = await fetch('http://127.0.0.1:8000/polls/');
      setPolls(await refreshed.json());
    } catch (e) {
      console.error(e);
      alert('Voting failed. Check console for details.');
    }
  };

  const handleLogout = () => {
    navigate('/login');
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEventData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFriendsChange = (e) => {
    const options = Array.from(e.target.selectedOptions).map(o => o.value);
    setEventData((prev) => ({ ...prev, invitedFriends: options }));
  };

  const handleCreateEvent = async (e) => {
    e.preventDefault();

    const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
    const token = localStorage.getItem("access_token");

    // find a calendar_id: try localStorage first, then fetch /calendars
    let calendarId = null;
    try {
      const stored = localStorage.getItem("calendars");
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) calendarId = parsed[0].calendar_id;
      }
    } catch (err) {
      console.warn("Failed to read stored calendars", err);
    }

    if (!calendarId) {
      try {
        const res = await fetch(`${API_BASE}/calendar`, {
          headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            "Content-Type": "application/json",
          },
        });
        if (res.ok) {
          const cals = await res.json();
          if (Array.isArray(cals) && cals.length > 0) calendarId = cals[0].calendar_id;
        }
      } catch (err) {
        console.error("Failed to fetch calendars", err);
      }
    }

    if (!calendarId) {
      alert("No calendar found. Create a calendar first.");
      return;
    }

    // build event payload (adjust field names if your EventCreate schema differs)
    let startIso = null;
    let endIso = null;
    try {
      if (eventData.date && eventData.startTime) {
        startIso = new Date(`${eventData.date}T${eventData.startTime}`).toISOString();
      }
      if (eventData.date && eventData.endTime) {
        endIso = new Date(`${eventData.date}T${eventData.endTime}`).toISOString();
      }
    } catch (err) {
      console.warn("Failed to parse dates/times", err);
    }

    const payload = {
      title: eventData.title,
      description: eventData.description,
      start_time: startIso,
      end_time: endIso,
      invited: eventData.invitedFriends, // adjust key if backend expects different name
    };

    try {
      const res = await fetch(`${API_BASE}/calendar/${calendarId}/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(payload),
      });

      if (res.status === 401) {
        alert("You must be logged in to create events.");
        return;
      }
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        alert("Create event failed: " + (err.detail || res.statusText));
        return;
      }

      // success: close modal, clear form, refresh UI as needed
      const created = await res.json().catch(() => null);
      console.log("Event created:", created);
      setShowModal(false);
      setEventData({ title: "", description: "", date: "", startTime: "", endTime: "", invitedFriends: [] });

      // optional: trigger a refresh for Calendar component
      window.dispatchEvent(new Event("events-updated"));
    } catch (err) {
      console.error(err);
      alert("Error creating event. See console.");
    }
  };



  return (
    <div className="w-full">
      <nav className="navbar">
        <div className="nav-left">
          <i className="fa-solid fa-calendar-days logo" />
          <span className="brand">SyncUp</span>
        </div>
        <div className="nav-right">
          {/* settings icon */}
          <i
            className="fa-solid fa-gear"
            style={{
              cursor: "pointer",
              fontSize: "1.2rem",
              marginRight: "12px",
              color: "#fff"
            }}
            onClick={() => navigate('/settings')}
          ></i>
          <div className="profile-circle">PN</div>
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      <main className="dashboard">
        {/* Top cards */}
        <section className="top-cards">
          <div className="card">
            <i className="fa-regular fa-calendar" />
            <h3>Upcoming Events</h3>
            <p>8</p>
          </div>
          <div className="card">
            <i className="fa-regular fa-clock" />
            <h3>Active Polls</h3>
            <p>5</p>
          </div>
          <div className="card">
            <i className="fa-solid fa-users" />
            <h3>Friends</h3>
            <p>24</p>
          </div>
        </section>

        {/* Main content */}
        <section className="main-content">
          <div className="left-column">
            <div className="schedule card-large">
              <div className="header">
                <h3>Schedule</h3>
                <button className="btn new-event" onClick={() => setShowModal(true)}>+ New Event</button>
              </div>
              <div className="calendar">
                <div className="calendar-toggle">
                  <button className="active">Calendar</button>
                  <button>List View</button>
                </div>
                <Calendar />
              </div>
            </div>

            <div className="active-polls card-large">
              <div className="header">
                <h3>Active Polls</h3>
                <button className="btn create-poll" onClick={() => setShowPollModal(true)}>+ Create Poll</button>
              </div>
              {polls.length === 0 && <p>No active polls</p>}
              {polls.map(p => (
                <div className="poll" key={p.poll_id}>
                  <div>
                    <i className="fa-regular fa-circle-check check" />
                    <div>
                      <p><strong>{p.question}</strong></p>
                      <span>{p.options.reduce((acc, o) => acc + o.votes, 0)} votes</span>
                    </div>
                  </div>
                  <div>
                    {p.options.map(o => (
                      <div key={o.option_id} style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px'}}>
                        <button className="vote-btn" onClick={() => handleVote(p.poll_id, o.option_id)}>Vote</button>
                        <span>{o.option_text} — {o.votes}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <aside className="right-column">
            <div className="friends card-side">
              <div className="header">
                <h3>Friends</h3>
                <button className="btn">+</button>
              </div>
              <ul>
                {friendsList.map(f => (
                  <li key={f}><span className="avatar online">{f[0]}{f[1]}</span> {f} <button>Invite</button></li>
                ))}
              </ul>
            </div>

            <div className="recent-activity card-side">
              <h3>Recent Activity</h3>
              <p><strong>Frabina</strong> voted on "Best time for group study?"<br /><span>2 hours ago</span></p>
              <p><strong>Fahim</strong> created a new event<br /><span>4 hours ago</span></p>
              <p><strong>Henry</strong> joined your study group<br /><span>Yesterday</span></p>
              <p>Poll "Vote for best group" ended with 12 votes<br /><span>Yesterday</span></p>
            </div>

            <div className="upcoming-events card-side">
              <h3>Upcoming Events</h3>
              <p><strong>Frabina</strong> is hosting Study Hangout<br /><span>In 5 hours</span></p>
              <p><strong>Evan</strong> is hosting Pumpkin Painting<br /><span>In 2 days</span></p>
            </div>
          </aside>
        </section>
      </main>

      {/* Modal for New Event */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h2>Create New Event</h2>
            <form onSubmit={handleCreateEvent}>
              <input type="text" name="title" placeholder="Event Title" value={eventData.title} onChange={handleInputChange} required />
              <textarea name="description" placeholder="Description" value={eventData.description} onChange={handleInputChange} />
              <input type="date" name="date" value={eventData.date} onChange={handleInputChange} required />
              <input type="time" name="startTime" value={eventData.startTime} onChange={handleInputChange} required />
              <input type="time" name="endTime" value={eventData.endTime} onChange={handleInputChange} required />
              <select multiple name="invitedFriends" value={eventData.invitedFriends} onChange={handleFriendsChange}>
                {friendsList.map(f => <option key={f} value={f}>{f}</option>)}
              </select>
              <div className="modal-buttons">
                <button type="submit" className="btn">Create Event</button>
                <button type="button" className="btn cancel-btn" onClick={() => setShowModal(false)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal for Create Poll */}
      {showPollModal && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h2>Create Poll</h2>
            <form onSubmit={async (e) => {
              e.preventDefault();
              try {
                const token = localStorage.getItem('access_token');
                const res = await fetch('http://127.0.0.1:8000/polls/', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
                  },
                  body: JSON.stringify({ question: pollForm.question, options: pollForm.options.filter(o => o && o.trim().length > 0) })
                });
                if (res.status === 401) {
                  alert('You must be logged in to create a poll.');
                  return;
                }
                if (!res.ok) {
                  const err = await res.json().catch(() => ({}));
                  alert('Create poll failed: ' + (err.detail || res.statusText));
                  return;
                }
                // refresh poll list
                const refreshed = await fetch('http://127.0.0.1:8000/polls/');
                setPolls(await refreshed.json());
                setShowPollModal(false);
                setPollForm({ question: '', options: ['',''] });
              } catch (err) {
                console.error(err);
                alert('Error creating poll. See console.');
              }
            }}>
              <input type="text" name="question" placeholder="Poll question" value={pollForm.question} onChange={(e) => setPollForm(f => ({ ...f, question: e.target.value }))} required />
              <div style={{marginTop: '8px'}}>
                <label>Options</label>
                {pollForm.options.map((opt, idx) => (
                  <div key={idx} style={{display: 'flex', gap: '8px', marginTop: '6px'}}>
                    <input type="text" value={opt} onChange={(e) => setPollForm(f => { const next = [...f.options]; next[idx] = e.target.value; return { ...f, options: next }; })} placeholder={`Option ${idx+1}`} required />
                    <button type="button" className="btn" onClick={() => setPollForm(f => ({ ...f, options: f.options.filter((_,i) => i !== idx) }))}>-</button>
                  </div>
                ))}
                <div style={{marginTop: '8px'}}>
                  <button type="button" className="btn" onClick={() => setPollForm(f => ({ ...f, options: [...f.options, ''] }))}>Add option</button>
                </div>
              </div>
              <div className="modal-buttons">
                <button type="submit" className="btn">Create Poll</button>
                <button type="button" className="btn cancel-btn" onClick={() => setShowPollModal(false)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
