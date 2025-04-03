from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    RoomTypeMealPlanPriceSerializer,
    RoomTypeMealPlanPriceBulkSerializer,
)
from staytrade.providers.models import RoomTypeMealPlanPrice


class RoomTypeMealPlanPriceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeMealPlanPriceSerializer

    def get_queryset(self):
        room_type_id = self.request.query_params.get("room_type_id")
        meal_plan_id = self.request.query_params.get("meal_plan_id")
        start_date = self.request.query_params.get("start")
        end_date = self.request.query_params.get("end")

        queryset = RoomTypeMealPlanPrice.objects.all()

        if room_type_id and meal_plan_id:
            queryset = queryset.filter(
                room_type_id=room_type_id,
                meal_plan_id=meal_plan_id,
                date__range=[start_date, end_date],
            )

        return queryset

    @action(detail=False, methods=["post"])
    def bulk_update(self, request):
        # Para actualizar múltiples fechas a la vez
        serializer = RoomTypeMealPlanPriceBulkSerializer(data=request.data)
        if serializer.is_valid():
            # Lógica de actualización masiva
            return Response({"status": "success"})
        return Response(serializer.errors, status=400)
