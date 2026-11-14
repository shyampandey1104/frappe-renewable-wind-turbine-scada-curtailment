import unittest
from windpower.engine import WindEnergyScadaEngine, WindTurbineTelemetry

class TestWindEnergyScada(unittest.TestCase):
    def test_power_curve_and_curtailment_loss(self):
        engine = WindEnergyScadaEngine()

        # At 12 m/s (above rated 11.5 m/s) -> Rated 2100 kW
        self.assertEqual(engine.estimate_theoretical_power(12.0), 2100.0)
        # At 2 m/s (below cut-in 3.0 m/s) -> 0 kW
        self.assertEqual(engine.estimate_theoretical_power(2.0), 0.0)

        # Telemetry under SLDC Grid Curtailment cap of 1200 kW
        telem = WindTurbineTelemetry(
            turbine_id="WTG-JAISALMER-09",
            wind_speed_ms=13.0,
            nacelle_yaw_degrees=240.0,
            rotor_rpm=14.5,
            active_power_kw=1200.0,
            is_curtailed_by_grid=True,
            curtailment_cap_kw=1200.0
        )

        loss = engine.calculate_curtailment_loss(
            telemetry=telem,
            duration_hours=2.0, # 2 hours of curtailment
            ppa_tariff_inr=3.20
        )

        self.assertEqual(loss.theoretical_power_kw, 2100.0)
        self.assertEqual(loss.actual_dispatched_power_kw, 1200.0)
        # Loss kW = 900 kW -> For 2 hours = 1800 kWh
        self.assertEqual(loss.curtailed_energy_loss_kwh, 1800.0)
        # Revenue loss = 1800 * 3.20 = 5760.0
        self.assertEqual(loss.financial_revenue_loss_inr, 5760.0)

if __name__ == "__main__":
    unittest.main()
