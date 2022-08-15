from lca.lca import LCAMetrics
from processes.am import LPBF, Part, calc_ampowder_per_kg_part
from processes.powderfab import PowderFab, RawFeedstock, calc_feedstock_per_kg_ampowder

if __name__ == "__main__":

    feedstock_lcametric_test = LCAMetrics(name='material_test', energy=10.0, co2=50.0)
    feedstock_test = RawFeedstock(name='material_test', form='bar', lca_metrics=feedstock_lcametric_test)
    powderfab_lcametric_test = LCAMetrics(name='powderfab_test', energy=20.0, co2=100.0)
    powderfab_test = PowderFab(name='powderfab_test', proc_yield=0.4, lca_metrics=powderfab_lcametric_test)

    feedstock_per_unit_powder, _, _ = calc_feedstock_per_kg_ampowder(powderfab_test)

    lpbf_test = LPBF(machine_name='machine_test', build_env_height=325, build_env_length=250, build_env_width=250,
                     part_yield=0.9, scrap_reuse_frac=0.8, scrap_coprod_frac=0.3)
    part_test = Part(name='part_test', max_height=150, volume=1500000, support_volume=10000)

    powder_per_unit_part, _, _ = calc_ampowder_per_kg_part(amproc=lpbf_test, part=part_test)

    feedstock_per_unit_part = 1 / (powder_per_unit_part * feedstock_per_unit_powder)
