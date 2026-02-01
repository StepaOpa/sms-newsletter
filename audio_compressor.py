from pydub import AudioSegment
import os
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

TARGET_SIZE_BITS = 307*1024*8
TARGET_SIZE_BYTES = TARGET_SIZE_BITS / 8
RAW_AUDIO_DIR = "raw_audio"
COMPRESSED_AUDIO_DIR = "compressed_audio"

@dataclass
class AudioExportSettings:
    target_size_kb: int = 307
    raw_dir: str = "raw_audio"
    output_dir: str = "compressed_audio"
    safety_factor: float = 0.9
    sample_rate: int = 22050
    channels: int = 1
    format = 'ogg'
    codec = 'libopus'

    @property
    def target_size_bits(self) -> int:
        return self.target_size_kb * 1024 * 8

    @property
    def target_size_bytes(self) -> int:
        return self.target_size_kb * 1024
    
class AudioCompressor:
    def __init__(self, settings: AudioExportSettings):
        self.s = settings
        os.makedirs(self.s.raw_dir, exist_ok=True)
        os.makedirs(self.s.output_dir, exist_ok=True)
            
    def _load_audio(self, filepath: str) -> AudioSegment:
        audio = AudioSegment.from_file(filepath)
        return audio


    def compress_audio(self, filename: str):
        filepath = os.path.join(self.s.raw_dir, filename)
        audio = self._load_audio(filepath)
        
        duration_in_seconds = len(audio)/1000
        audio = audio.set_channels(1).set_frame_rate(22050)
        
        calculated_bitrate = (self.s.target_size_bits / duration_in_seconds) * self.s.safety_factor/ 1000
        name_without_ext = os.path.splitext(filename)[0]
        export_path = os.path.join(self.s.output_dir, f"compressed_{name_without_ext}.ogg")
        current_bitrate = calculated_bitrate
        best_safe_bitrate = None
        for i in range(5):
            target_bitrate = f"{int(current_bitrate)}k"    
            audio.export(export_path,
                                        format=self.s.format,
                                        codec=self.s.codec,
                                        bitrate=target_bitrate,
                                        )
            current_size = os.path.getsize(export_path)
            logger.info(f'\nПопытка {i+1}:\nТекущий битрейт: {target_bitrate},\nТекущий размер:{current_size} байт')

            ratio = self.s.target_size_bytes / current_size
            if current_size <= self.s.target_size_bytes:
                best_safe_bitrate = target_bitrate
                if 1 < ratio < 1.05:    
                    break
            current_bitrate = current_bitrate*ratio

        final_size = os.path.getsize(export_path)
        if final_size > self.s.target_size_bytes and best_safe_bitrate:
            logger.info(f"Последняя попытка превысила лимит. Откат к лучшему безопасному битрейту: {best_safe_bitrate}")
            audio.export(export_path,
                                        format=self.s.format,
                                        codec=self.s.codec,
                                        bitrate=target_bitrate,
                                        )
            





        # logger.info(f'')