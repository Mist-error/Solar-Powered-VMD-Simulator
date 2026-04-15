"""
Solar Input Model

Generates time-dependent solar irradiance including day/night cycles and cloud effects.
"""

import numpy as np
from typing import Callable


class SolarInput:
    """
    Generates time-dependent solar irradiance.
    Simulates day/night cycles and optional cloud fluctuations.
    """
    
    def __init__(
        self,
        solar_intensity: float = 800.0,  # W/m²
        enable_clouds: bool = False,
        cloud_frequency: float = 0.01  # Cloud event frequency (per second)
    ):
        """
        Initialize solar input model.
        
        Args:
            solar_intensity: Peak solar intensity (W/m²)
            enable_clouds: Enable cloud fluctuations
            cloud_frequency: Frequency of cloud events (0-1)
        """
        self.solar_intensity_peak = solar_intensity
        self.enable_clouds = enable_clouds
        self.cloud_frequency = cloud_frequency
        
    def solar_irradiance_daily(self, t: float, day_start: float = 6.0, day_end: float = 18.0) -> float:
        """
        Compute solar irradiance with day/night cycle.
        
        Uses a cosine function to simulate sunrise/sunset.
        
        Args:
            t: Time of day (hours, 0-24)
            day_start: Sunrise time (hours)
            day_end: Sunset time (hours)
            
        Returns:
            Solar irradiance (W/m²)
        """
        t_hour = t % 24  # 24-hour cycle
        
        # Outside daylight hours, irradiance is 0
        if t_hour < day_start or t_hour > day_end:
            return 0.0
        
        # Cosine profile during daylight
        progress = (t_hour - day_start) / (day_end - day_start)
        irradiance = self.solar_intensity_peak * np.cos((1 - 2 * progress) * np.pi / 2) ** 2
        
        return max(0.0, irradiance)
    
    def apply_cloud_effects(self, irradiance: float, t: float, seed: int = None) -> float:
        """
        Apply random cloud fluctuations to irradiance.
        
        Args:
            irradiance: Base solar irradiance (W/m²)
            t: Current time (used for random seed)
            seed: Random seed for reproducibility
            
        Returns:
            Irradiance with cloud effects (W/m²)
        """
        if not self.enable_clouds or irradiance == 0:
            return irradiance
        
        # Use time-based seed for reproducibility within a run
        if seed is None:
            seed = int(t * 1000) % (2**31 - 1)
        
        np.random.seed(seed)
        
        # Random drop in intensity due to clouds
        cloud_factor = np.random.normal(1.0, 0.1)  # Mean 1.0, std 0.1
        cloud_factor = np.clip(cloud_factor, 0.3, 1.0)  # Limit to 30-100% transmission
        
        return irradiance * cloud_factor
    
    def get_irradiance(
        self,
        t: float,
        apply_clouds: bool = None,
        day_start: float = 6.0,
        day_end: float = 18.0
    ) -> float:
        """
        Get solar irradiance at time t.
        
        Args:
            t: Time in hours (can be > 24 for multiple days)
            apply_clouds: Override enable_clouds setting
            day_start: Sunrise time (hours)
            day_end: Sunset time (hours)
            
        Returns:
            Solar irradiance (W/m²)
        """
        irradiance = self.solar_irradiance_daily(t, day_start, day_end)
        
        use_clouds = apply_clouds if apply_clouds is not None else self.enable_clouds
        if use_clouds:
            irradiance = self.apply_cloud_effects(irradiance, t)
        
        return max(0.0, irradiance)
