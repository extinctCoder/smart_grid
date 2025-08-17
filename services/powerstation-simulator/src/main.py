import argparse
from time import sleep

from config import AppConfig, load_power_station_configs
from logger import getLogger
from station_simulator import StationSimulator

logger = getLogger(__name__)

ps_banner = r"""
 ____ ____ _________ ____ ____ ____ ____ ____ ____ ____ ____ ____
||P |||S |||       |||S |||I |||M |||U |||L |||A |||T |||O |||R ||
||__|||__|||_______|||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|

"""


def main():
    parser = argparse.ArgumentParser(
        description="⚡ Power Station Simulator",
        epilog="""
IMPORTANT:
- Use the --station-prefix (or -sp) flag to load power station-specific config.
- The required environment variables should be defined in a `.env` file or OS environment.
- When a prefix is given, all relevant keys will be loaded with that prefix applied.

See `src/config.py` for the complete list of supported configuration fields.

Examples:
  # Load config with prefix PS_001 (looks for variables like PS_001_*)
  python main.py --station-prefix PS_001

  # Load config with prefix TEST (looks for variables like TEST_*)
  python main.py -sp TEST
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-sp",
        "--station-prefix",
        type=str,
        help="Prefix for power station-specific environment variables (e.g., PS_001)",
    )

    args = parser.parse_args()

    print(ps_banner)
    logger.info(
        f"Simple Power Station SIMULATOR serving station : {args.station_prefix}"
    )
    app_config: AppConfig = load_power_station_configs(
        station_prefix=args.station_prefix
    )

    simulator: StationSimulator = StationSimulator(app_config=app_config)
    simulator.startup_sequence()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        simulator.shutdown_sequence()


if __name__ == "__main__":
    main()
