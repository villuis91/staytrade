from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from staytrade.providers.models import RoomTypeMealPlanPrice, RoomType, MealPlan
from .serializers import (
    RoomTypeMealPlanPriceSerializer,
    RoomTypeMealPlanPriceBulkSerializer,
)


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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_room_prices(request):
    try:
        with transaction.atomic():
            data = request.data

            # Validaciones
            if not all(
                [
                    data.get("start_date"),
                    data.get("end_date"),
                    data.get("price"),
                    data.get("room_type_id"),
                    data.get("meal_plan_id"),
                ]
            ):
                raise ValidationError("Faltan campos requeridos")

            # Validar que el precio sea positivo
            if float(data["price"]) <= 0:
                raise ValidationError("El precio debe ser mayor que 0")

            # Validar que la fecha final sea posterior a la inicial
            if data["end_date"] <= data["start_date"]:
                raise ValidationError("La fecha final debe ser posterior a la inicial")

            # Validar que el tipo de habitación y plan de comidas existan
            room_type = RoomType.objects.get(pk=data["room_type_id"])
            meal_plan = MealPlan.objects.get(pk=data["meal_plan_id"])

            # Crear o actualizar precios
            RoomPrice.objects.create_or_update_prices(
                start_date=data["start_date"],
                end_date=data["end_date"],
                price=data["price"],
                room_type=room_type,
                meal_plan=meal_plan,
            )

            return Response(
                {"message": "Precios actualizados correctamente"},
                status=status.HTTP_200_OK,
            )

    except (RoomType.DoesNotExist, MealPlan.DoesNotExist):
        return Response(
            {"error": "Tipo de habitación o plan de comidas no encontrado"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": "Error al guardar los precios"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
