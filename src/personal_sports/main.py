import logging
import pathlib

import whenever

log_dir = pathlib.Path(__file__).parent / "logs"
log_file = log_dir / f"personal_sports_{whenever.Instant.now().round('minute').format_iso()}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file),
    ],
)

from personal_sports.sport import formual1  # noqa: E402

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting personal sports data fetch...")
    formual1.main()
