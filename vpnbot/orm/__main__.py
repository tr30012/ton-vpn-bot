import argparse
import logging
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Union

from alembic.config import CommandLine, Config

PROJECT_PATH = Path(__file__).parent.parent.resolve()


def make_alembic_config(cmd_opts: Union[argparse.Namespace, SimpleNamespace],
                        base_path: str = PROJECT_PATH) -> Config:

    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name,
                    cmd_opts=cmd_opts)

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))

    return config


def main():
    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    options = alembic.parser.parse_args()
    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))
