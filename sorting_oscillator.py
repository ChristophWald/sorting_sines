import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd
import soundfile as sf

def bubblesort(arr):
    """
    takes an array to be sorted
    returns an array of arrays with all intermediate sorting steps
    """
    steps = [arr.copy()]
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr.copy())
    return steps

def track_sine_sorting(sorting_function):
    """
    takes a sorting function
    returns the intermediate steps as an array of arrays for sorting a sine wave
    """
    y = np.sin(np.linspace(0, 2 * np.pi, 64))
    steps = sorting_function(y)
    return steps

def generate_morphing_wavetable(
    wavetables, freq=220, morph_speed=1.0, samplerate=44100, hold_duration=0.5
):
    """
    Morph forward then backward through wavetables once,
    with hold_duration seconds of steady tone at start and end.

    Parameters:
        wavetables (list of np.ndarray): List of 1D wavetables.
        freq (float): Frequency in Hz.
        morph_speed (float): Morphs per second.
        samplerate (int): Sample rate.
        hold_duration (float): Seconds to hold first and last wavetable.

    Returns:
        np.ndarray: Stereo audio buffer (samples, 2), float32.
    """
    wavetables = [np.asarray(w) for w in wavetables]
    num_tables = len(wavetables)
    table_len = len(wavetables[0])

    # Calculate morph segments and duration as before
    total_morphs = 2 * (num_tables - 1)
    morph_duration = total_morphs / morph_speed
    morph_samples = int(morph_duration * samplerate)

    hold_samples = int(hold_duration * samplerate)

    total_samples = hold_samples + morph_samples + hold_samples
    samples = np.zeros(total_samples, dtype=np.float32)

    # Function to generate steady tone from one wavetable for N samples
    def generate_steady(wavetable, freq, samplerate, length_samples):
        phase_inc = freq * table_len / samplerate
        phase = 0.0
        out = np.zeros(length_samples, dtype=np.float32)
        for i in range(length_samples):
            idx = int(phase) % table_len
            idx_next = (idx + 1) % table_len
            frac = phase - int(phase)
            val = wavetable[idx] + (wavetable[idx_next] - wavetable[idx]) * frac
            out[i] = val
            phase += phase_inc
            if phase >= table_len:
                phase -= table_len
        return out

    # Fill hold at start (first wavetable)
    samples[:hold_samples] = generate_steady(
        wavetables[0], freq, samplerate, hold_samples
    )

    # Morph forward/backward in middle
    phase = 0.0
    table_index = 0
    morph_pos = 0.0
    morph_speed_per_sample = morph_speed / samplerate
    phase_inc = freq * table_len / samplerate
    forward = True

    for i in range(morph_samples):
        global_i = i + hold_samples
        next_index = table_index + 1 if forward else table_index - 1

        idx = phase % table_len
        idx_int = int(idx)
        idx_frac = idx - idx_int

        val1_curr = wavetables[table_index][idx_int]
        val2_curr = wavetables[table_index][(idx_int + 1) % table_len]
        curr_val = val1_curr + (val2_curr - val1_curr) * idx_frac

        val1_next = wavetables[next_index][idx_int]
        val2_next = wavetables[next_index][(idx_int + 1) % table_len]
        next_val = val1_next + (val2_next - val1_next) * idx_frac

        sample_val = curr_val * (1 - morph_pos) + next_val * morph_pos
        samples[global_i] = sample_val

        phase += phase_inc
        if phase >= table_len:
            phase -= table_len

        morph_pos += morph_speed_per_sample
        if morph_pos >= 1.0:
            morph_pos -= 1.0
            if forward:
                table_index += 1
                if table_index >= num_tables - 1:
                    forward = False
            else:
                table_index -= 1
                if table_index <= 0:
                    # Finished morphing early if needed
                    # but we fill tail anyway so just continue here
                    pass

    # Fill hold at end (last wavetable)
    samples[-hold_samples:] = generate_steady(
        wavetables[0], freq, samplerate, hold_samples
    )  # you can change to last wavetable if you prefer

    # Make stereo
    stereo = np.column_stack([samples, samples])
    return stereo.astype(np.float32)


