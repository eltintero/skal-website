# Instructions for Adding New Eventos

This guide explains how to add new events (comidas mensuales and eventos especiales) to the Skål website.

## File Structure

```
skal-website/
├── comidas.html                 # Main events listing page
├── index.html                   # Homepage (upcoming events preview)
├── comida-[month]-[year].html   # Event detail page with RSVP
├── script.js                    # Shared RSVP logic (do not duplicate inline)
├── styles.css                   # All event/RSVP styles
├── images/
│   └── comida_[month]_[year].jpg # Event flyer images
└── COMIDAS_INSTRUCTIONS.md      # This file
```

## Event Types

### Comidas Mensuales
Regular monthly networking meals. Listed in the **Comidas Mensuales** section of `comidas.html`.

- **Template:** `comida-febrero-2026.html`
- **Tipo:** `Comida Mensual` or `Comida Reglamentaria`

### Eventos Especiales
One-off events (galas, celebrations, tournaments, etc.). Listed in the **Eventos Especiales** section of `comidas.html`.

- **Template:** `comida-junio-2026.html` (pricing + service details)
- **Tipo:** `Evento Especial`, `Cena Show`, etc.
- For events with dress code, also reference `comida-mayo-2026.html`

Both types use the same detail page format and RSVP form.

## Google Sheets RSVP Integration

All RSVP forms submit to a single Google Apps Script endpoint, configured in `script.js`:

```
https://script.google.com/macros/s/AKfycbzBkUBFLg3y_faTZGcoQ1qyZQIKY5hB0KLWQ6TQhrfkk4xSxfQbeZcRG5Ps2usnrNs/exec
```

**Do not** add inline RSVP scripts to detail pages. RSVP handling (guest toggle, submission, auto-close) lives entirely in `script.js`.

### Form fields submitted to Google Sheets

| Field | Type | Notes |
|-------|------|-------|
| `evento` | hidden | Unique event identifier |
| `tipo_asistencia` | radio | `"individual"` or `"con_invitado"` |
| `nombre` | text | Required |
| `email` | email | Required |
| `telefono` | tel | Required |
| `nombre_invitado` | text | Required when guest selected |
| `email_invitado` | email | Required when guest selected |
| `telefono_invitado` | tel | Required when guest selected |
| `comentarios` | textarea | Optional — dietary restrictions |

## RSVP Auto-Close

RSVP forms automatically close after the event date passes, preventing post-event spam submissions.

### How it works

1. Each RSVP form must include a `data-event-date` attribute in ISO format (`YYYY-MM-DD`).
2. On page load, `script.js` compares the event date against the current date in the **America/Cancun** timezone.
3. If today is **after** the event date, the form is hidden and a closed message is shown:
   > *"El periodo de confirmación para este evento ha finalizado."*
4. The form remains open on the event day itself and closes starting the next day at midnight.

### Required on every detail page

```html
<form id="rsvp-form" data-event-date="2026-06-11">
```

The `data-event-date` must match the event's actual date. The hidden `evento` field and `data-event-date` serve different purposes — both are required.

### Detail page scripts

Detail pages should only include:

```html
<script src="script.js"></script>
```

No inline `<script>` blocks for RSVP logic.

## Steps to Add a New Evento

### Step 1: Gather Event Details

Collect from the user:
- Event name/title
- Date and time
- Location/venue
- Event type (comida mensual or evento especial)
- Description
- Pricing (if applicable — Skållegas and invitados)
- Service includes (if applicable)
- RSVP confirmation deadline (display only, in the description)
- Flyer image

### Step 2: Create the Detail Page

1. Copy the appropriate template:
   - Standard comida → `comida-febrero-2026.html`
   - With pricing/dress code → `comida-mayo-2026.html`
   - Special event with service details → `comida-junio-2026.html`
2. Save as `comida-[month]-[year].html` (e.g., `comida-julio-2026.html`)
3. Update these sections:

**Page title and header:**
```html
<title>[Event Name] | Skål International Isla Mujeres-Puerto Morelos</title>
...
<section class="page-header">
    <h1>[Event Name]</h1>
    <p>[Month Year] &mdash; [Venue]</p>
</section>
```

**Event flyer:**
```html
<img src="images/comida_[month]_[year].jpg" alt="[Event Name]">
```

