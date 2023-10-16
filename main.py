import argparse
import pyroomacoustics as pra
from utils import load_signal_from_wav, circular_layout, write_signal_to_wav, write_spectrogram


def main(args):
    file_path = "impulse_response.wav"
    fs = 16000
    signal = load_signal_from_wav(file_path, fs)

    # 引数から次元とZ軸の大きさを取得
    dim = int(args.dim)
    z = int(args.z)

    m = pra.Material(energy_absorption=0.0)

    if dim == 3:
        room = pra.ShoeBox([10, 10, z], fs=fs, max_order=17, materials=m)
        room.add_microphone_array(circular_layout([5, 5, z], 0.1, 8))
        room.add_source([1, 1, z], signal=signal)
    else:
        room = pra.ShoeBox([10, 10], fs=fs, max_order=17, materials=m)
        mic_array = pra.MicrophoneArray(pra.circular_2D_array([5, 5], 8, 0, 0.1), room.fs)
        room.add_microphone_array(mic_array)
        room.add_source([1, 1], signal=signal)

    room.simulate()

    # 出力ファイル名を引数から取得
    write_signal_to_wav(room.mic_array.signals, f"output/{dim}d_{z}.wav", fs)

    # スペクトログラムをプロット
    write_spectrogram(room.mic_array.signals[0, :], f"output/{dim}d_{z}.png", fs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acoustic Simulation")
    # 次元の引数
    parser.add_argument("--dim", type=int, default=3, help="Dimensions for simulation (2 or 3)")
    # Z軸の大きさの引数
    parser.add_argument("--z", type=float, default=10, help="Size of the Z axis")
    args = parser.parse_args()
    main(args)
