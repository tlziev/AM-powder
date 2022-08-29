from numpy import allclose

from processes.am import LPBF, Part, calc_ampowder_per_kg_part


def test_calc_feedstock_per_kg_ampowder_part100_yield100_other0():
    lpbf_test = LPBF(machine_name='machine_test', build_env_height=10, build_env_length=10, build_env_width=10,
                     part_yield=1.0, scrap_reuse_frac=0.0, scrap_coprod_frac=0.0)
    part_test = Part(name='part_test', max_height=10, volume=1000, support_volume=0)

    powder_per_unit_part, kg_coproduct, kg_waste = calc_ampowder_per_kg_part(amproc=lpbf_test, part=part_test)

    assert powder_per_unit_part == 1
    assert kg_coproduct == 0
    assert kg_waste == 0

def test_calc_feedstock_per_kg_ampowder_part40_yield100_other0():
    lpbf_test = LPBF(machine_name='machine_test', build_env_height=10, build_env_length=10, build_env_width=10,
                     part_yield=1.0, scrap_reuse_frac=0.0, scrap_coprod_frac=0.0)
    part_test = Part(name='part_test', max_height=10, volume=400, support_volume=0)

    powder_per_unit_part, kg_coproduct, kg_waste = calc_ampowder_per_kg_part(amproc=lpbf_test, part=part_test)

    assert allclose(powder_per_unit_part, (1.0 / 0.4))
    assert allclose(kg_coproduct, 0)
    assert allclose(kg_waste, (0.6 / 0.4))

def test_calc_feedstock_per_kg_ampowder_part40_support_10_yield100_other0():
    lpbf_test = LPBF(machine_name='machine_test', build_env_height=10, build_env_length=10, build_env_width=10,
                     part_yield=1.0, scrap_reuse_frac=0.0, scrap_coprod_frac=0.0)
    part_test = Part(name='part_test', max_height=10, volume=400, support_volume=100)

    powder_per_unit_part, kg_coproduct, kg_waste = calc_ampowder_per_kg_part(amproc=lpbf_test, part=part_test)

    assert allclose(powder_per_unit_part, (1.0 / 0.4))
    assert allclose(kg_coproduct, 0)
    assert allclose(kg_waste, (0.6 / 0.4))

def test_calc_feedstock_per_kg_ampowder_part40_support_10_reuse80_coprod0_yield100():
    lpbf_test = LPBF(machine_name='machine_test', build_env_height=10, build_env_length=10, build_env_width=10,
                     part_yield=1.0, scrap_reuse_frac=0.8, scrap_coprod_frac=0.0)
    part_test = Part(name='part_test', max_height=10, volume=400, support_volume=100)

    powder_per_unit_part, kg_coproduct, kg_waste = calc_ampowder_per_kg_part(amproc=lpbf_test, part=part_test)

    assert allclose(powder_per_unit_part, (1.0 / 2.4))
    assert allclose(kg_coproduct, 0)
    assert allclose(kg_waste, (-1.4 / 2.4))

def test_calc_feedstock_per_kg_ampowder_part40_support_0_reuse80_coprod0_yield100():
    lpbf_test = LPBF(machine_name='machine_test', build_env_height=10, build_env_length=10, build_env_width=10,
                     part_yield=1.0, scrap_reuse_frac=0.8, scrap_coprod_frac=0.0)
    part_test = Part(name='part_test', max_height=10, volume=400, support_volume=0)

    powder_per_unit_part, kg_coproduct, kg_waste = calc_ampowder_per_kg_part(amproc=lpbf_test, part=part_test)

    assert allclose(powder_per_unit_part, (1.0 / 2.8))
    assert allclose(kg_coproduct, 0)
    assert allclose(kg_waste, (-1.8 / 2.8))

def test_calc_feedstock_per_kg_ampowder_part40_support_0_reuse80_coprod30_yield100():
    lpbf_test = LPBF(machine_name='machine_test', build_env_height=10, build_env_length=10, build_env_width=10,
                     part_yield=1.0, scrap_reuse_frac=0.8, scrap_coprod_frac=0.3)
    part_test = Part(name='part_test', max_height=10, volume=400, support_volume=0)

    powder_per_unit_part, kg_coproduct, kg_waste = calc_ampowder_per_kg_part(amproc=lpbf_test, part=part_test)

    assert allclose(powder_per_unit_part, (1.0 / 2.8))
    assert allclose(kg_coproduct, (-0.54 / 2.8))
    assert allclose(kg_waste, (-1.26 / 2.8))
