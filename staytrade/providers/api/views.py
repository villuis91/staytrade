from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from staytrade.providers.models import RoomTypeMealPlanPrice
from .serializers import CalendarEventSerializer, RoomTypeMealPlanPriceBulkSerializer


class RoomPriceViewSet(viewsets.ViewSet):
    """
    ViewSet para gestionar los precios de las habitaciones
    """

    def create(self, request):
        """
        Endpoint POST /api/room-prices/
        Guarda un nuevo precio
        """
        serializer = RoomTypeMealPlanPriceBulkSerializer(data=request.data)
        if serializer.is_valid():
            RoomTypeMealPlanPrice.objects.create_or_update_prices(
                **serializer.validated_data
            )
            return Response(
                {"message": "Precio guardado"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        if not all([room_type_id, meal_plan_id, start_date, end_date]):
            return Response([])

        prices = RoomTypeMealPlanPrice.objects.filter(
            room_type_id=room_type_id,
            meal_plan_id=meal_plan_id,
            start_date__gte=start_date,
            end_date__lte=end_date,
        )

        serializer = CalendarEventSerializer(prices, many=True)
        return Response(serializer.data)