def generate_morphing_animation_frames(
    wavetables,
    morph_speed=100.0,
    hold_duration=0.5,
    samplerate=44100,
    frames_per_second=60,
):
    """
    Generate animation frames (waveform arrays) that match morph speed and hold durations.

    Parameters:
        wavetables (list of np.ndarray): List of 1D wavetables.
        morph_speed (float): Morphs per second (same as audio).
        hold_duration (float): Seconds to hold first and last wavetable.
        samplerate (int): Sample rate (used to align timing).
        frames_per_second (int): Animation frame rate.

    Returns:
        np.ndarray: Array of shape (num_frames, wavetable_length), dtype float32.
    """
    wavetables = [np.asarray(w) for w in wavetables]
    num_tables = len(wavetables)
    table_len = len(wavetables[0])

    # Calculate total morph segments (forward + backward)
    total_morphs = 2 * (num_tables - 1)
    morph_duration = total_morphs / morph_speed

    # Calculate total animation duration and frame counts
    total_duration = hold_duration + morph_duration + hold_duration
    total_frames = int(total_duration * frames_per_second)

    # Frame counts for hold and morph
    hold_frames = int(hold_duration * frames_per_second)
    morph_frames = total_frames - 2 * hold_frames

    frames = np.zeros((total_frames, table_len), dtype=np.float32)

    # Helper function to morph between two wavetables with a morph parameter (0..1)
    def morph_waveforms(w1, w2, t):
        return w1 * (1 - t) + w2 * t

    # 1) Fill hold frames at start with first wavetable
    for i in range(hold_frames):
        frames[i] = wavetables[0]

    # 2) Morph forward then backward in the middle morph_frames
    # Morph segments count = total_morphs
    frames_per_morph = morph_frames / total_morphs

    for frame_i in range(morph_frames):
        global_frame = frame_i + hold_frames

        # Which morph segment are we in?
        morph_segment = int(frame_i // frames_per_morph)
        # progress in current morph segment [0..1)
        morph_progress = (frame_i % frames_per_morph) / frames_per_morph

        if morph_segment < num_tables - 1:
            # forward morph: segment 0..num_tables-2
            start_idx = morph_segment
            end_idx = start_idx + 1
        else:
            # backward morph: segment num_tables-1 .. total_morphs-1
            backward_seg = morph_segment - (num_tables - 1)
            start_idx = (num_tables - 1) - backward_seg
            end_idx = start_idx - 1

        frames[global_frame] = morph_waveforms(
            wavetables[start_idx], wavetables[end_idx], morph_progress
        )

    # 3) Hold last wavetable at end
    for i in range(hold_frames):
        frames[hold_frames + morph_frames + i] = wavetables[0]  # or wavetables[-1]

    return frames


def play_animation(frames, fps=60):
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, frames.shape[1])
    line, = ax.plot(x, frames[0])
    ax.set_ylim(-1.1, 1.1)
    ax.set_title("Wavetable Morphing Animation")
    ax.set_xlabel("Phase")
    ax.set_ylabel("Amplitude")

    def update(frame_idx):
        line.set_ydata(frames[frame_idx])
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=frames.shape[0], interval=1000 / fps, blit=True, repeat=False
    )
    plt.show()

def play_animation(frames, fps=60):
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, frames.shape[1])
    line, = ax.plot(x, frames[0])
    ax.set_ylim(-1.1, 1.1)
    ax.set_title("Wavetable Morphing Animation")
    ax.set_xlabel("Phase")
    ax.set_ylabel("Amplitude")

    def update(frame_idx):
        line.set_ydata(frames[frame_idx])
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=frames.shape[0], interval=1000 / fps, blit=True, repeat=False
    )
    plt.show()

if __name__ == "__main__":
    wavetables = track_sine_sorting(bubblesort)
    audio_fast = generate_morphing_wavetable_audio(wavetables, freq=220, morph_speed=500.0)
    #sf.write('morphing_sine.wav', audio_buffer, 44100)
    #sd.play(audio_fast, 44100)
    #sd.wait()  # wait until playback is done



