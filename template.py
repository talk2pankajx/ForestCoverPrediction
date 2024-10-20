from pathlib import Path
import os

package_name = "forest"

list_of_files = [
        
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/components/__init__.py",
    f"src/{package_name}/components/data_ingestion.py",
    f"src/{package_name}/components/data_validation.py",
    f"src/{package_name}/components/data_transformation.py",
    f"src/{package_name}/components/model_training.py",
    f"src/{package_name}/components/model_evaluation.py",
    f"src/{package_name}/components/model_pusher.py",
    f"src/{package_name}/constants/__init__.py",
    f"src/{package_name}/configuration/__init__.py",
    f"src/{package_name}/entity/__init__.py",
    f"src/{package_name}/exception/__init__.py",
    f"src/{package_name}/logger/__init__.py",
    f"src/{package_name}/utils/__init__.py",
    f"src/{package_name}/pipeline/__init__.py",
    f"src/{package_name}/pipeline/training_pipeline.py",
    f"src/{package_name}/pipeline/prediction_pipeline.py",
    "app.py",
    "requirements.txt",
    "notebooks/EDA.ipynb",
    "notebooks/Preprocessing.ipynb"
    
]   

for file_path in list_of_files:
    file_path=Path(file_path)
    file_dir, file_name =  os.path.split(file_path)
    
    if file_dir!='':
        os.makedirs(file_dir, exist_ok=True)
        
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path, 'w') as f:
            pass