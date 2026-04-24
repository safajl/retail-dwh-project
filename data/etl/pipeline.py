# ============================================================
# Pipeline -- Orchestrateur ETL principal
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import logging
import argparse
import sys
import os
from datetime import datetime

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.load_initial import DataLoaderInitial
from etl.load_incremental import DataLoaderIncremental

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            f'pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
    ]
)
logger = logging.getLogger(__name__)


def run_pipeline(mode='initial', raw_path='data/raw'):
    """
    Orchestre le pipeline ETL complet.

    Args:
        mode: 'initial' pour chargement complet,
              'incremental' pour chargement delta
        raw_path: chemin vers les fichiers CSV sources
    """
    start_time = datetime.now()
    logger.info('=' * 60)
    logger.info(f'DÉMARRAGE PIPELINE ETL -- Mode : {mode.upper()}')
    logger.info(f'Heure de début : {start_time}')
    logger.info('=' * 60)

    try:
        # ── Phase 1 : Extract ─────────────────────────────────
        logger.info('PHASE 1 : EXTRACTION')
        extractor = DataExtractor(raw_path=raw_path)
        raw_data  = extractor.run()
        logger.info(f'Extraction OK : {len(raw_data)} tables extraites')

        # ── Phase 2 : Transform ───────────────────────────────
        logger.info('PHASE 2 : TRANSFORMATION')
        transformer    = DataTransformer(raw_data)
        clean_data     = transformer.run()
        logger.info('Transformation OK')

        # ── Phase 3 : Load ────────────────────────────────────
        logger.info('PHASE 3 : CHARGEMENT')

        if mode == 'initial':
            loader = DataLoaderInitial()
            loader.run(clean_data)
        elif mode == 'incremental':
            loader = DataLoaderIncremental()
            loader.run(clean_data)
        else:
            raise ValueError(
                f'Mode invalide : {mode}. '
                f'Utiliser "initial" ou "incremental"'
            )

        # ── Résumé final ──────────────────────────────────────
        end_time  = datetime.now()
        duration  = (end_time - start_time).seconds
        logger.info('=' * 60)
        logger.info('PIPELINE TERMINÉ AVEC SUCCÈS ✓')
        logger.info(f'Durée totale : {duration} secondes')
        logger.info('=' * 60)

        return True

    except Exception as e:
        logger.error('=' * 60)
        logger.error(f'ERREUR PIPELINE : {str(e)}')
        logger.error('=' * 60)
        raise


if __name__ == '__main__':
    # Arguments en ligne de commande
    parser = argparse.ArgumentParser(
        description='Pipeline ETL -- DWH Retail'
    )
    parser.add_argument(
        '--mode',
        type=str,
        default='initial',
        choices=['initial', 'incremental'],
        help='Mode de chargement : initial ou incremental'
    )
    parser.add_argument(
        '--raw-path',
        type=str,
        default='data/raw',
        help='Chemin vers les fichiers CSV sources'
    )

    args = parser.parse_args()
    run_pipeline(mode=args.mode, raw_path=args.raw_path)