// Skål International Mujeres Puerto Morelos - JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            });
        });
    }

    // Header scroll effect
    const header = document.querySelector('.main-header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }

        lastScroll = currentScroll;
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form submission handling
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Gracias por tu mensaje. Nos pondremos en contacto contigo pronto.');
            contactForm.reset();
        });
    }

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Animate sections on scroll
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // Don't animate hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.opacity = '1';
        hero.style.transform = 'translateY(0)';
    }

    // Don't animate page header
    const pageHeader = document.querySelector('.page-header');
    if (pageHeader) {
        pageHeader.style.opacity = '1';
        pageHeader.style.transform = 'translateY(0)';
    }

    initRsvpForm();

    console.log('Skål International Mujeres Puerto Morelos - Website loaded');
});

const RSVP_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzBkUBFLg3y_faTZGcoQ1qyZQIKY5hB0KLWQ6TQhrfkk4xSxfQbeZcRG5Ps2usnrNs/exec';

function isEventPast(eventDate) {
    const today = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Cancun' }).format(new Date());
    return today > eventDate;
}

function closeRsvpForm(form) {
    form.style.display = 'none';

    const container = form.closest('.rsvp-form-container');
    if (!container || container.querySelector('.rsvp-closed-message')) return;

    const closedMessage = document.createElement('p');
    closedMessage.className = 'rsvp-closed-message';
    closedMessage.textContent = 'El periodo de confirmación para este evento ha finalizado.';
    container.appendChild(closedMessage);
}

function initRsvpForm() {
    const form = document.getElementById('rsvp-form');
    if (!form) return;

    const eventDate = form.dataset.eventDate;
    if (eventDate && isEventPast(eventDate)) {
        closeRsvpForm(form);
        return;
    }

    const tipoAsistencia = document.querySelectorAll('input[name="tipo_asistencia"]');
    const guestFields = document.getElementById('guest-fields');
    const guestInputs = guestFields ? guestFields.querySelectorAll('input') : [];
    const formMessage = document.getElementById('form-message');

    tipoAsistencia.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'con_invitado') {
                guestFields.classList.add('visible');
                guestInputs.forEach(input => input.required = true);
            } else {
                guestFields.classList.remove('visible');
                guestInputs.forEach(input => {
                    input.required = false;
                    input.value = '';
                });
            }
        });
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        if (eventDate && isEventPast(eventDate)) {
            closeRsvpForm(form);
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Enviando...';
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const params = new URLSearchParams(formData).toString();

        fetch(`${RSVP_SCRIPT_URL}?${params}`, {
            method: 'GET',
            mode: 'no-cors'
        })
        .then(() => {
            formMessage.style.display = 'block';
            formMessage.style.color = '#27ae60';
            formMessage.textContent = '¡Gracias! Tu asistencia ha sido confirmada. Te enviaremos más detalles pronto.';
            form.reset();
            guestFields.classList.remove('visible');
            guestInputs.forEach(input => input.required = false);
        })
        .catch(() => {
            formMessage.style.display = 'block';
            formMessage.style.color = '#e74c3c';
            formMessage.textContent = 'Hubo un error. Por favor intenta de nuevo o contáctanos directamente.';
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
    });
}
