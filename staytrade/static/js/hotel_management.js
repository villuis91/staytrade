document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) {
        console.error('No se encuentra el elemento calendar');
        return;
    }

    function formatDate(date) {
        // Convierte la fecha a YYYY-MM-DD
        return date.toISOString().split('T')[0];
    }

    function loadPrices(start, end, callback) {
        const roomTypeId = document.getElementById('roomTypeSelect').value;
        const mealPlanId = document.getElementById('mealPlanSelect').value;

        if (!roomTypeId || !mealPlanId) return;

        // Formateamos las fechas antes de enviarlas
        const formattedStart = formatDate(start);
        const formattedEnd = formatDate(end);

        fetch(`/api/room-prices/?room_type_id=${roomTypeId}&meal_plan_id=${mealPlanId}&start=${formattedStart}&end=${formattedEnd}`)
            .then(response => response.json())
            .then(data => callback(data));
    }

     function handleDateSelection(start, end, price) {
        const roomTypeId = document.getElementById('roomTypeSelect').value;
        const mealPlanId = document.getElementById('mealPlanSelect').value;

        if (!roomTypeId || !mealPlanId) {
            alert('Por favor, seleccione tipo de habitación y plan de comidas');
            return;
        }

        // Formateamos las fechas antes de enviarlas
        const formattedStart = formatDate(start);
        const formattedEnd = formatDate(end);

        // Aquí implementaremos la lógica para guardar los precios
        console.log('Guardando precios:', {
            start: formattedStart,
            end: formattedEnd,
            price,
            roomTypeId,
            mealPlanId
        });
    }

    // Inicialización del calendario
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth'
        },
        select: function(info) {
            const price = document.getElementById('defaultPrice').value;
            if (!price) {
                alert('Por favor, establezca un precio');
                return;
            }
            handleDateSelection(info.start, info.end, price);
        },
        events: function(info, successCallback, failureCallback) {
            loadPrices(info.start, info.end, successCallback);
        }
    });

    calendar.render();

    // Event Listeners
    document.getElementById('roomTypeSelect').addEventListener('change', function() {
        console.log('Tipo de habitación cambiado:', this.value);
        calendar.refetchEvents();
    });

    document.getElementById('mealPlanSelect').addEventListener('change', function() {
        console.log('Plan de comidas cambiado:', this.value);
        calendar.refetchEvents();
    });

    document.getElementById('applyPrice').addEventListener('click', function() {
        const price = document.getElementById('defaultPrice').value;
        console.log('Precio a aplicar:', price);
        // Aquí implementaremos la lógica para aplicar el precio
    });
});

function handleDateSelection(start, end, price) {
    const roomTypeId = document.getElementById('roomTypeSelect').value;
    const mealPlanId = document.getElementById('mealPlanSelect').value;

    if (!roomTypeId || !mealPlanId) {
        alert('Por favor, seleccione tipo de habitación y plan de comidas');
        return;
    }

    const formattedStart = formatDate(start);
    const formattedEnd = formatDate(end);

    // Enviar al backend
    fetch('/api/room-prices/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // Función para obtener el token CSRF
        },
        body: JSON.stringify({
            start_date: formattedStart,
            end_date: formattedEnd,
            price: parseFloat(price),
            room_type_id: roomTypeId,
            meal_plan_id: mealPlanId
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => Promise.reject(err));
        }
        return response.json();
    })
    .then(data => {
        // Refrescar el calendario
        calendar.refetchEvents();
        // Mostrar mensaje de éxito
        showSuccessMessage('Precios actualizados correctamente');
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Error al guardar los precios');
    });
}

// Función auxiliar para obtener el token CSRF
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Funciones para mostrar mensajes
function showSuccessMessage(message) {
    // Implementa tu lógica de mostrar mensajes
}

function showErrorMessage(message) {
    // Implementa tu lógica de mostrar mensajes
}
