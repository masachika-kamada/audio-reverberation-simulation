import os
import wave

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly


def load_signal_from_wav(wav_file_path: str, expected_fs: int) -> np.ndarray:
    fs, signal = wavfile.read(wav_file_path)
    if fs != expected_fs:
        signal = signal.astype(float)
        signal = resample_poly(signal, expected_fs, fs)
    return signal


def circular_layout(center: np.ndarray, radius: float, num_items: int) -> np.ndarray:
    angles = np.linspace(0, 2 * np.pi, num_items, endpoint=False)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    z = np.ones_like(x) * center[2]
    return np.vstack((x, y, z))


def ensure_dir(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def scale_signal(signal: np.ndarray) -> np.ndarray:
    # スケーリングファクターを信号の最大絶対値に設定
    scaling_factor = np.max(np.abs(signal))
    # 音声データをスケーリングして int16 に変換
    return (signal * np.iinfo(np.int16).max / scaling_factor).astype(np.int16)


def write_signal_to_wav(signal: np.ndarray, wav_file_path: str, sample_rate: int) -> None:
    ensure_dir(wav_file_path)
    signal = scale_signal(signal)
    if len(signal.shape) == 1:
        channels = 1
    else:
        channels = signal.shape[0]
        signal = signal.T.flatten()

    with wave.open(wav_file_path, "w") as wave_out:
        wave_out.setnchannels(channels)
        wave_out.setsampwidth(2)
        wave_out.setframerate(sample_rate)
        wave_out.writeframes(signal.tobytes())


def write_spectrogram(data: np.ndarray, file_path: str, sample_rate: int) -> None:
    fig = plt.figure(figsize=(10, 4))
    spectrum, freqs, t, im = plt.specgram(data, NFFT=512, noverlap=int(512 / 16 * 15), Fs=sample_rate, cmap="inferno")
    fig.colorbar(im).set_label("Intensity [dB]")
    plt.xlabel("Time [sec]")
    plt.ylabel("Frequency [Hz]")
    plt.savefig(file_path)
    plt.close()
