#!/usr/bin/env python3
"""
Generate a PDF guide for Skål WhatsApp attendance confirmation.
Creates WhatsApp-style mockup screenshots and composes them into a professional PDF.
"""

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = BASE_DIR
LOGO_PATH = os.path.join(IMAGES_DIR, "Skål International Isla Mujeres-Puerto Morelos_Logo.png")

# Colors
WA_GREEN = (37, 211, 102)
WA_DARK_GREEN = (0, 128, 105)
WA_BG = (236, 229, 221)
WA_CHAT_BG = (225, 218, 208)
WA_BUBBLE_OUT = (212, 253, 198)
WA_BUBBLE_IN = (255, 255, 255)
WA_HEADER = (0, 92, 75)
PHONE_FRAME = (30, 30, 30)
FORM_BG = (255, 255, 255)
FORM_HEADER_BG = (0, 128, 105)
BUTTON_BLUE = (0, 122, 255)
BUTTON_GREEN = (37, 211, 102)
RADIO_BLUE = (0, 122, 255)
TEXT_DARK = (30, 30, 30)
TEXT_GRAY = (130, 130, 130)
TEXT_WHITE = (255, 255, 255)
FIELD_BG = (245, 245, 245)
FIELD_BORDER = (200, 200, 200)
UPLOAD_BG = (240, 248, 255)
UPLOAD_BORDER = (180, 210, 240)

# Phone dimensions
PHONE_W = 360
PHONE_H = 640
PHONE_PADDING = 16
CORNER_RADIUS = 24
HEADER_H = 56
STATUS_BAR_H = 24


