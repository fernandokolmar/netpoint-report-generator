"""
Calculadora de tempo e retenção para relatórios.
"""

from typing import Optional
import pandas as pd
from datetime import datetime


class TimeCalculator:
    """Cálculos relacionados a tempo e retenção."""

    @staticmethod
    def format_minutes_to_time(minutes: float) -> str:
        """
        Converte minutos para formato HH:MM:SS.

        Args:
            minutes: Tempo em minutos

        Returns:
            String no formato "HH:MM:SS"

        Raises:
            ValueError: Se minutos for negativo

        Example:
            >>> TimeCalculator.format_minutes_to_time(125)
            '02:05:00'
            >>> TimeCalculator.format_minutes_to_time(0)
            '0:00:00'
        """
        if pd.isna(minutes):
            return "0:00:00"

        if minutes < 0:
            raise ValueError(f"Tempo não pode ser negativo: {minutes}")

        if minutes == 0:
            return "0:00:00"

        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}:{mins:02d}:00"

    @staticmethod
    def calculate_time_from_dates(
        inicial_str: str,
        final_str: str,
        date_format: str = '%d/%m/%Y %H:%M:%S'
    ) -> str:
        """
        Calcula diferença de tempo entre duas datas.

        Args:
            inicial_str: Data inicial como string
            final_str: Data final como string
            date_format: Formato das datas

        Returns:
            String no formato "HH:MM:SS"

        Raises:
            ValueError: Se data final for anterior à inicial

        Example:
            >>> TimeCalculator.calculate_time_from_dates(
            ...     '29/01/2025 14:00:00',
            ...     '29/01/2025 15:30:45'
            ... )
            '1:30:45'
        """
        try:
            inicial = pd.to_datetime(inicial_str, format=date_format, dayfirst=True)
            final = pd.to_datetime(final_str, format=date_format, dayfirst=True)

            if final < inicial:
                raise ValueError(
                    f"Data final ({final_str}) não pode ser anterior à inicial ({inicial_str})"
                )

            diff = final - inicial
            total_seconds = int(diff.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            return f"{hours}:{minutes:02d}:{seconds:02d}"

        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError(
                    f"Formato de data inválido. Esperado: {date_format}\n"
                    f"Recebido: {inicial_str} e {final_str}"
                )
            raise

    @staticmethod
    def convert_time_to_minutes(time_str: str) -> float:
        """
        Converte string HH:MM:SS para minutos (numérico).

        Args:
            time_str: String no formato "HH:MM:SS"

        Returns:
            Tempo em minutos (float)

        Example:
            >>> TimeCalculator.convert_time_to_minutes("02:05:30")
            125.5
            >>> TimeCalculator.convert_time_to_minutes("0:00:00")
            0.0
        """
        if pd.isna(time_str) or time_str == "0:00:00":
            return 0.0

        try:
            parts = str(time_str).split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2]) if len(parts) > 2 else 0

            total_minutes = hours * 60 + minutes + seconds / 60
            return round(total_minutes, 2)

        except (ValueError, IndexError) as e:
            raise ValueError(f"Formato de tempo inválido: {time_str}. Esperado HH:MM:SS")
