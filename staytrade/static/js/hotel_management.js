class HotelCalendar {
    constructor() {
        this.calendar = null;
        this.roomTypeSelect = document.getElementById('roomTypeSelect');
        this.mealPlanSelect = document.getElementById('mealPlanSelect');
        this.initializeCalendar();
        this.setupEventListeners();
    }

initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) {
        console.error('No se encuentra el elemento calendar');
        return;
    }

    this.calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth'
        },
        select: (info) => this.handleDateSelection(info),
        events: (info, successCallback, failureCallback) => {
            this.loadPrices(info, successCallback, failureCallback);
        },
        // Añadimos la configuración de visualización de eventos
        eventContent: (arg) => {
            return {
                html: `
                    <div class="fc-event-main-content" style="padding: 2px;">
                        <div style="font-weight: bold; color: #2c3e50;">
                            ${arg.event.extendedProps.price}€
                        </div>
                    </div>
                `
            };
        },
        // Configuración adicional para mejorar la visualización
        eventDisplay: 'block',
        eventBackgroundColor: '#ffffff',
        eventBorderColor: '#e0e0e0',
        eventTextColor: '#2c3e50'
    });

    this.calendar.render();
}

    setupEventListeners() {
        this.roomTypeSelect.addEventListener('change', () => {
            this.calendar.refetchEvents();
        });

        this.mealPlanSelect.addEventListener('change', () => {
            this.calendar.refetchEvents();
        });
    }

    async loadPrices(info, successCallback, failureCallback) {
        try {
            const params = new URLSearchParams({
                room_type_id: this.roomTypeSelect.value || '',
                meal_plan_id: this.mealPlanSelect.value || '',
                start: this.formatDate(info.start),
                end: this.formatDate(info.end)
            });

            const response = await fetch(`/api/room-prices/calendar_data/?${params}`);

            if (!response.ok) {
                throw new Error('Error al cargar los precios');
            }

            const data = await response.json();
            successCallback(data);
        } catch (error) {
            console.error('Error cargando precios:', error);
            failureCallback(error);
        }
    }

    async handleDateSelection(info) {
        if (!this.validateSelections()) return;

        try {
            const price = await this.showPricePrompt();
            if (!price) return;

            const response = await fetch('/api/room-prices/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    room_type_id: this.roomTypeSelect.value,
                    meal_plan_id: this.mealPlanSelect.value,
                    start_date: this.formatDate(info.start),
                    end_date: this.formatDate(info.end),
                    price: parseFloat(price)
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al guardar los precios');
            }

            const data = await response.json();
            toastr.success('Precios guardados correctamente');
            this.calendar.refetchEvents();

        } catch (error) {
            console.error('Error:', error);
            toastr.error(error.message);
        }
    }

    // Utilidades
    formatDate(date) {
        return date.toISOString().split('T')[0];
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    validateSelections() {
        if (!this.roomTypeSelect.value || !this.mealPlanSelect.value) {
            toastr.warning('Por favor, seleccione tipo de habitación y plan de comidas');
            return false;
        }
        return true;
    }

    showPricePrompt() {
        return new Promise((resolve) => {
            const price = prompt('Introduce el precio:');
            if (!price || isNaN(price) || price <= 0) {
                toastr.warning('Por favor, introduce un precio válido');
                resolve(null);
            } else {
                resolve(price);
            }
        });
    }
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const hotelCalendar = new HotelCalendar();
});
