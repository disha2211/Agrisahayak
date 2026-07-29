from pathlib import Path

from fastapi import HTTPException

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


class ImageValidator:

    @staticmethod
    async def validate(file):

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:

            raise HTTPException(
                status_code=400,
                detail="Unsupported image format."
            )

        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:

            raise HTTPException(
                status_code=413,
                detail="Image exceeds 10 MB."
            )

        await file.seek(0)

        return extension