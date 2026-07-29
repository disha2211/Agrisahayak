from pathlib import Path
import shutil
import uuid


class FileManager:

    TEMP_DIR = Path("temp")

    TEMP_DIR.mkdir(exist_ok=True)

    @classmethod
    def save_upload(cls, file, extension):

        filename = f"{uuid.uuid4()}{extension}"

        path = cls.TEMP_DIR / filename

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return path

    @staticmethod
    def delete(path: Path):

        if path.exists():
            path.unlink()