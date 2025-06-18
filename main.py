from sorting_algorithms import *
from generation import *
import argparse
import numpy as np
import soundfile as sf



def track_sine_sorting(sorting_function):
    """
    Takes a sorting function.
    Returns intermediate steps for sorting a sine wave.
    """
    y = np.sin(np.linspace(0, 2 * np.pi, 64))
    steps = sorting_function(y)
    return steps

def main(args):
    sorting_functions = {
        "bubblesort": bubblesort,
        "selectionsort": selectionsort,
        "insertionsort": insertionsort,
        "heapsort": heapsort,
        # add more sorting functions here later
    }
    sort_func = sorting_functions.get(args.sort)
    wavetables = track_sine_sorting(sort_func)
    audio = generate_morphing_wavetable(wavetables, freq=args.freq, morph_speed=args.speed, hold_duration=args.hold)
    if args.save_audio:
        sf.write("output.wav", audio, samplerate=44100)
    frames = generate_morphing_animation_frames(wavetables, morph_speed=args.speed, hold_duration=args.hold, frames_per_second=args.frames)
    save_morphing_video(frames, audio, filename="output.mp4", fps=args.frames)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sort",
        type=str,
        default="selectionsort",
    )
    parser.add_argument(
        "--freq",
        type = int,
        default = 220,
    )
    parser.add_argument(
        "--speed",
        type = int,
        default = 50,
    )
    parser.add_argument(
        "--hold",
        type=float,
        default = 1.0
    )
    parser.add_argument(
        "--save_audio",
        action="store_true",
    )
    parser.add_argument(
        "--frames",
        type= int,
        default= 12,
    )
    args = parser.parse_args()
    main(args)
    
    #
    #

