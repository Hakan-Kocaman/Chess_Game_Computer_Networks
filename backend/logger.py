
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(".log"),   # dosyaya yaz
        logging.StreamHandler()        # terminale de yaz
    ]
)

logger = logging.getLogger(__name__)
