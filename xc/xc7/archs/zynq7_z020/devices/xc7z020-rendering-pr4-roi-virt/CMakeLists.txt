add_xc_device_define_type(
  ARCH zynq7_z020
  DEVICE xc7z020-rendering-pr4
  ROI_DIR ${symbiflow-arch-defs_SOURCE_DIR}/xc/xc7/archs/zynq7_z020/devices/xc7z020-rendering-pr4-roi-virt
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