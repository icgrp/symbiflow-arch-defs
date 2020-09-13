add_xc_device_define_type(
  ARCH artix7_200t
  DEVICE xc7a200t-fig1
  ROI_DIR ${symbiflow-arch-defs_SOURCE_DIR}/xc/xc7/archs/artix7_200t/devices/xc7a200t-fig1-roi-virt
  TILE_TYPES
    CLBLL_L
    CLBLL_R
    CLBLM_L
    CLBLM_R
    BRAM_L
    BRAM_R
  PB_TYPES
    SLICEL
    SLICEM
    BRAM_L
    BRAM_R
)

