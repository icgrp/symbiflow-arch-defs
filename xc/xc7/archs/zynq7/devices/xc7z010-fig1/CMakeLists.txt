add_xc_device_define_type(
  ARCH zynq7
  DEVICE xc7z010-fig1
  ROI_DIR ${symbiflow-arch-defs_SOURCE_DIR}/xc/xc7/archs/zynq7/devices/xc7z010-fig1-roi-virt
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
