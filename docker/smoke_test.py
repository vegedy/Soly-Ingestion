"""Verify the installed package using isolated Python outside the source tree."""

import sys
import sysconfig
from importlib import import_module
from importlib.metadata import version
from pathlib import Path


def main() -> None:
    if sys.version_info[:3] != (3, 12, 15):
        raise RuntimeError(f"Expected Python 3.12.15, got {sys.version}")
    package = import_module("soly_ingestion")
    if package.__file__ is None:
        raise RuntimeError("The installed package has no file")
    package_path = Path(package.__file__).resolve()
    site_packages = Path(sysconfig.get_path("purelib")).resolve()
    if not package_path.is_relative_to(site_packages):
        raise RuntimeError(f"Package imported outside site-packages: {package_path}")
    kafka = import_module("confluent_kafka")
    if version("confluent-kafka") != "2.16.0" or kafka.__version__ != "2.16.0":
        raise RuntimeError("Expected confluent-kafka 2.16.0")
    print(f"confluent-kafka {kafka.__version__}, librdkafka {kafka.libversion()}")
    print(f"Python {sys.version.split()[0]}")
    print(f"soly-ingestion {version('soly-ingestion')}: {package_path}")


if __name__ == "__main__":
    main()
