from numpy import allclose
from lca.lca import LCAMetrics
from processes.powderfab import PowderFab, calc_feedstock_per_kg_ampowder


def test_calc_feedstock_per_kg_ampowder_yield100():
    powderfab_lcametric_test = LCAMetrics(name='powderfab_test', energy=20.0, co2=100.0)
    powderfab_test = PowderFab(name='powderfab_test', proc_yield=1.0, lca_metrics=powderfab_lcametric_test)

    feedstock_per_kg_ampowder, kg_coproduct, kg_waste = calc_feedstock_per_kg_ampowder(powderfab_test)

    assert feedstock_per_kg_ampowder == 1
    assert kg_coproduct == 0
    assert kg_waste == 0


def test_calc_feedstock_per_kg_ampowder_yield60_reuse0_coprod0():
    powderfab_lcametric_test = LCAMetrics(name='powderfab_test', energy=20.0, co2=100.0)
    powderfab_test = PowderFab(name='powderfab_test', proc_yield=0.6, lca_metrics=powderfab_lcametric_test)

    feedstock_per_kg_ampowder, kg_coproduct, kg_waste = calc_feedstock_per_kg_ampowder(powderfab_test)

    assert feedstock_per_kg_ampowder == (1 / 0.6)
    assert kg_coproduct == 0
    assert kg_waste == (1 / 0.6 - 1)


def test_calc_feedstock_per_kg_ampowder_yield60_reuse30_coprod0():
    powderfab_lcametric_test = LCAMetrics(name='powderfab_test', energy=20.0, co2=100.0)
    powderfab_test = PowderFab(name='powderfab_test', proc_yield=0.6, lca_metrics=powderfab_lcametric_test,
                               scrap_reuse_frac=0.3)

    feedstock_per_kg_ampowder, kg_coproduct, kg_waste = calc_feedstock_per_kg_ampowder(powderfab_test)

    assert allclose(feedstock_per_kg_ampowder, (0.7 / 0.54))
    assert allclose(kg_coproduct, 0)
    assert allclose(kg_waste, (0.7 / 0.54 - 1))


def test_calc_feedstock_per_kg_ampowder_yield60_reuse30_coprod10():
    powderfab_lcametric_test = LCAMetrics(name='powderfab_test', energy=20.0, co2=100.0)
    powderfab_test = PowderFab(name='powderfab_test', proc_yield=0.6, lca_metrics=powderfab_lcametric_test,
                               scrap_reuse_frac=0.3, scrap_coprod_frac=0.1)

    feedstock_per_kg_ampowder, kg_coproduct, kg_waste = calc_feedstock_per_kg_ampowder(powderfab_test)

    assert allclose(feedstock_per_kg_ampowder, (0.7 / 0.54))
    assert allclose(kg_coproduct, (0.016 / 0.54))
    assert allclose(kg_waste, (0.144 / 0.54))

