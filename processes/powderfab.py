from lca.lca import LCAMetrics


class RawFeedstock:
    """
    Raw material input to powder production process.
    """

    def __init__(self, name, form, lca_metrics):
        """
        Initializes an instance of RawFeedstock class.

        Parameters
        ----------
        name: str
            Name of raw feedstock material.
        form: str
            Form factor of feedstock material, e.g. ore, bar, sheet, etc..
        lca_metrics: LCAMetrics
            Instance of LCAMetrics containing LCA metric data associated with raw feedstock material.
        """
        self.name = name
        self.form = form
        self.lca_metrics = lca_metrics


class PowderFab:
    """
    Powder fabrication process that converts raw feedstock material to additive manufacturing (AM) powder.
    """

    def __init__(self, name, proc_yield, lca_metrics: LCAMetrics, scrap_reuse_frac=0.0, scrap_coprod_frac=0.0):
        """
        Initializes an instance of PowderFab class.

        Parameters
        ----------
        name: str
            Name of powder fabrication process.
        proc_yield: float
            Yield fraction of AM quality powder from fabrication process (value between 0 and 1).
        lca_metrics: LCAMetrics
            Instance of LCAMetrics containing LCA metric data associated with raw feedstock material.
        scrap_reuse_frac: float
            Fraction of scrap powder that can be recycled as feedstock for fabrication process (value between 0 and 1).
        scrap_coprod_frac: float
            Fraction of non-recyclable scrap powder that can be used in a non-AM production process, i.e. a coproduct
            (value between 0 and 1).
        """
        self.name = name
        self.proc_yield = proc_yield
        self.lca_metrics = lca_metrics
        self.scrap_reuse_frac = scrap_reuse_frac
        self.scrap_coprod_frac = scrap_coprod_frac


def calc_feedstock_per_kg_ampowder(powderfab: PowderFab, recycle_times='inf'):
    """
        Calculates the kg of feedstock material required to produce 1 kg AM quality powder via a specified powder
        fabrication process.


        Parameters
        ----------
        powderfab: PowderFab
            Instance of the PowderFab class that specifies the powder fabrication process to be used to produce AM
            powder.
        recycle_times: str or int
            Number of times scrap from the powder fabrication process of virgin feedstock can be recycled as powder
            feedstock. Options include 0 for no recycling, int for a specific number of allowed recycles, or str 'inf'
            for infinite recycling.

        Returns
        -------
        feedstock_per_kg_ampowder: float
            Kg of virgin feedstock material required to produce 1 kg of AM powder.
        kg_coproduct: float
            Kg of coproduct powder produced during production of 1 kg of AM powder.
        kg_waste: float
            Kg of waste powder produced during production of 1 kg of AM powder.

        """

    # create variables to use internally in function
    powder_2_am = powderfab.proc_yield
    powder_2_scrap = 1 - powder_2_am
    powder_2_reuse = powderfab.scrap_reuse_frac
    powder_2_other = 1 - powder_2_reuse
    powder_2_other_proc = powderfab.scrap_coprod_frac
    powder_2_waste = 1 - powder_2_other_proc

    if recycle_times == 'inf':
        # in case of infinite recycling, use inf geometric series sum to account for recycled powder scrap
        # offsetting need for virgin feedstock.
        feedstock_per_kg_ampowder = 1 / (powder_2_am + powder_2_scrap / (1 - powder_2_reuse))
    elif recycle_times == 0:
        # case of no recycling
        feedstock_per_kg_ampowder = 1 / powder_2_am
    else:
        # in case of fixed number of reuses for recycled powder scrap, use sum of geometric series for n terms
        feedstock_per_kg_ampowder = 1 / (powder_2_am + powder_2_scrap * (1 - powder_2_reuse ** recycle_times)
                                         / (1 - powder_2_reuse))

    # calculate kg of coproduct and waste generated in production of 1 kg AM powder
    kg_coproduct = (feedstock_per_kg_ampowder - 1) * powder_2_other_proc
    kg_waste = (feedstock_per_kg_ampowder - 1) * powder_2_waste

    return feedstock_per_kg_ampowder, kg_coproduct, kg_waste
