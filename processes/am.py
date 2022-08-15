class LPBF:
    """
    Laser powder bed fusion (LPBF) process that converts AM powder to a printed part.
    """

    def __init__(self, machine_name, build_env_height, build_env_length, build_env_width, part_yield=1.0,
                 scrap_reuse_frac=0.0, scrap_coprod_frac=0.0):
        """
        Initializes and instance of LPBF class.

        Parameters
        ----------
        machine_name: str
            Name of LPBF machine to be used.
        build_env_height: int or float
            Height (mm) of machine build envelope.
        build_env_length: int or float
            Length (mm) of machine build envelope.
        build_env_width: int or float
            Width (mm) of machine build envelope.
        part_yield: float
            Yield fraction of parts meeting specifications from AM process (value between 0 and 1).
        scrap_reuse_frac: float
            Fraction of scrap powder that can be recycled as feedstock for AM process (value between 0 and 1).
        scrap_coprod_frac: float
            Fraction of non-recyclable scrap powder that can be used in a non-AM production process, i.e. a coproduct
            (value between 0 and 1).
        """

        self.machine_name = machine_name
        self.build_env_height = build_env_height
        self.build_env_length = build_env_length
        self.build_env_width = build_env_width
        self.part_yield = part_yield
        self.scrap_reuse_frac = scrap_reuse_frac
        self.scrap_coprod_frac = scrap_coprod_frac


class Part:
    """
    Part to be fabricated via AM.
    """

    def __init__(self, name, max_height, mass=None, volume=None, support_mass=None, support_volume=None):
        """
        Initializes an instance of Part class.

        Parameters
        ----------
        name:str
            Part name.
        max_height: int or float
            Maximum height (mm) of part (dimension perpendicular to build plate).
        mass: int or float
            Total mass (kg) of part.
        volume: int or float
            Total volume (mm^3) of part.
        support_mass: int or float
            Total mass (kg) of printed supports.
        support_volume: int or float
            Total volume (mm^3) of printed supports.
        """
        self.name = name
        self.max_height = max_height
        self.mass = mass
        self.volume = volume
        self.support_mass = support_mass
        self.support_volume = support_volume


class AMpowder:
    """AM powder produced via a specified powder fabrication process"""

    def __init__(self, name):
        self.name = name


def calc_ampowder_per_kg_part(amproc: LPBF, part: Part, recycle_times='inf'):
    """
        Calculates the kg of AM powder required to produce 1 kg AM part via LPBF process.

        Parameters
        ----------
        amproc: LPBF
            Instance of the LPBF class that specifies the LPBF process to be used to produce the AM part.
        part: Part
            Instance of the Part class that specifies the AM part to be produced.
        recycle_times: str or int
            Number of times scrap from the powder fabrication process of virgin feedstock can be recycled as powder
            feedstock. Options include 0 for no recycling, int for a specific number of allowed recycles, or str 'inf'
            for infinite recycling.

        Returns
        -------
        ampowder_per_kg_part: float
            Kg of virgin AM powder required to produce 1 kg of AM part.
        kg_coproduct: float
            Kg of coproduct AM powder produced during production of 1 kg of AM part.
        kg_waste: float
            Kg of waste AM powder produced during production of 1 kg of AM part.

        Notes
        -----
        This method assumes printing a single part per build.

        """
    # create variables to use internally in function

    # calculate powder fill for part build
    powder_volume = amproc.build_env_length * amproc.build_env_width * part.max_height

    # calculate portion of powder that is consolidated into part & portion that is scrap
    am_2_part = part.volume / powder_volume
    am_2_scrap = 1 - am_2_part

    # calculate portion of scrap that is consolidated into supports & portion that is powder scrap
    am_2_scrap_volume = am_2_scrap * powder_volume
    am_2_melted_scrap_waste = part.support_volume / am_2_scrap_volume
    am_2_powder_scrap = 1 - am_2_melted_scrap_waste

    am_2_reuse = amproc.scrap_reuse_frac
    am_2_other = 1 - am_2_reuse
    am_2_other_proc = amproc.scrap_coprod_frac
    am_2_waste = 1 - am_2_other_proc

    # calculate AM powder per kg part for 100% part yield
    if recycle_times == 'inf':
        # in case of infinite recycling, use inf geometric series sum to account for recycled powder scrap
        # offsetting need for virgin AM powder.
        ampowder_per_kg_part = (1 / (am_2_part + (am_2_scrap * am_2_powder_scrap) / (1 - am_2_reuse)))
    elif recycle_times == 0:
        # case of no recycling
        ampowder_per_kg_part = (1 / am_2_part)
    else:
        # in case of fixed number of reuses for recycled powder scrap, use sum of geometric series for n terms
        ampowder_per_kg_part = (1 / (am_2_part + (am_2_scrap * am_2_powder_scrap) * (1 - am_2_reuse ** recycle_times)
                                     / (1 - am_2_reuse)))

    # calculate kg of coproduct and waste generated in production of 1 kg AM powder for 100% part yield
    kg_coproduct = (ampowder_per_kg_part - 1) * am_2_other_proc
    kg_waste = ((ampowder_per_kg_part - 1) * (am_2_waste + am_2_melted_scrap_waste))

    # Adjust coproduct and waste quantities
    effective_units = 1 / amproc.part_yield
    kg_coproduct = kg_coproduct * (1 + effective_units)
    kg_waste = kg_waste * (1 + effective_units) + ampowder_per_kg_part * (effective_units - 1)

    return ampowder_per_kg_part, kg_waste, kg_coproduct
