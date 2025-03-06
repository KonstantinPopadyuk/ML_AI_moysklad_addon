from fastapi import APIRouter
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mlmodel_goods_router = APIRouter()

MODEL_SCRIPT_PATH = "MLModelsService/ds_sales_model/sales_multi_goods_7_30-60.py"

def update_model(script_path: str):
    if not Path(script_path).exists():
        raise FileNotFoundError(f"Model script not found: {script_path}")
    
    try:
        result = subprocess.run(
            ["python", script_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        error_msg = f"Script failed with code {e.returncode}: {e.stderr}"
        raise RuntimeError(error_msg) from e

@mlmodel_goods_router.get("/multi_goods_7_30-60")
async def create_model_multigoods73060():
    """
    This handle creates pickle file with predictions
    Intent to be used in Airflow DAG and not anywhere else
    """
    try:
        update_model(MODEL_SCRIPT_PATH)
        return {"status": "success of creating multi_goods_7_30-60"}
    except Exception as e:
        logger.error(f'{str(e)}')
        return {"status": "error"}