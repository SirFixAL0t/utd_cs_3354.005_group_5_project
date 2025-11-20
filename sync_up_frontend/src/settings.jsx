import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./settings.css";

export default function Settings() {
  const navigate = useNavigate();

  const [open, setOpen] = useState({
    account: true,
    schedule: false,
    privacy: false,
    notif: false,
    sync: false,
    smart: false,
    appearance: false,
    data: false,
    feedback: false,
  });

  const [darkMode, setDarkMode] = useState(true);
  const [autoImport, setAutoImport] = useState(true);
  const [timeFormat, setTimeFormat] = useState("12h");
  const [notifTime, setNotifTime] = useState("15m");
  const [smartOn, setSmartOn] = useState(true);

  const injectFontAwesome = () => {
    if (!document.getElementById("fa-cdn")) {
      const link = document.createElement("link");
      link.id = "fa-cdn";
      link.rel = "stylesheet";
      link.href =
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css";
      document.head.appendChild(link);
    }
  };

  useEffect(() => {
    injectFontAwesome();
  }, []);

  const toggle = (key) => {
    setOpen((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="settings-wrapper">
      {/* nav same style */}
      <nav className="navbar">
        <div className="nav-left">
          <i className="fa-solid fa-calendar-days logo" />
          <span className="brand">SyncUp</span>
        </div>

        <div className="nav-right">
          <i
            className="fa-solid fa-arrow-left"
            onClick={() => navigate("/dashboard")}
            style={{ cursor: "pointer", fontSize: "1.2rem", marginRight: "12px" }}
          ></i>
          <div className="profile-circle">PN</div>
        </div>
      </nav>

      <main className="settings-main">
        <h2 className="settings-title">Settings</h2>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("account")}>
            <h3>Account Settings</h3>
            <i className={`fa-solid fa-chevron-${open.account ? "up" : "down"}`}></i>
          </div>

          {open.account && (
            <div className="section-body">
              <div className="setting-row">
                <label>Name</label>
                <input type="text" placeholder="Edit name" />
              </div>
              <div className="setting-row">
                <label>Email</label>
                <input type="text" placeholder="Edit email" />
              </div>
              <div className="setting-row">
                <label>Password</label>
                <input type="password" placeholder="Change password" />
              </div>
              <div className="setting-row">
                <button className="btn-small">Link School Account</button>
              </div>
              <div className="setting-row">
                <button className="btn-small">Upload Profile Picture</button>
              </div>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("schedule")}>
            <h3>Schedule & Calendar</h3>
            <i className={`fa-solid fa-chevron-${open.schedule ? "up" : "down"}`}></i>
          </div>

          {open.schedule && (
            <div className="section-body">
              <div className="setting-row">
                <label>Default Calendar View</label>
                <select>
                  <option>Day</option>
                  <option>Week</option>
                  <option>Month</option>
                </select>
              </div>

              <div className="toggle-row">
                <span>Auto Import Class Schedule</span>
                <input
                  type="checkbox"
                  checked={autoImport}
                  onChange={() => setAutoImport(!autoImport)}
                />
              </div>

              <div className="setting-row">
                <label>Time Format</label>
                <select value={timeFormat} onChange={(e) => setTimeFormat(e.target.value)}>
                  <option value="12h">12-hour</option>
                  <option value="24h">24-hour</option>
                </select>
              </div>

              <div className="setting-row">
                <label>Default Availability Hours</label>
                <input type="text" placeholder="ex: After 6 PM" />
              </div>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("privacy")}>
            <h3>Privacy Settings</h3>
            <i className={`fa-solid fa-chevron-${open.privacy ? "up" : "down"}`}></i>
          </div>

          {open.privacy && (
            <div className="section-body">
              <div className="setting-row">
                <label>Who can view my schedule?</label>
                <select>
                  <option>Friends only</option>
                  <option>Classmates</option>
                  <option>Everyone school-wide</option>
                  <option>Only me</option>
                </select>
              </div>

              <div className="toggle-row">
                <span>Hide event details</span>
                <input type="checkbox" />
              </div>

              <div className="toggle-row">
                <span>Allow friend requests</span>
                <input type="checkbox" defaultChecked />
              </div>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("notif")}>
            <h3>Notifications</h3>
            <i className={`fa-solid fa-chevron-${open.notif ? "up" : "down"}`}></i>
          </div>

          {open.notif && (
            <div className="section-body">
              <div className="toggle-row">
                <span>Class reminders</span>
                <input type="checkbox" defaultChecked />
              </div>
              <div className="toggle-row">
                <span>Event reminders</span>
                <input type="checkbox" defaultChecked />
              </div>
              <div className="toggle-row">
                <span>Study session suggestions</span>
                <input type="checkbox" defaultChecked />
              </div>
              <div className="toggle-row">
                <span>Friend availability alerts</span>
                <input type="checkbox" />
              </div>

              <div className="setting-row">
                <label>Reminder Time</label>
                <select value={notifTime} onChange={(e) => setNotifTime(e.target.value)}>
                  <option value="5m">5 minutes before</option>
                  <option value="15m">15 minutes before</option>
                  <option value="1h">1 hour before</option>
                </select>
              </div>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("sync")}>
            <h3>Sync & Integration</h3>
            <i className={`fa-solid fa-chevron-${open.sync ? "up" : "down"}`}></i>
          </div>

          {open.sync && (
            <div className="section-body">
              <button className="btn-small">Sync Google Calendar</button>
              <button className="btn-small">Sync Outlook/Apple</button>
              <button className="btn-small">Refresh Schedule</button>

              <div className="toggle-row">
                <span>Background Sync</span>
                <input type="checkbox" defaultChecked />
              </div>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("smart")}>
            <h3>Smart Suggestions</h3>
            <i className={`fa-solid fa-chevron-${open.smart ? "up" : "down"}`}></i>
          </div>

          {open.smart && (
            <div className="section-body">
              <div className="toggle-row">
                <span>Smart Suggestions</span>
                <input
                  type="checkbox"
                  checked={smartOn}
                  onChange={() => setSmartOn(!smartOn)}
                />
              </div>

              <div className="setting-row">
                <label>Suggestion Types</label>
                <select>
                  <option>Study sessions</option>
                  <option>Group work</option>
                  <option>Social hangouts</option>
                  <option>All of the above</option>
                </select>
              </div>

              <div className="setting-row">
                <label>Preferred Study Times</label>
                <input type="text" placeholder="ex: Evenings" />
              </div>

              <div className="setting-row">
                <label>Do Not Disturb</label>
                <input type="text" placeholder="ex: 11 PM - 8 AM" />
              </div>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("appearance")}>
            <h3>Appearance / Theme</h3>
            <i className={`fa-solid fa-chevron-${open.appearance ? "up" : "down"}`}></i>
          </div>

          {open.appearance && (
            <div className="section-body">
              <div className="toggle-row">
                <span>Dark Mode</span>
                <input
                  type="checkbox"
                  checked={darkMode}
                  onChange={() => setDarkMode(!darkMode)}
                />
              </div>

              <div className="setting-row">
                <label>Accent Color</label>
                <select>
                  <option>Blue</option>
                  <option>Green</option>
                  <option>Purple</option>
                  <option>Orange</option>
                </select>
              </div>

              <div className="setting-row">
                <label>Layout Spacing</label>
                <select>
                  <option>Compact</option>
                  <option>Normal</option>
                  <option>Spacious</option>
                </select>
              </div>

              <div className="setting-row">
                <label>Font Size</label>
                <select>
                  <option>Small</option>
                  <option>Medium</option>
                  <option>Large</option>
                </select>
              </div>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("data")}>
            <h3>Data & Security</h3>
            <i className={`fa-solid fa-chevron-${open.data ? "up" : "down"}`}></i>
          </div>

          {open.data && (
            <div className="section-body">
              <button className="btn-small">Download My Data</button>
              <button className="btn-small">Reset Settings</button>
              <button className="btn-small danger-btn">Delete Account</button>
            </div>
          )}
        </div>

        <div className="settings-card">
          <div className="section-header" onClick={() => toggle("feedback")}>
            <h3>Feedback & Support</h3>
            <i
              className={`fa-solid fa-chevron-${open.feedback ? "up" : "down"}`}
            ></i>
          </div>

          {open.feedback && (
            <div className="section-body">
              <button className="btn-small">Report a Bug</button>
              <button className="btn-small">Send Feedback</button>
              <button className="btn-small">About the App</button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
