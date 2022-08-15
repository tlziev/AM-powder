class LCAMetrics:
    """
    LCA metrics used in LCA analysis for a material, process step, etc.
    """

    def __init__(self, name, energy, co2, energy_unit="MJ/kg", co2_unit="kg_CO2/kg"):
        """
        Initializes an instance of LCAMetrics class.

        Parameters
        ----------
        name: str
            Name of the material, process step, etc. associated with instance of LCAMetrics.
        energy: int or float
            Energy consumption per unit for material, process step, etc.
        co2: int or float
            CO2 emissions per unit for material, process step, etc.
        energy_unit: str
            Units for energy LCA metric.
        co2_unit: str
            Units for CO2 metric.
        """

        self.name = name
        self.energy = energy
        self.co2 = co2
        self.energy_unit = energy_unit
        self.co2_unit = co2_unit
