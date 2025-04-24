# views/api.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from staytrade.providers.models import RoomTypeMealPlanPrice


class RoomPriceViewSet(viewsets.ViewSet):
    """
    ViewSet para gestionar los precios de las habitaciones
    """

    def list(self, request):
        """
        Endpoint GET /api/room-prices/
        Retorna los precios según los filtros proporcionados
        """
        room_type_id = request.query_params.get("room_type_id")
        meal_plan_id = request.query_params.get("meal_plan_id")
        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")

        # Aquí tu lógica para obtener los precios
        # Por ahora retornamos datos de ejemplo
        return Response(
            [
                {
                    "id": 1,
                    "start": start_date,
                    "end": end_date,
                    "extendedProps": {"price": 100},
                }
            ]
        )

    def create(self, request):
        """
        Endpoint POST /api/room-prices/
        Guarda un nuevo precio
        """
        # Aquí tu lógica para guardar precio
        data = request.data
        RoomTypeMealPlanPrice.objects.create_or_update_prices(**data)
        return Response({"message": "Precio guardado"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def calendar_data(self, request):
        """
        Endpoint GET /api/room-prices/calendar_data/
        Retorna los datos formateados para el calendario
        """
        room_type_id = request.query_params.get("room_type_id")
        meal_plan_id = request.query_params.get("meal_plan_id")
        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")

        # Por ahora retornamos datos de ejemplo
        return Response(
            [
                {
                    "id": 1,
                    "start": start_date,
                    "end": end_date,
                    "extendedProps": {"price": 100},
                }
            ]
        )
