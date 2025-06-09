

import asyncio
import sys
import os
from pathlib import Path

from services.document_indexer import DocumentIndexingService


if __name__ == "__main__":
    indexer = DocumentIndexingService()
    asyncio.run(indexer.index_all_documents(force_reindex=False))


