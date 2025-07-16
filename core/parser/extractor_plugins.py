import gzip
import zipfile
import lzma
import rarfile
import py7zr

from pathlib import Path
from typing import Optional


def extract_gz(file_path: Path, out_dir: Path) -> Optional[Path]:
    """
    Извлекает файл из gzip-архива.

    :param file_path: Путь к .gz файлу.
    :param out_dir: Папка для извлечения.
    :return: Путь к извлечённому файлу или None.
    """

    out_path = out_dir / file_path.with_suffix("").name
    with gzip.open(file_path, "rb") as f_in, open(out_path, "wb") as f_out:
        f_out.write(f_in.read())
    return out_path


def extract_xz(file_path: Path, out_dir: Path) -> Optional[Path]:
    """
    Извлекает файл из xz-архива.

    :param file_path: Путь к .xz файлу.
    :param out_dir: Папка для извлечения.
    :return: Путь к извлечённому файлу или None.
    """

    out_path = out_dir / file_path.with_suffix("").name
    with lzma.open(file_path, "rb") as f_in, open(out_path, "wb") as f_out:
        f_out.write(f_in.read())
    return out_path


def extract_zip(file_path: Path, out_dir: Path) -> Optional[Path]:
    """
    Извлекает первый .xml файл из zip-архива.

    :param file_path: Путь к .zip файлу.
    :param out_dir: Папка для извлечения.
    :return: Путь к извлечённому .xml файлу или None.
    """

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        for zip_info in zip_ref.infolist():
            if zip_info.filename.endswith(".xml"):
                out_path = out_dir / Path(zip_info.filename).name
                with open(out_path, "wb") as f_out:
                    f_out.write(zip_ref.read(zip_info.filename))
                return out_path
    return None


def extract_rar(file_path: Path, out_dir: Path) -> Optional[Path]:
    """
    Извлекает первый .xml файл из rar-архива.

    :param file_path: Путь к .rar файлу.
    :param out_dir: Папка для извлечения.
    :return: Путь к извлечённому .xml файлу или None.
    """

    with rarfile.RarFile(file_path) as rf:
        for entry in rf.infolist():
            if entry.filename.endswith(".xml"):
                out_path = out_dir / Path(entry.filename).name
                with open(out_path, "wb") as f_out:
                    f_out.write(rf.read(entry))
                return out_path
    return None


def extract_7z(file_path: Path, out_dir: Path) -> Optional[Path]:
    """
    Извлекает первый .xml файл из 7z-архива.

    :param file_path: Путь к .7z файлу.
    :param out_dir: Папка для извлечения.
    :return: Путь к извлечённому .xml файлу или None.
    """

    with py7zr.SevenZipFile(file_path, mode="r") as archive:
        for name, bio in archive.readall().items():
            if name.endswith(".xml"):
                out_path = out_dir / Path(name).name
                with open(out_path, "wb") as f_out:
                    f_out.write(bio.read())
                return out_path
    return None


"""
Словарь с функциями-обработчиками архивов по расширению файла.
Ключ - расширение файла, значение - функция для извлечения.
"""
EXTRACTION_PLUGINS = {
    ".gz": extract_gz,
    ".xz": extract_xz,
    ".zip": extract_zip,
    ".rar": extract_rar,
    ".7z": extract_7z,
}
