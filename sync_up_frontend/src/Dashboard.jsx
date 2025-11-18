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

  const friendsList = ["Frabina", "Fred", "Evan", "Fahim", "Hasti", "Henry"];

  useEffect(() => {
    injectFontAwesome();
  }, []);

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

  const handleCreateEvent = (e) => {
    e.preventDefault();
    console.log("New Event Created:", eventData);
    // TODO: send eventData to backend or state
    setShowModal(false);
    setEventData({ title: "", description: "", date: "", startTime: "", endTime: "", invitedFriends: [] });
  };

  return (
    <div className="w-full">
      <nav className="navbar">
        <div className="nav-left">
          <i className="fa-solid fa-calendar-days logo" />
          <span className="brand">SyncUp</span>
        </div>
        <div className="nav-right">
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
                <button className="btn create-poll">+ Create Poll</button>
              </div>
              <div className="poll">
                <div>
                  <i className="fa-regular fa-circle-check check" />
                  <div>
                    <p><strong>Best time for group study?</strong></p>
                    <span>8 votes</span>
                  </div>
                </div>
                <button className="vote-btn">Vote</button>
              </div>
              <div className="poll">
                <div>
                  <i className="fa-regular fa-circle-check check" />
                  <div>
                    <p><strong>Hangout this weekend?</strong></p>
                    <span>3 votes</span>
                  </div>
                </div>
                <button className="vote-btn">Vote</button>
              </div>
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
    </div>
  );
}
