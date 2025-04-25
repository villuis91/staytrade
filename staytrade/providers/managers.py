from django.db.models import Manager
from datetime import datetime, timedelta
from decimal import Decimal


class RoomPriceManager(Manager):
    def _generate_date_range(self, start_date, end_date):
        """
        Helper para generar tuplas de fechas consecutivas (start_date, end_date)

        Returns:
            List[Tuple[date, date]]: Lista de tuplas con fechas consecutivas
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        date_pairs = []
        current_date = start_date

        while current_date < end_date:
            next_date = current_date + timedelta(days=1)
            date_pairs.append((current_date, next_date))
            current_date = next_date

        return date_pairs

    def create_or_update_prices(
        self, room_type_id, meal_plan_id, start_date, end_date, price
    ):
        """
        Crea o actualiza precios para cada par de días consecutivos en el rango
        """
        if isinstance(price, str):
            price = Decimal(price)

        date_ranges = self._generate_date_range(start_date, end_date)

        # Obtenemos los rangos existentes primero
        existing_query = self.filter(
            room_type_id=room_type_id,
            meal_plan_id=meal_plan_id,
            start_date__range=(start_date, end_date),
        )

        # Actualizamos los precios existentes
        existing_query.update(price=price)

        # Obtenemos los rangos que ya existen (usando la misma query)
        existing_ranges = set(existing_query.values_list("start_date", "end_date"))

        # Creamos solo los rangos que no existen
        bulk_create_data = [
            self.model(
                room_type_id=room_type_id,
                meal_plan_id=meal_plan_id,
                start_date=range_start,
                end_date=range_end,
                price=price,
            )
            for range_start, range_end in date_ranges
            if (range_start, range_end) not in existing_ranges
        ]

        if bulk_create_data:
            self.bulk_create(bulk_create_data)

        return True
