if __name__ == "__main__":

    class LCAMetrics:

        def __init__(self, name, energy_use, co2):
            self.name = name
            self.energy_use = energy_use
            self.CO2 = co2


    class RawFeedstock:

        def __init__(self, name, form, lca_metric):
            self.name = name
            self.form = form
            self.lca_metric = lca_metric


