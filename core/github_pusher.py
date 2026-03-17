import subprocess
import os
from core.logger import logger

class GitHubPusher:
    @staticmethod
    def push_changes(commit_message="Auto-update: New viral post published"):
        """
        Agrega los cambios, hace commit y sube a GitHub automáticamente.
        """
        try:
            # Verificar si es un repositorio git
            if not os.path.exists(".git"):
                logger.warning("No se detectó un repositorio Git. Saltando el Push automático.")
                return False

            # 1. Git Add (solo los archivos necesarios para el blog)
            subprocess.run(["git", "add", "web/data/posts.json"], check=True)
            subprocess.run(["git", "add", "web/data/images/"], check=True)
            
            # 2. Git Commit
            # Usamos -m para el mensaje. Si no hay cambios, git commit fallará, así que lo capturamos.
            result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
            
            if "nothing to commit" in result.stdout:
                logger.info("Nada nuevo para hacer commit.")
                return True

            # 3. Git Push
            logger.info("Subiendo cambios a GitHub...")
            subprocess.run(["git", "push"], check=True)
            
            logger.info("¡Despliegue automático en GitHub exitoso!")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Error en el proceso Git: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado en GitHubPusher: {e}")
            return False
