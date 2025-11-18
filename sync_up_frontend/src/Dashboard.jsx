import { useEffect } from "react";
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

  useEffect(() => {
    injectFontAwesome();
  }, []);

  const handleLogout = () => {
    // Clear any stored login info if needed
    navigate('/login'); // redirect to login page
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
                <button className="btn new-event">+ New Event</button>
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
                <li><span className="avatar online">FE</span> Frabina E. <button>Invite</button></li>
                <li><span className="avatar online">FR</span> Fred E. <button>Invite</button></li>
                <li><span className="avatar online">ES</span> Evan S. <button>Invite</button></li>
                <li><span className="avatar offline">FX</span> Fahim H. <button>Invite</button></li>
                <li><span className="avatar offline">HP</span> Hasti P. <button>Invite</button></li>
                <li><span className="avatar offline">HX</span> Henry N. <button>Invite</button></li>
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
    </div>
  );
}
