get_target_property_required(OPENOCD env OPENOCD)

add_xc_board(
  BOARD basys3
  DEVICE xc7a50t-basys3
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcpg236-1
)

add_xc_board(
  BOARD basys3-full
  DEVICE xc7a50t
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcpg236-1
)

add_xc_board(
  BOARD basys3-bottom
  DEVICE xc7a50t-bottom
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcpg236-1
)

add_xc_board(
  BOARD arty-swbut
  DEVICE xc7a50t-arty-swbut
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty-swbut-pr
  DEVICE xc7a50t-arty-swbut-pr1
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty-swbut-overlay
  DEVICE xc7a50t-arty-swbut-overlay
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty-switch-processing-pr1
  DEVICE xc7a50t-arty-switch-processing-pr1
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty-switch-processing-pr2
  DEVICE xc7a50t-arty-switch-processing-pr2
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty-switch-processing-overlay
  DEVICE xc7a50t-arty-switch-processing-overlay
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty-uart
  DEVICE xc7a50t-arty-uart
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty-full
  DEVICE xc7a50t
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a35tcsg324-1
)

add_xc_board(
  BOARD arty100t-full
  DEVICE xc7a100t
  PACKAGE test
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-basys3.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
  PART xc7a100tcsg324-1
)

add_xc_board(
  BOARD netv2-a100t
  DEVICE xc7a100t
  PACKAGE test
  PART xc7a100tfgg484-2
)

# TODO: https://github.com/SymbiFlow/symbiflow-arch-defs/issues/344
add_xc_board(
  BOARD zybo
  DEVICE xc7z010-zybo
  PACKAGE test
  PART xc7z010clg400-1
)

add_xc_board(
  BOARD zybo-full
  DEVICE xc7z010
  PACKAGE test
  PART xc7z010clg400-1
)

# TODO: fix openocd file
add_xc_board(
  BOARD zybo-fig1
  DEVICE xc7z010-fig1
  PACKAGE test
  PART xc7z010clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD nexys_video
  DEVICE xc7a200t
  PACKAGE test
  PART xc7a200tsbg484-1
  PROG_CMD "${OPENOCD} -f board/digilent_nexys_video.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD nexys_video-fig1
  DEVICE xc7a200t-fig1
  PACKAGE test
  PART xc7a200tffg1156-1
  PROG_CMD "${OPENOCD} -f board/digilent_nexys_video.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD nexys_video-mid
  DEVICE xc7a200t-mid
  PACKAGE test
  PART xc7a200tsbg484-1
  PROG_TOOL ${OPENOCD_TARGET}
  PROG_CMD "${OPENOCD} -f board/digilent_nexys_video.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

#add_xc_board(
#  BOARD zedboard-full
#  DEVICE xc7z020
#  PACKAGE test
#  PART xc7z020clg484-1
#)

#add_xc_board(
#  BOARD microzed-full
#  DEVICE xc7z020
#  PACKAGE test
#  PART xc7z020clg484-1
#)

add_xc_board(
  BOARD pynqz1-full
  DEVICE xc7z020
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-fig1
  DEVICE xc7z020-fig1
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-fig2-1600
  DEVICE xc7z020-fig2-1600
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-fig2-3200
  DEVICE xc7z020-fig2-3200
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-fig2-6400
  DEVICE xc7z020-fig2-6400
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-fig2-12800
  DEVICE xc7z020-fig2-12800
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-rendering-pr2
  DEVICE xc7z020-rendering-pr2
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-rendering-pr3
  DEVICE xc7z020-rendering-pr3
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-rendering-pr4
  DEVICE xc7z020-rendering-pr4
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-rendering-pr5
  DEVICE xc7z020-rendering-pr5
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-rendering-pr6
  DEVICE xc7z020-rendering-pr6
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-rendering-pr7
  DEVICE xc7z020-rendering-pr7
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

add_xc_board(
  BOARD pynqz1-rendering-pr8
  DEVICE xc7z020-rendering-pr8
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${PRJXRAY_DIR}/utils/openocd/board-digilent-pynqz1.cfg -c \\\"init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)

#add_xc_board(
#  BOARD marszx3-full
#  DEVICE xc7z020
#  PACKAGE test
#  PART xc7z020clg484-1
#)

add_xc_board(
  BOARD zybo-z7-20
  DEVICE xc7z020
  PACKAGE test
  PART xc7z020clg400-1
  PROG_CMD "${OPENOCD} -f ${OPENOCD_DATADIR}/scripts/interface/ftdi/digilent-hs1.cfg -f ${OPENOCD_DATADIR}/scripts/target/zynq_7000.cfg -c \\\"ftdi_tdo_sample_edge falling $<SEMICOLON> adapter_khz 1000000 $<SEMICOLON> init $<SEMICOLON> pld load 0 \${OUT_BIN} $<SEMICOLON> exit\\\""
)
