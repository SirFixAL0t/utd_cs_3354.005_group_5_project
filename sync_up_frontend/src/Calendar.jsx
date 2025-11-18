import { useState, useEffect } from "react";

export default function Calendar() {
  const today = new Date();
  const [month, setMonth] = useState(today.getMonth());
  const [year, setYear] = useState(today.getFullYear());
  const [calendarDays, setCalendarDays] = useState([]);

  useEffect(() => {
    setCalendarDays(generateCalendar(month, year));
  }, [month, year]);

  function nextMonth() {
    if (month === 11) {
      setMonth(0);
      setYear(year + 1);
    } else {
      setMonth(month + 1);
    }
  }

  function prevMonth() {
    if (month === 0) {
      setMonth(11);
      setYear(year - 1);
    } else {
      setMonth(month - 1);
    }
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
            <div className="events"></div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* -----------------------------
   CALENDAR GENERATION LOGIC
-------------------------------- */
function generateCalendar(month, year) {
  const days = [];

  const firstDayOfMonth = new Date(year, month, 1);
  const lastDayOfMonth = new Date(year, month + 1, 0);

  const firstWeekday = firstDayOfMonth.getDay();
  const totalDays = lastDayOfMonth.getDate();

  // Days in current month
  for (let i = 1; i <= totalDays; i++) {
    const date = new Date(year, month, i);
    days.push({
      date,
      day: i,
      isCurrentMonth: true,
      isToday: isToday(date),
    });
  }


  return days;
}

function isToday(date) {
  const t = new Date();
  return (
    date.getDate() === t.getDate() &&
    date.getMonth() === t.getMonth() &&
    date.getFullYear() === t.getFullYear()
  );
}