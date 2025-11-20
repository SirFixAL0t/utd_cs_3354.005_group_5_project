import { useState, useEffect } from "react";

export default function Calendar() {
  const today = new Date();
  const [month, setMonth] = useState(today.getMonth());
  const [year, setYear] = useState(today.getFullYear());
  const [calendarDays, setCalendarDays] = useState([]);
  const [eventsByDate, setEventsByDate] = useState({});

  useEffect(() => {
    setCalendarDays(generateCalendar(month, year, eventsByDate));
  }, [month, year, eventsByDate]);

  useEffect(() => {
    // fetch events for the user (try authenticated then public fallback)
    async function fetchEvents() {
      const base = "http://localhost:8000";
      const token = localStorage.getItem("access_token");
      const headers = token
        ? { Authorization: `Bearer ${token}` }
        : { Accept: "application/json" };

      try {
        const calRes = await fetch(`${base}/calendar`, { headers, credentials: "include" });
        let calendars = [];
        if (calRes.ok) {
          calendars = await calRes.json();
        }
        const calendarId = calendars[0].calendar_id;
        let res = await fetch(`${base}/calendar/${calendarId}/events`, { headers, credentials: "include" });
       
        const events = await res.json();

        // build map of events keyed by local date YYYY-MM-DD
        const map = {};
        for (const ev of events) {
          if (!ev.start_time) continue;
          const d = new Date(ev.start_time);
          const key = dateKey(d);
          if (!map[key]) map[key] = [];
          map[key].push(ev);
        }
        setEventsByDate(map);
      } catch (err) {
        // keep eventsByDate empty on error — optionally log for dev
        console.error("Failed to fetch events:", err);
        setEventsByDate({});
      }
    }

    fetchEvents();
  }, []);

  function nextMonth() {
    // use Date arithmetic to avoid year/month edge-case bugs
    const d = new Date(year, month + 1, 1);
    setMonth(d.getMonth());
    setYear(d.getFullYear());
  }

  function prevMonth() {
    const d = new Date(year, month - 1, 1);
    setMonth(d.getMonth());
    setYear(d.getFullYear());
  }

  return (
    <div className="calendar-container">
      <div className="calendar-header">
        <button onClick={prevMonth}>←</button>
        <h3>
          {new Date(year, month).toLocaleString("default", {
            month: "long",
          })}{" "}
          {year}
        </h3>
        <button onClick={nextMonth}>→</button>
      </div>

      <div className="calendar-grid">
        <span>Su</span><span>Mo</span><span>Tu</span>
        <span>We</span><span>Th</span><span>Fr</span><span>Sa</span>

        {calendarDays.map((day, idx) => (
          <div
            key={idx}
            className={`calendar-day ${
              day.isCurrentMonth ? "" : "faded"
            } ${day.isToday ? "today" : ""}`}
          >
            <div className="day-number">{day.day}</div>
            <div className="events">
              {day.events && day.events.length > 0 ? (
                day.events.slice(0, 3).map((ev, i) => (
                  <div key={i} className="event-badge" title={ev.title}>
                    {ev.title}
                  </div>
                ))
              ) : null}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* -----------------------------
   CALENDAR GENERATION LOGIC
-------------------------------- */
function generateCalendar(month, year, eventsByDate = {}) {
  const days = [];

  const firstDayOfMonth = new Date(year, month, 1);
  const lastDayOfMonth = new Date(year, month + 1, 0);

  const firstWeekday = firstDayOfMonth.getDay();
  const totalDays = lastDayOfMonth.getDate();
  // Leading days from previous month 
  const prevMonthLastDate = new Date(year, month, 0).getDate();
  // i = index of first day of current month
  // so fill prev month days - i to 0 
  for (let i = firstWeekday - 1; i >= 0; i--) {
    const dayNum = prevMonthLastDate - i;
    const date = new Date(year, month - 1, dayNum);
    days.push({
      date,
      day: date.getDate(),
      isCurrentMonth: false,
      isToday: isToday(date),
      events: []
    });
  }

  // Days in current month
  for (let i = 1; i <= totalDays; i++) {
    const date = new Date(year, month, i);
    const key = dateKey(date);
    days.push({
      date,
      day: i,
      isCurrentMonth: true,
      isToday: isToday(date),
      events: eventsByDate[key] || [],
    });
  }

  // Trailing days from next month so the grid completes full weeks
  const remainder = days.length % 7;
  const daysNeeded = remainder === 0 ? 0 : 7 - remainder;
  for (let i = 1; i <= daysNeeded; i++) {
    const date = new Date(year, month + 1, i);
    days.push({
      date,
      day: date.getDate(),
      isCurrentMonth: false,
      isToday: isToday(date),
      events: []
    });
  }

  return days;
}

function pad(n) {
  return String(n).padStart(2, "0");
}

function dateKey(d) {
  // produce YYYY-MM-DD in local time
  const y = d.getFullYear();
  const m = pad(d.getMonth() + 1);
  const day = pad(d.getDate());
  return `${y}-${m}-${day}`;
}

function isToday(date) {
  const t = new Date();
  return (
    date.getDate() === t.getDate() &&
    date.getMonth() === t.getMonth() &&
    date.getFullYear() === t.getFullYear()
  );
}