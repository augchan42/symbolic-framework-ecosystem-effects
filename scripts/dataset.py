"""Canonical N=41 dataset manifest.

Single source of truth for which games belong to the clean dataset
used in the paper. All extraction scripts should import from here.
"""

CLEAN_DATASET = {
    "control": [
        "control_opus_20260329_124001_df65",
        "control_opus_20260329_165843_aee4",
        "control_opus_20260403_125741_8c67",
        "control_opus_20260403_125743_cf36",
        "control_opus_20260404_101008_523c",
        "control_opus_20260404_101008_8291",
        "control_opus_20260329_074444_c154",
        "control_opus_20260507_233507_c007",
        "control_opus_20260508_090009_7177",
        "control_opus_20260510_184414_c19f",
        "control_opus_20260511_001142_57fe",
    ],
    "yarrow": [
        "random_oracle_opus_20260329_124241_7b69",
        "random_oracle_opus_20260329_165843_fdb1",
        "random_oracle_opus_20260403_125734_f6d2",
        "random_oracle_opus_20260403_125737_c9b7",
        "random_oracle_opus_20260404_101008_0154",
        "random_oracle_opus_20260404_101008_ea16",
        "random_oracle_opus_20260427_182540_65a1",
        "random_oracle_opus_20260503_174137_3c96",
        "random_oracle_opus_20260504_113552_3506",
        "random_oracle_opus_20260504_202055_1bd9",
    ],
    "tarot": [
        "tarot_opus_20260410_143545_2eba",
        "tarot_opus_20260410_195001_0fa6",
        "tarot_opus_20260411_113544_eacb",
        "tarot_opus_20260411_174138_b51a",
        "tarot_opus_20260416_070448_ceea",
        "tarot_opus_20260416_084349_35a7",
        "tarot_opus_20260417_064826_fbb9",
        "tarot_opus_20260417_064827_e0ff",
        "tarot_opus_20260417_064828_54d8",
        "tarot_opus_20260417_064828_ffa6",
    ],
    "scrambled": [
        "scrambled_text_opus_20260423_234641_7c92",
        "scrambled_text_opus_20260424_115648_1bfd",
        "scrambled_text_opus_20260424_232606_d1ae",
        "scrambled_text_opus_20260425_095615_296c",
        "scrambled_text_opus_20260425_234105_6338",
        "scrambled_text_opus_20260426_071651_9c0b",
        "scrambled_text_opus_20260426_141428_207d",
        "scrambled_text_opus_20260426_221514_422f",
        "scrambled_text_opus_20260427_064006_cb32",
        "scrambled_text_opus_20260427_100040_de3f",
    ],
}
