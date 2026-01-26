# Instructions for Adding New Comidas

This guide is for Claude Code to add new monthly comidas to the Skål website.

## File Structure

```
/Users/jesus/projects/skal/
├── comidas.html                 # Main comidas listing page
├── comida-enero-2026.html       # Detail page template (use as reference)
├── images/
│   └── comida_enero.png         # Event flyer images go here
└── styles.css                   # Already has all required styles
```

## Google Sheets RSVP Integration

All comidas use the same Google Sheets endpoint:
```
https://script.google.com/macros/s/AKfycbx21wwO4OJJGostbUJhKU43K9c7s-_hhJyRKo1F-ovaIJrP0Krf0fYPBRw8FsuCBXHs/exec
```

The form submits these fields:
- `evento` - Event name (hidden field)
- `tipo_asistencia` - "individual" or "con_invitado"
- `nombre` - Attendee name
- `email` - Attendee email
- `telefono` - Attendee phone
- `nombre_invitado` - Guest name (if applicable)
- `email_invitado` - Guest email (if applicable)
- `telefono_invitado` - Guest phone (if applicable)
- `comentarios` - Comments/dietary restrictions

## Steps to Add a New Comida

### Step 1: Get Event Details from User

Ask for:
- Event name/title
- Date
- Time
- Location/Venue
- Brief description
- Flyer image (if available)

### Step 2: Create the Detail Page

1. Copy `comida-enero-2026.html` as template
2. Create new file named: `comida-[month]-[year].html` (e.g., `comida-febrero-2026.html`)
3. Update these sections:

**Page title and header:**
```html
<title>[Event Name] | Skål International Isla Mujeres-Puerto Morelos</title>
...
<section class="page-header">
    <h1>[Event Name]</h1>
    <p>[Event Subtitle/Description]</p>
</section>
```

**Event image:**
```html
<img src="images/[image-filename].png" alt="[Event Name]">
```

**Event details:**
```html
<div class="detail-item">
    <span class="icon">&#128197;</span>
    <span><strong>Fecha:</strong> [Date in Spanish, e.g., "28 de Febrero, 2026"]</span>
</div>
<div class="detail-item">
    <span class="icon">&#128336;</span>
    <span><strong>Horario:</strong> [Time, e.g., "2:00 PM - 6:00 PM"]</span>
</div>
<div class="detail-item">
    <span class="icon">&#128205;</span>
    <span><strong>Lugar:</strong> [Venue Name]</span>
</div>
<div class="detail-item">
    <span class="icon">&#127860;</span>
    <span><strong>Tipo:</strong> [Event Type, e.g., "Comida Mensual"]</span>
</div>
```

**Hidden form field (IMPORTANT):**
```html
<input type="hidden" name="evento" value="[Event Name] - [Month Year]">
```

This identifies the event in Google Sheets.

### Step 3: Update comidas.html

Add a new event card in the `events-grid` section:

```html
<a href="comida-[month]-[year].html" class="event-card" style="text-decoration: none; cursor: pointer;">
    <div class="event-date">
        <span class="day">[DD]</span>
        <span class="month">[MMM in Spanish caps, e.g., FEB]</span>
    </div>
    <div class="event-info">
        <h3>[Event Name]</h3>
        <p><strong>[Venue]</strong><br>[Time]<br>[Brief description]</p>
        <span style="display: inline-block; margin-top: 10px; color: #65A8DE; font-weight: 600; font-size: 0.9rem;">Ver detalles y RSVP &rarr;</span>
    </div>
</a>
```

### Step 4: Update index.html (Optional)

If this is the next upcoming event, update the event preview on the homepage:

```html
<a href="comida-[month]-[year].html" class="event-card" style="text-decoration: none;">
    <div class="event-date">
        <span class="day">[DD]</span>
        <span class="month">[MMM]</span>
    </div>
    <div class="event-info">
        <h3>[Event Name]</h3>
        <p>[Venue] | [Time]</p>
        <span style="display: inline-block; margin-top: 8px; color: #65A8DE; font-weight: 600; font-size: 0.85rem;">RSVP &rarr;</span>
    </div>
</a>
```

### Step 5: Add Flyer Image (if provided)

1. Save the image to `/Users/jesus/projects/skal/images/`
2. Use a simple filename: `comida_[month]_[year].png` (e.g., `comida_febrero_2026.png`)
3. Update the image src in the detail page

### Step 6: Deploy Changes

```bash
cd /Users/jesus/projects/skal
git add .
git commit -m "Add [Month] [Year] comida"
git push
```

Site will auto-update at: https://eltintero.github.io/skal-website/

## Spanish Month Abbreviations

| Month | Spanish | Abbreviation |
|-------|---------|--------------|
| January | Enero | ENE |
| February | Febrero | FEB |
| March | Marzo | MAR |
| April | Abril | ABR |
| May | Mayo | MAY |
| June | Junio | JUN |
| July | Julio | JUL |
| August | Agosto | AGO |
| September | Septiembre | SEP |
| October | Octubre | OCT |
| November | Noviembre | NOV |
| December | Diciembre | DIC |

## Example Prompt for Adding a Comida

"Add a new comida for February 2026. Event name: Comida de Febrero - Networking. Date: February 28, 2026. Time: 1:00 PM - 5:00 PM. Location: Restaurant La Habichuela, Cancún. Description: Monthly networking lunch with Skålleagues. I've added the flyer image as comida_febrero_2026.png in the images folder."
