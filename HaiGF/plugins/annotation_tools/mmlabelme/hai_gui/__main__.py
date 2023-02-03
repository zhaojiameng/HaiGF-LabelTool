import argparse
import codecs
import logging
import os
import os.path as osp
import sys
from pathlib import Path

import yaml
# from qtpy import QtCore
# from qtpy import QtWidgets
from PySide2 import QtCore, QtWidgets

pydir = Path(os.path.abspath(__file__)).parent
sys.path.append(os.path.abspath(f'{pydir.parent}'))  # zzd

from hai_gui import __appname__
from hai_gui import __version__
from hai_gui.app import MainWindow
from hai_gui.config import get_config
from hai_gui.logger import logger
from hai_gui.utils import newIcon

import matplotlib
matplotlib.use('Agg')


"""
This app is based on the open source project "labelme" under GUN licence: https://github.com/wkentaro/labelme
We think to the labelme team for providing the baseline.
"""



def main(args):
    # args = get_opt()

    if args.version:
        print("{0} {1}".format(__appname__, __version__))
        sys.exit(0)

    logger.setLevel(getattr(logging, args.logger_level.upper()))
    if hasattr(args, "flags"):
        if os.path.isfile(args.flags):
            with codecs.open(args.flags, "r", encoding="utf-8") as f:
                args.flags = [line.strip() for line in f if line.strip()]
        else:
            args.flags = [line for line in args.flags.split(",") if line]
    if hasattr(args, "labels"):
        if os.path.isfile(args.labels):
            with codecs.open(args.labels, "r", encoding="utf-8") as f:
                args.labels = [line.strip() for line in f if line.strip()]
        else:
            args.labels = [line for line in args.labels.split(",") if line]
    if hasattr(args, "label_flags"):
        if os.path.isfile(args.label_flags):
            with codecs.open(args.label_flags, "r", encoding="utf-8") as f:
                args.label_flags = yaml.safe_load(f)
        else:
            args.label_flags = yaml.safe_load(args.label_flags)

    # config for the gui
    config_from_args = args.__dict__
    config_from_args.pop("version")
    reset_config = config_from_args.pop("reset_config")
    filename = config_from_args.pop("filename")
    output = config_from_args.pop("output")
    config_file_or_yaml = config_from_args.pop("config")
    config = get_config(config_file_or_yaml, config_from_args)
    # print(config['mm'], config['canvas'])

    if not config["labels"] and config["validate_label"]:
        logger.error(
            "--labels must be specified with --validatelabel or "
            "validate_label: true in the config file "
            "(ex. ~/.labelmerc)."
        )
        sys.exit(1)

    output_file = None
    output_dir = None
    if output is not None:
        if output.endswith(".json"):
            output_file = output
        else:
            output_dir = output

    translator = QtCore.QTranslator()
    translator.load(
        QtCore.QLocale.system().name(),
        osp.dirname(osp.abspath(__file__)) + "/translate",
    )
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("icon"))
    app.installTranslator(translator)

    # print(f'config {config} \nfilename: {filename} \noutput_file: {output_file} \noutput_dir: {output_dir}')
    # print('end __main__.py')

    # filename = '/home/sawyer/data/test'
    # filename = '/home/sawyer/data/slice_P4_1217.tar/slice_P4_1217'
    # filename = f'{os.environ["HOME"]}/datasets/xsensing/mm_data/slice_P4_1217/vis'
    # filename = '/home/zzd/datasets/ceyu/raw_fall_images/getup1_2'
    win = MainWindow(
        config=config,
        filename=filename,
        output_file=output_file,
        output_dir=output_dir,
    )

    if reset_config:
        logger.info("Resetting Qt config: %s" % win.settings.fileName())
        win.settings.clear()
        sys.exit(0)

    win.show()
    win.raise_()
    sys.exit(app.exec_())

# this main block is required to generate executable by pyinstaller
if __name__ == "__main__":
    main()