**Event details (standard fields):**
```html
<div class="detail-item">
    <span class="icon">&#128197;</span>
    <span><strong>Fecha:</strong> [Date in Spanish, e.g., "11 de Junio, 2026"]</span>
</div>
<div class="detail-item">
    <span class="icon">&#128336;</span>
    <span><strong>Horario:</strong> [Time, e.g., "12:30 PM - 2:00 PM"]</span>
</div>
<div class="detail-item">
    <span class="icon">&#128205;</span>
    <span><strong>Lugar:</strong> [Venue Name]</span>
</div>
<div class="detail-item">
    <span class="icon">&#127860;</span>
    <span><strong>Tipo:</strong> [Event Type]</span>
</div>
```

**Optional detail fields (when applicable):**
```html
<div class="detail-item">
    <span class="icon">&#128087;</span>
    <span><strong>Vestimenta:</strong> Formal</span>
</div>
<div class="detail-item">
    <span class="icon">&#128181;</span>
    <span><strong>Precio Skållegas:</strong> $550 MXN</span>
</div>
<div class="detail-item">
    <span class="icon">&#128181;</span>
    <span><strong>Precio Invitados:</strong> $1,200 MXN</span>
</div>
```

**RSVP form (required fields):**
```html
<form id="rsvp-form" data-event-date="2026-06-11">
    <input type="hidden" name="evento" value="[Event Name] - [Month Year]">
    ...
</form>
```

- `data-event-date` — ISO date for auto-close (`YYYY-MM-DD`)
- `evento` hidden field — unique name stored in Google Sheets

### Step 3: Update comidas.html

Add a new event card at the **top** of the appropriate `events-grid` (newest first). Use the `featured` class for the next upcoming event.

**Comidas Mensuales** section:
```html
<a href="comida-[month]-[year].html" class="event-card featured" style="text-decoration: none; cursor: pointer;">
    <div class="event-date">
        <span class="day">[DD]</span>
        <span class="month">[MMM]</span>
    </div>
    <div class="event-info">
        <h3>[Event Name]</h3>
        <p><strong>[Venue]</strong><br>[Time]<br>[Brief description]</p>
        <span style="display: inline-block; margin-top: 10px; color: #65A8DE; font-weight: 600; font-size: 0.9rem;">Ver detalles y RSVP &rarr;</span>
    </div>
</a>
```

**Eventos Especiales** section — same card format, placed in that section's `events-grid` instead.

### Step 4: Update index.html

If this is the next upcoming event, replace the card in the **Próximos Eventos** section:

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

### Step 5: Add Flyer Image

1. Save the image to `images/`
2. Use filename: `comida_[month]_[year].jpg` (e.g., `comida_julio_2026.jpg`)
3. Set the `src` in the detail page to match

### Step 6: Deploy

```bash
git add .
git commit -m "Add [Event Name] event for [Month] [Year]"
git push
```

Site: https://skalislamujerespuertomorelos.org/

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

## Existing Events (2026)

| File | Event | Date | Section |
|------|-------|------|---------|
| `comida-enero-2026.html` | 1er Comida Reglamentaria y Toma de Protesta | Jan 30 | Comidas Mensuales |
| `comida-febrero-2026.html` | 2da Comida Reglamentaria | Feb 27 | Comidas Mensuales |
| `comida-marzo-2026.html` | 3ra Comida Reglamentaria y Aniversario | Mar 20 | Comidas Mensuales |
| `comida-abril-2026.html` | 4ta Comida Reglamentaria | Apr 17 | Comidas Mensuales |
| `comida-mayo-2026.html` | Cena de Gala - Junta Nacional 2026 | May 30 | Comidas Mensuales |
| `comida-junio-2026.html` | Inauguración del Mundial | Jun 11 | Eventos Especiales |

## Example Prompts

**Monthly comida:**
> Add a new comida for July 2026. Event name: 5ta Comida Reglamentaria. Date: July 25, 2026. Time: 1:30 PM. Location: Hotel Xcaret. Description: Quinta comida reglamentaria del año. Flyer: comida_julio_2026.jpg

**Special event:**
> Add a special event for August 2026. Event name: Noche de Networking. Date: August 15, 2026. Time: 6:00 PM - 9:00 PM. Location: Puerto Morelos. Precio Skållegas: $600, Precio invitados: $1,000. Servicio incluye: cena de 3 tiempos y barra libre. Flyer attached.

## Checklist

- [ ] Detail page created from correct template
- [ ] `data-event-date` set on RSVP form (ISO format)
- [ ] Hidden `evento` field set (unique identifier)
- [ ] Flyer image saved to `images/`
- [ ] Event card added to `comidas.html` (correct section)
- [ ] `index.html` updated if this is the next upcoming event
- [ ] No inline RSVP `<script>` — only `<script src="script.js"></script>`
- [ ] Changes committed and pushed