def get_font(size=14, bold=False):
    """Try to load a nice font, fallback to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    if fill:
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
        draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)
    if outline:
        draw.arc([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)


def create_phone_frame(content_img):
    """Wrap a content image in a phone-like frame."""
    border = 8
    top_bezel = 32
    bottom_bezel = 24
    total_w = PHONE_W + border * 2
    total_h = PHONE_H + border * 2 + top_bezel + bottom_bezel

    img = Image.new("RGB", (total_w, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Phone body
    draw_rounded_rect(draw, [0, 0, total_w - 1, total_h - 1], 20, fill=PHONE_FRAME)

    # Screen area
    sx = border
    sy = border + top_bezel
    content_resized = content_img.resize((PHONE_W, PHONE_H), Image.LANCZOS)
    img.paste(content_resized, (sx, sy))

    # Top notch indicator
    notch_w = 80
    notch_h = 6
    nx = (total_w - notch_w) // 2
    ny = border + (top_bezel - notch_h) // 2
    draw_rounded_rect(draw, [nx, ny, nx + notch_w, ny + notch_h], 3, fill=(60, 60, 60))

    # Bottom bar indicator
    bar_w = 100
    bar_h = 4
    bx = (total_w - bar_w) // 2
    by = total_h - bottom_bezel + (bottom_bezel - bar_h) // 2
    draw_rounded_rect(draw, [bx, by, bx + bar_w, by + bar_h], 2, fill=(80, 80, 80))

    return img


def draw_wa_header(draw, y_start, title="LowCode Agency"):
    """Draw WhatsApp-style header."""
    font_title = get_font(16, bold=True)
    font_small = get_font(10)

    # Header background
    draw.rectangle([0, y_start, PHONE_W, y_start + HEADER_H], fill=WA_HEADER)

    # Back arrow
    draw.text((12, y_start + 18), "\u2190", fill=TEXT_WHITE, font=get_font(18, bold=True))

    # Profile circle
    cx, cy = 48, y_start + HEADER_H // 2
    r = 18
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WA_DARK_GREEN)
    draw.text((cx - 6, cy - 8), "S", fill=TEXT_WHITE, font=get_font(14, bold=True))

    # Title
    draw.text((76, y_start + 12), title, fill=TEXT_WHITE, font=font_title)
    draw.text((76, y_start + 32), "en l\u00ednea", fill=(180, 230, 200), font=font_small)


def draw_status_bar(draw, y=0):
    """Draw a simple status bar."""
    draw.rectangle([0, y, PHONE_W, y + STATUS_BAR_H], fill=WA_HEADER)
    font = get_font(10)
    draw.text((12, y + 6), "9:41", fill=TEXT_WHITE, font=font)
    draw.text((PHONE_W - 60, y + 6), "100%", fill=TEXT_WHITE, font=font)


def draw_chat_bubble(draw, y, text, is_outgoing=False, font_size=13):
    """Draw a WhatsApp chat bubble and return the bottom y position."""
    font = get_font(font_size)
    max_width = 240
    padding = 10

    lines = []
    for line in text.split('\n'):
        if line.strip() == '':
            lines.append('')
        else:
            wrapped = textwrap.wrap(line, width=32)
            lines.extend(wrapped if wrapped else [''])

    line_height = font_size + 4
    bubble_h = len(lines) * line_height + padding * 2

    text_widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_widths.append(bbox[2] - bbox[0])
    bubble_w = min(max(text_widths) + padding * 2 + 10, max_width) if text_widths else 100

    if is_outgoing:
        color = WA_BUBBLE_OUT
        x = PHONE_W - bubble_w - 16
    else:
        color = WA_BUBBLE_IN
        x = 16

    draw_rounded_rect(draw, [x, y, x + bubble_w, y + bubble_h], 10, fill=color)

    ty = y + padding
    for line in lines:
        draw.text((x + padding, ty), line, fill=TEXT_DARK, font=font)
        ty += line_height

    time_font = get_font(9)
    draw.text((x + bubble_w - 40, y + bubble_h - 16), "9:41", fill=TEXT_GRAY, font=time_font)

    return y + bubble_h + 8


def draw_wa_button(draw, y, text, x_center=None):
    """Draw a WhatsApp-style reply button and return bottom y."""
    font = get_font(13, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    btn_w = tw + 40
    btn_h = 36

    if x_center is None:
        x_center = PHONE_W // 2

    x = x_center - btn_w // 2

    draw_rounded_rect(draw, [x, y, x + btn_w, y + btn_h], 18,
                       fill=(255, 255, 255), outline=WA_DARK_GREEN, width=2)
    draw.text((x + 20, y + 8), text, fill=WA_DARK_GREEN, font=font)

    return y + btn_h + 6


def draw_form_field(draw, y, label, placeholder="", required=False):
    """Draw a form input field and return bottom y."""
    font_label = get_font(11, bold=True)
    font_input = get_font(11)

    label_text = label + (" *" if required else "")
    draw.text((20, y), label_text, fill=TEXT_DARK, font=font_label)
    y += 18

    draw_rounded_rect(draw, [20, y, PHONE_W - 20, y + 32], 6,
                       fill=FIELD_BG, outline=FIELD_BORDER, width=1)
    if placeholder:
        draw.text((28, y + 8), placeholder, fill=TEXT_GRAY, font=font_input)
    y += 40

    return y


def draw_radio_option(draw, y, text, selected=False):
    """Draw a radio button option and return bottom y."""
    font = get_font(12)
    cx, cy = 32, y + 10
    r = 9

    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RADIO_BLUE if selected else TEXT_GRAY, width=2)
    if selected:
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RADIO_BLUE)

    draw.text((50, y + 2), text, fill=TEXT_DARK, font=font)
    return y + 28


# ============================================================
# SCREEN GENERATORS
# ============================================================

def create_screen_1():
    """Screen 1: Initial WhatsApp chat with RSVP Skal button."""
    img = Image.new("RGB", (PHONE_W, PHONE_H), WA_CHAT_BG)
    draw = ImageDraw.Draw(img)

    draw_status_bar(draw)
    draw_wa_header(draw, STATUS_BAR_H)

    y = STATUS_BAR_H + HEADER_H + 16

    y = draw_chat_bubble(draw, y,
        "\u00a1Hola! Bienvenido.\nSoy el asistente virtual.\n\u00bfEn qu\u00e9 puedo ayudarte?",
        is_outgoing=False)

    y += 4

    y = draw_wa_button(draw, y, "Tucanes")
    y = draw_wa_button(draw, y, "RSVP Skal")

    # Highlight arrow
    font_arrow = get_font(22, bold=True)
    draw.text((PHONE_W // 2 + 70, y - 38), "\u2190", fill=(255, 50, 50), font=font_arrow)

    y += 16

    y = draw_chat_bubble(draw, y, "RSVP Skal", is_outgoing=True)

    return create_phone_frame(img)


def create_screen_2():
    """Screen 2: Bot responds with confirmation button."""
    img = Image.new("RGB", (PHONE_W, PHONE_H), WA_CHAT_BG)
    draw = ImageDraw.Draw(img)

    draw_status_bar(draw)
    draw_wa_header(draw, STATUS_BAR_H)

    y = STATUS_BAR_H + HEADER_H + 16

    y = draw_chat_bubble(draw, y, "RSVP Skal", is_outgoing=True)

    y += 8

    y = draw_chat_bubble(draw, y,
        "Por favor confirma tu\nasistencia al evento de\nSk\u00e5l International",
        is_outgoing=False)

    y += 4

    y = draw_wa_button(draw, y, "Confirmar asistencia")

    font_arrow = get_font(22, bold=True)
    draw.text((PHONE_W // 2 + 90, y - 38), "\u2190", fill=(255, 50, 50), font=font_arrow)

    return create_phone_frame(img)


def create_screen_3():
    """Screen 3: Attendance confirmation form."""
    img = Image.new("RGB", (PHONE_W, PHONE_H), FORM_BG)
    draw = ImageDraw.Draw(img)

    draw_status_bar(draw, 0)

    y = STATUS_BAR_H
    header_h = 70
    draw.rectangle([0, y, PHONE_W, y + header_h], fill=FORM_HEADER_BG)
    font_title = get_font(16, bold=True)
    font_sub = get_font(11)
    draw.text((20, y + 12), "Confirmaci\u00f3n de Asistencia", fill=TEXT_WHITE, font=font_title)
    draw.text((20, y + 36), "Sk\u00e5l International - Isla Mujeres", fill=(200, 240, 220), font=font_sub)
    draw.text((20, y + 50), "y Puerto Morelos", fill=(200, 240, 220), font=font_sub)

    y += header_h + 20

    y = draw_form_field(draw, y, "Tu nombre completo", "Escribe tu nombre...", required=True)
    y = draw_form_field(draw, y, "Email", "correo@ejemplo.com")
    y = draw_form_field(draw, y, "Tel\u00e9fono", "+52 ...")

    y += 8

    font_q = get_font(12, bold=True)
    draw.text((20, y), "\u00bfAsistir\u00e1s al evento? *", fill=TEXT_DARK, font=font_q)
    y += 24

    y = draw_radio_option(draw, y, "S\u00ed, asistir\u00e9", selected=True)
    y = draw_radio_option(draw, y, "No podr\u00e9 asistir", selected=False)

    y += 20

    btn_w = PHONE_W - 40
    draw_rounded_rect(draw, [20, y, 20 + btn_w, y + 44], 8, fill=WA_DARK_GREEN)
    font_btn = get_font(15, bold=True)
    bbox = draw.textbbox((0, 0), "Enviar", font=font_btn)
    tw = bbox[2] - bbox[0]
    draw.text((20 + (btn_w - tw) // 2, y + 12), "Enviar", fill=TEXT_WHITE, font=font_btn)

    return create_phone_frame(img)


def create_screen_4():
    """Screen 4: Guest question."""
    img = Image.new("RGB", (PHONE_W, PHONE_H), WA_CHAT_BG)
    draw = ImageDraw.Draw(img)

    draw_status_bar(draw)
    draw_wa_header(draw, STATUS_BAR_H)

    y = STATUS_BAR_H + HEADER_H + 16

    y = draw_chat_bubble(draw, y,
        "\u00a1Excelente! Gracias por\nconfirmar tu asistencia.\n\n\u00bfTraer\u00e1s un invitado?",
        is_outgoing=False)

    y += 4

    y = draw_wa_button(draw, y, "S\u00ed, traer\u00e9 un invitado")
    y = draw_wa_button(draw, y, "No, asistir\u00e9 solo/a")

    return create_phone_frame(img)


def create_screen_5():
    """Screen 5: Guest details form with payment upload."""
    img = Image.new("RGB", (PHONE_W, PHONE_H), FORM_BG)
    draw = ImageDraw.Draw(img)

    draw_status_bar(draw, 0)

    y = STATUS_BAR_H
    header_h = 50
    draw.rectangle([0, y, PHONE_W, y + header_h], fill=FORM_HEADER_BG)
    font_title = get_font(16, bold=True)
    draw.text((20, y + 14), "Datos del Invitado", fill=TEXT_WHITE, font=font_title)

    y += header_h + 16

    y = draw_form_field(draw, y, "Nombre completo del invitado", "Nombre...", required=True)
    y = draw_form_field(draw, y, "Email del invitado", "correo@ejemplo.com")
    y = draw_form_field(draw, y, "Tel\u00e9fono del invitado", "+52 ...")
    y = draw_form_field(draw, y, "Restricciones alimenticias", "Opcional...")

    y += 4

    font_label = get_font(12, bold=True)
    font_small = get_font(10)

    draw.text((20, y), "Comprobante de pago *", fill=TEXT_DARK, font=font_label)
    y += 20

    upload_h = 80
    draw_rounded_rect(draw, [20, y, PHONE_W - 20, y + upload_h], 8,
                       fill=UPLOAD_BG, outline=UPLOAD_BORDER, width=2)

    cx = PHONE_W // 2
    draw.text((cx - 12, y + 10), "[+]", fill=RADIO_BLUE, font=get_font(20, bold=True))
    draw.text((cx - 60, y + 40), "Subir foto del comprobante", fill=RADIO_BLUE, font=get_font(10))
    draw.text((cx - 30, y + 56), "Max 25 MB", fill=TEXT_GRAY, font=font_small)

    y += upload_h + 16

    btn_w = PHONE_W - 40
    draw_rounded_rect(draw, [20, y, 20 + btn_w, y + 44], 8, fill=WA_DARK_GREEN)
    font_btn = get_font(15, bold=True)
    bbox = draw.textbbox((0, 0), "Enviar", font=font_btn)
    tw = bbox[2] - bbox[0]
    draw.text((20 + (btn_w - tw) // 2, y + 12), "Enviar", fill=TEXT_WHITE, font=font_btn)

    return create_phone_frame(img)


# ============================================================
# PDF GENERATION
# ============================================================

class SkalPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header_bar(self):
        """Draw a green header bar."""
        self.set_fill_color(0, 128, 105)
        self.rect(0, 0, 210, 8, 'F')

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10,
                  "Sk\u00e5l International - Isla Mujeres y Puerto Morelos  |  P\u00e1gina " + str(self.page_no()),
                  align="C")

    def section_title(self, num, title):
        """Draw a step number and title."""
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 128, 105)

        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(0, 128, 105)
        self.ellipse(x, y, 10, 10, 'F')
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(255, 255, 255)
        if num < 10:
            self.text(x + 3.2, y + 7.2, str(num))
        else:
            self.text(x + 1.5, y + 7.2, str(num))

        self.set_x(x + 14)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 128, 105)
        self.cell(0, 10, title)
        self.ln(14)

    def body_text(self, text):
        """Write body text."""
        self.set_font("Helvetica", "", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet_item(self, bold_text, normal_text, highlight=False):
        """Draw a single bullet item with bold label and normal description."""
        x_start = self.get_x() + 6
        self.set_x(x_start)

        if highlight:
            self.set_text_color(200, 50, 0)
        else:
            self.set_text_color(50, 50, 50)

        self.set_font("Helvetica", "B", 10)
        self.cell(4, 6, "\u00bb")
        self.cell(2, 6, "")

        # Use multi_cell for the full text to avoid truncation
        full_text = bold_text + "  " + normal_text
        remaining_w = self.w - self.get_x() - self.r_margin

        # Write bold part
        bold_w = self.get_string_width(bold_text + "  ")
        if bold_w < remaining_w:
            self.cell(bold_w, 6, bold_text + "  ")
            self.set_font("Helvetica", "I" if not highlight else "BI", 10)
            if not highlight:
                self.set_text_color(100, 100, 100)
            self.cell(0, 6, normal_text)
        else:
            self.multi_cell(remaining_w, 6, full_text)

        self.set_text_color(50, 50, 50)
        self.ln(8)

    def important_note(self, text):
        """Draw a highlighted important note box."""
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(255, 180, 0)
        x = self.get_x()
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin

        # Calculate height needed using multi_cell dry run
        self.set_font("Helvetica", "", 10)
        # Estimate lines needed
        avg_chars_per_line = (w - 8) / 2.2  # rough estimate
        num_lines = len(text) / avg_chars_per_line + text.count('\n') + 1
        h = num_lines * 5 + 18  # 18 for header + padding
        h = max(h, 24)

        self.rect(x, y, w, h, 'FD')
        self.set_x(x + 4)
        self.set_y(y + 3)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(180, 100, 0)
        self.cell(0, 5, "IMPORTANTE:")
        self.ln(7)
        self.set_x(x + 4)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(100, 70, 0)
        self.multi_cell(w - 8, 5, text)
        self.set_y(y + h + 4)

    def green_box(self, text):
        """Draw a green info box."""
        self.set_fill_color(230, 250, 240)
        self.set_draw_color(0, 128, 105)
        x = self.get_x()
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin

        self.set_font("Helvetica", "", 10)
        avg_chars_per_line = (w - 8) / 2.2
        num_lines = len(text) / avg_chars_per_line + text.count('\n') + 1
        h = max(num_lines * 5 + 10, 16)

        self.rect(x, y, w, h, 'FD')
        self.set_xy(x + 4, y + 3)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 90, 70)
        self.multi_cell(w - 8, 5, text)
        self.set_y(y + h + 4)


def generate_pdf():
    """Generate the complete PDF guide."""
    print("Generating mockup screenshots...")

    screens = [
        create_screen_1(),
        create_screen_2(),
        create_screen_3(),
        create_screen_4(),
        create_screen_5(),
    ]

    screen_paths = []
    for i, screen in enumerate(screens):
        path = os.path.join(OUTPUT_DIR, f"_temp_screen_{i+1}.png")
        screen.save(path, "PNG")
        screen_paths.append(path)

    print("Creating PDF...")

    pdf = SkalPDF()
    pdf.set_margins(15, 15, 15)

    # Page width for content
    content_w = 210 - 15 - 15  # 180mm

    # =============================================
    # PAGE 1: COVER
    # =============================================
    pdf.add_page()
    pdf.header_bar()

    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=25, y=30, w=160)

    pdf.ln(80)

    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(0, 128, 105)
    pdf.cell(0, 14, "Gu\u00eda de Confirmaci\u00f3n", align="C")
    pdf.ln(14)
    pdf.cell(0, 14, "de Asistencia", align="C")
    pdf.ln(20)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "C\u00f3mo confirmar tu asistencia a eventos", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, "de Sk\u00e5l International por WhatsApp", align="C")
    pdf.ln(20)

    # WhatsApp number box
    pdf.set_fill_color(230, 250, 240)
    pdf.set_draw_color(0, 128, 105)
    box_w = 120
    box_x = (210 - box_w) / 2
    pdf.rect(box_x, pdf.get_y(), box_w, 30, 'FD')
    pdf.set_xy(box_x, pdf.get_y() + 4)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 90, 70)
    pdf.cell(box_w, 6, "N\u00famero de WhatsApp:", align="C")
    pdf.ln(8)
    pdf.set_x(box_x)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 128, 105)
    pdf.cell(box_w, 10, "+1 (555) 812-3144", align="C")
    pdf.ln(24)

    # Decorative line
    pdf.set_draw_color(0, 128, 105)
    pdf.set_line_width(0.5)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "Sk\u00e5l International - Isla Mujeres y Puerto Morelos", align="C")

    # =============================================
    # PAGE 2: STEPS 1 & 2 with screen 1
    # =============================================
    pdf.add_page()
    pdf.header_bar()
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(0, 128, 105)
    pdf.cell(0, 10, "Instrucciones Paso a Paso", align="L")
    pdf.ln(12)

    pdf.body_text(
        "A continuaci\u00f3n te mostramos c\u00f3mo confirmar tu asistencia a los eventos "
        "de Sk\u00e5l International a trav\u00e9s de nuestro asistente de WhatsApp. "
        "El proceso es r\u00e1pido y sencillo."
    )
    pdf.ln(2)

    # Step 1
    pdf.section_title(1, "Inicia la conversaci\u00f3n")
    pdf.body_text(
        "Agrega el n\u00famero +1 (555) 812-3144 a tus contactos de WhatsApp. "
        "Env\u00eda cualquier mensaje (por ejemplo \"Hola\") "
        "para iniciar la conversaci\u00f3n con el asistente virtual."
    )
    pdf.ln(1)

    # Step 2
    pdf.section_title(2, "Selecciona \"RSVP Sk\u00e5l\"")
    pdf.body_text(
        "El asistente te mostrar\u00e1 un men\u00fa con opciones. "
        "Selecciona el bot\u00f3n \"RSVP Sk\u00e5l\" para iniciar el proceso de "
        "confirmaci\u00f3n de asistencia al evento."
    )

    # Place screen 1 - centered
    img_w = 42
    img_x = (210 - img_w) / 2
    pdf.image(screen_paths[0], x=img_x, y=pdf.get_y() + 2, w=img_w)
    pdf.ln(82)

    # =============================================
    # PAGE 3: STEP 3 with screen 2 + STEP 4 with screen 3
    # =============================================
    pdf.add_page()
    pdf.header_bar()
    pdf.ln(6)

    pdf.section_title(3, "Confirma tu asistencia")
    pdf.body_text(
        "Despu\u00e9s de seleccionar \"RSVP Sk\u00e5l\", el asistente te enviar\u00e1 un mensaje "
        "con un bot\u00f3n para confirmar tu asistencia. Presiona el bot\u00f3n "
        "\"Confirmar asistencia\" para abrir el formulario."
    )

    # Screen 2 on left, text on right
    img_w = 42
    img_x = 18
    img_y = pdf.get_y() + 2
    pdf.image(screen_paths[1], x=img_x, y=img_y, w=img_w)

    text_x = img_x + img_w + 8
    pdf.set_xy(text_x, img_y + 6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    text_w = 210 - text_x - 15
    pdf.multi_cell(text_w, 5,
        "Al presionar el bot\u00f3n se abrir\u00e1 un formulario donde podr\u00e1s registrar tu asistencia al evento.")

    pdf.set_xy(text_x, pdf.get_y() + 4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 128, 105)
    pdf.multi_cell(text_w, 5,
        "Tip: Si el bot\u00f3n no aparece, env\u00eda \"RSVP Sk\u00e5l\" como mensaje de texto.")

    pdf.set_y(img_y + 80)
    pdf.ln(4)

    # STEP 4: Fill the form + Screen 3 (side by side)
    pdf.section_title(4, "Completa el formulario")
    pdf.body_text(
        "Se abrir\u00e1 el formulario de \"Confirmaci\u00f3n de Asistencia\". "
        "Completa los siguientes campos:"
    )

    # Place screen 3 on the right, bullets on the left
    form_img_w = 38
    form_img_x = 210 - 15 - form_img_w  # right-aligned
    form_img_y = pdf.get_y()
    pdf.image(screen_paths[2], x=form_img_x, y=form_img_y, w=form_img_w)

    # Bullet points on the left side (constrained width)
    pdf.bullet_item("Tu nombre completo", "(obligatorio)")
    pdf.bullet_item("Email", "(opcional)")
    pdf.bullet_item("Tel\u00e9fono", "(opcional)")
    pdf.bullet_item("\u00bfAsistir\u00e1s al evento?",
                    "Selecciona \"S\u00ed, asistir\u00e9\"")

    pdf.body_text("Presiona \"Enviar\" para confirmar.")

    # Ensure we're past the image before continuing
    form_img_bottom = form_img_y + form_img_w * (704 / 376)  # aspect ratio of phone frame
    if pdf.get_y() < form_img_bottom:
        pdf.set_y(form_img_bottom + 4)

    # =============================================
    # PAGE: STEP 5 - GUEST QUESTION + screen 4
    # =============================================
    pdf.add_page()
    pdf.header_bar()
    pdf.ln(6)

    pdf.section_title(5, "Invitado (opcional)")
    pdf.body_text(
        "Despu\u00e9s de confirmar tu asistencia, el asistente te preguntar\u00e1 si "
        "traer\u00e1s un invitado al evento. Tienes dos opciones:"
    )

    # Option boxes side by side
    y_boxes = pdf.get_y()
    box_w = 82

    # Option A
    pdf.set_fill_color(230, 250, 240)
    pdf.set_draw_color(0, 128, 105)
    pdf.rect(15, y_boxes, box_w, 28, 'FD')
    pdf.set_xy(17, y_boxes + 3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 128, 105)
    pdf.cell(box_w - 4, 5, "Opci\u00f3n A:", align="L")
    pdf.set_xy(17, y_boxes + 10)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(0, 90, 70)
    pdf.multi_cell(box_w - 4, 4, "\"S\u00ed, traer\u00e9 un invitado\"\n(Contin\u00faa al paso 6)")

    # Option B
    pdf.set_fill_color(245, 245, 245)
    pdf.set_draw_color(150, 150, 150)
    pdf.rect(15 + box_w + 6, y_boxes, box_w, 28, 'FD')
    pdf.set_xy(15 + box_w + 8, y_boxes + 3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(box_w - 4, 5, "Opci\u00f3n B:", align="L")
    pdf.set_xy(15 + box_w + 8, y_boxes + 10)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(box_w - 4, 4, "\"No, asistir\u00e9 solo/a\"\n(\u00a1Tu registro est\u00e1 completo!)")

    pdf.set_y(y_boxes + 34)

    # Screen 4 centered
    img_w = 42
    img_x = (210 - img_w) / 2
    pdf.image(screen_paths[3], x=img_x, y=pdf.get_y() + 2, w=img_w)
    pdf.ln(86)

    # =============================================
    # STEP 6: GUEST DETAILS + screen 5
    # =============================================
    pdf.section_title(6, "Datos del invitado y comprobante de pago")
    pdf.body_text(
        "Si seleccionaste que traer\u00e1s un invitado, se abrir\u00e1 un formulario "
        "para registrar los datos de tu invitado:"
    )

    pdf.bullet_item("Nombre completo del invitado", "(obligatorio)")
    pdf.bullet_item("Email del invitado", "(opcional)")
    pdf.bullet_item("Tel\u00e9fono del invitado", "(opcional)")
    pdf.bullet_item("Restricciones alimenticias", "(opcional)")
    pdf.bullet_item("Comprobante de pago", "(OBLIGATORIO)", highlight=True)

    pdf.ln(2)

    # Important note about payment
    pdf.important_note(
        "Si traes un invitado, es OBLIGATORIO subir el comprobante de pago "
        "de tu invitado. Toma una foto clara del comprobante de transferencia "
        "o recibo de pago y s\u00fabela en la secci\u00f3n \"Comprobante de pago\" del formulario. "
        "El archivo no debe exceder los 25 MB."
    )

    pdf.ln(2)

    # Screen 5 centered
    img_w = 42
    img_x = (210 - img_w) / 2
    if pdf.get_y() + 82 > 275:
        pdf.add_page()
        pdf.header_bar()
        pdf.ln(6)
    pdf.image(screen_paths[4], x=img_x, y=pdf.get_y() + 2, w=img_w)
    pdf.ln(84)

    # =============================================
    # NOTES SECTION (same page if space, else new page)
    # =============================================
    if pdf.get_y() + 60 > 275:
        pdf.add_page()
        pdf.header_bar()
        pdf.ln(6)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 128, 105)
    pdf.cell(0, 10, "Notas Importantes")
    pdf.ln(12)

    notes = [
        "El n\u00famero de WhatsApp es: +1 (555) 812-3144",
        "Si no recibes respuesta, intenta enviar \"Hola\" nuevamente.",
        "Si traes invitado, debes subir el comprobante de pago de tu invitado.",
        "Puedes confirmar tu asistencia en cualquier momento antes del evento.",
        "Si tienes problemas con el asistente virtual, contacta a la directiva.",
    ]

    for note in notes:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.set_x(20)
        pdf.cell(4, 6, "\u00bb")
        pdf.cell(2, 6, "")
        pdf.cell(0, 6, note)
        pdf.ln(8)

    pdf.ln(6)

    pdf.green_box(
        "\u00a1Recuerda! Tu confirmaci\u00f3n nos ayuda a organizar mejor los eventos. "
        "\u00a1Agradecemos tu pronta respuesta!"
    )

    # =============================================
    # SAVE PDF
    # =============================================
    output_path = os.path.join(OUTPUT_DIR, "guia-confirmacion-asistencia-whatsapp.pdf")
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")

    # Clean up temp images
    for path in screen_paths:
        if os.path.exists(path):
            os.remove(path)

    print("Temporary files cleaned up.")
    print("Done!")


if __name__ == "__main__":
    generate_pdf()
