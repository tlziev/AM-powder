if __name__ == "__main__":
    powder_2_AM = 0.25
    powder_2_scrap = 1 - powder_2_AM

    powder_2_reuse = 0.8
    powder_2_other = 1 - powder_2_reuse

    powder_2_other_proc = 0.3
    powder_2_waste = 1 - powder_2_other_proc

    AM_2_part = 0.55
    AM_2_scrap = 1 - AM_2_part

    AM_2_reuse = 0.1
    AM_2_other = 1 - AM_2_reuse

    AM_2_other_proc = 0.4
    AM_2_waste = 1 - AM_2_other_proc

    feedstock_per_unit_powder = 1 / (powder_2_AM * (1 + powder_2_scrap * powder_2_reuse))

    powder_per_unit_part = 1 / (AM_2_part * (1 + AM_2_scrap * AM_2_reuse))

    feedstock_per_unit_part = 1 / (powder_per_unit_part * feedstock_per_unit_powder)
