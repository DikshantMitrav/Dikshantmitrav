"""Fetches live Bengaluru weather (Open-Meteo, free, no API key) and writes weather.svg."""
import json, urllib.request, sys
from datetime import datetime, timezone, timedelta

LAT, LON, CITY = 12.97, 77.59, "Bengaluru"
URL = ("https://api.open-meteo.com/v1/forecast"
       f"?latitude={LAT}&longitude={LON}"
       "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,is_day"
       "&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FKolkata")

CODES = {0:("Clear sky","☀️","🌙"),1:("Mainly clear","🌤️","🌙"),2:("Partly cloudy","⛅","☁️"),
         3:("Overcast","☁️","☁️"),45:("Foggy","🌫️","🌫️"),48:("Foggy","🌫️","🌫️"),
         51:("Light drizzle","🌦️","🌧️"),53:("Drizzle","🌦️","🌧️"),55:("Heavy drizzle","🌧️","🌧️"),
         61:("Light rain","🌦️","🌧️"),63:("Rain","🌧️","🌧️"),65:("Heavy rain","🌧️","🌧️"),
         80:("Rain showers","🌦️","🌧️"),81:("Rain showers","🌧️","🌧️"),82:("Violent showers","⛈️","⛈️"),
         95:("Thunderstorm","⛈️","⛈️"),96:("Thunderstorm","⛈️","⛈️"),99:("Thunderstorm","⛈️","⛈️")}

def render(d):
    c, day = d["current"], d["daily"]
    desc, icon_day, icon_night = CODES.get(c["weather_code"], ("—", "🌡️", "🌡️"))
    icon = icon_day if c.get("is_day", 1) else icon_night
    ist = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d %b, %I:%M %p IST")
    t, feels = round(c["temperature_2m"]), round(c["apparent_temperature"])
    hi, lo = round(day["temperature_2m_max"][0]), round(day["temperature_2m_min"][0])
    hum, wind = c["relative_humidity_2m"], round(c["wind_speed_10m"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="190" viewBox="0 0 480 190">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1a1b27"/><stop offset="1" stop-color="#24283b"/>
    </linearGradient>
    <linearGradient id="ac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#36BCF7"/><stop offset="1" stop-color="#bb9af7"/>
    </linearGradient>
    <style>
      text{{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif}}
      .city{{font-size:15px;font-weight:600;fill:#a9b1d6;letter-spacing:2px}}
      .temp{{font-size:58px;font-weight:700;fill:url(#ac)}}
      .desc{{font-size:17px;fill:#c0caf5}}
      .lbl{{font-size:11px;fill:#565f89;letter-spacing:1px}}
      .val{{font-size:16px;font-weight:600;fill:#c0caf5}}
      .upd{{font-size:10px;fill:#565f89}}
      .ic{{font-size:64px;animation:b 3s ease-in-out infinite}}
      @keyframes b{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
    </style>
  </defs>
  <rect width="480" height="190" rx="14" fill="url(#bg)"/>
  <rect width="480" height="4" rx="2" fill="url(#ac)"/>
  <text class="city" x="26" y="38">📍 {CITY.upper()}, INDIA</text>
  <text class="ic" x="26" y="118">{icon}</text>
  <text class="temp" x="112" y="114">{t}°C</text>
  <text class="desc" x="116" y="140">{desc} · feels {feels}°</text>
  <line x1="330" y1="30" x2="330" y2="160" stroke="#2f3549"/>
  <text class="lbl" x="350" y="48">HIGH / LOW</text><text class="val" x="350" y="68">{hi}° / {lo}°</text>
  <text class="lbl" x="350" y="96">HUMIDITY</text><text class="val" x="350" y="116">💧 {hum}%</text>
  <text class="lbl" x="350" y="144">WIND</text><text class="val" x="350" y="164">🍃 {wind} km/h</text>
  <text class="upd" x="26" y="172">Updated {ist}</text>
</svg>'''

if __name__ == "__main__":
    if len(sys.argv) > 1:  # local test with a JSON file
        data = json.load(open(sys.argv[1]))
    else:
        data = json.load(urllib.request.urlopen(URL, timeout=20))
    open("weather.svg", "w", encoding="utf-8").write(render(data))
    print("weather.svg written")
