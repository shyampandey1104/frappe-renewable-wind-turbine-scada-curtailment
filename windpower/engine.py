"""Renewable Wind Turbine SCADA Telemetry, SLDC Curtailment & Power Curve Engine."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class WindTurbineTelemetry:
    turbine_id: str
    wind_speed_ms: float
    nacelle_yaw_degrees: float
    rotor_rpm: float
    active_power_kw: float
    is_curtailed_by_grid: bool = False
    curtailment_cap_kw: Optional[float] = None


@dataclass
class CurtailmentLossReport:
    turbine_id: str
    wind_speed_ms: float
    theoretical_power_kw: float
    actual_dispatched_power_kw: float
    curtailed_energy_loss_kwh: float
    financial_revenue_loss_inr: float
    ppa_tariff_rate_inr_per_kwh: float


class WindEnergyScadaEngine:
    """Models aerodynamic wind turbine power curves and computes grid curtailment revenue loss."""

    # Typical 2.1 MW Suzlon / Vestas power curve
    CUT_IN_WIND_SPEED_MS = 3.0
    RATED_WIND_SPEED_MS = 11.5
    CUT_OUT_WIND_SPEED_MS = 25.0
    RATED_CAPACITY_KW = 2100.0

    def estimate_theoretical_power(self, wind_speed_ms: float) -> float:
        if wind_speed_ms < self.CUT_IN_WIND_SPEED_MS or wind_speed_ms >= self.CUT_OUT_WIND_SPEED_MS:
            return 0.0
        if wind_speed_ms >= self.RATED_WIND_SPEED_MS:
            return self.RATED_CAPACITY_KW
        # Cubic curve segment between cut-in and rated
        ratio = (wind_speed_ms - self.CUT_IN_WIND_SPEED_MS) / (self.RATED_WIND_SPEED_MS - self.CUT_IN_WIND_SPEED_MS)
        return round(self.RATED_CAPACITY_KW * (ratio ** 3), 2)

    def calculate_curtailment_loss(
        self,
        telemetry: WindTurbineTelemetry,
        duration_hours: float = 1.0,
        ppa_tariff_inr: float = 3.15
    ) -> CurtailmentLossReport:
        theoretical_kw = self.estimate_theoretical_power(telemetry.wind_speed_ms)

        if telemetry.is_curtailed_by_grid and telemetry.curtailment_cap_kw is not None:
            dispatched_kw = min(theoretical_kw, telemetry.curtailment_cap_kw)
        else:
            dispatched_kw = theoretical_kw

        loss_kw = max(0.0, theoretical_kw - dispatched_kw)
        loss_kwh = round(loss_kw * duration_hours, 2)
        revenue_loss = round(loss_kwh * ppa_tariff_inr, 2)

        return CurtailmentLossReport(
            turbine_id=telemetry.turbine_id,
            wind_speed_ms=telemetry.wind_speed_ms,
            theoretical_power_kw=theoretical_kw,
            actual_dispatched_power_kw=dispatched_kw,
            curtailed_energy_loss_kwh=loss_kwh,
            financial_revenue_loss_inr=revenue_loss,
            ppa_tariff_rate_inr_per_kwh=ppa_tariff_inr
        )
