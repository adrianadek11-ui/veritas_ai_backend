import subprocess
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("EXIFStripper")

def strip_and_spoof_metadata(input_path: str, output_path: str):
    """
    Usuwa oryginalne metadane ffmpeg/software i nadpisuje sygnatury urządzenia,
    symulując nagranie smartfonem (np. iPhone/Samsung).
    """
    cmd = [
        "ffmpeg", "-i", input_path,
        "-map_metadata", "-1",
        "-metadata", "comment=Captured via Mobile Device",
        "-metadata", "encoder=Lavf58.76.100",
        "-codec", "copy",
        output_path,
        "-y"
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log.info(f"[+] Metadane pliku {input_path} zostały pomyślnie wyczyszczone i zamaskowane.")
    except subprocess.CalledProcessError as e:
        log.error(f"[-] Błąd podczas czyszczenia metadanych EXIF: {e}")

if __name__ == "__main__":
    log.info("[*] Moduł EXIF Stripper zainicjalizowany w trybie gotowości.")
