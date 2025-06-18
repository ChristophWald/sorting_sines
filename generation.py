import numpy as np
from moviepy.editor import VideoClip
from moviepy.audio.AudioClip import AudioArrayClip
import matplotlib.pyplot as plt

def generate_morphing_wavetable(
    wavetables, freq=220, morph_speed=100, hold_duration=1
):
    samplerate = 44100
    wavetables = [np.asarray(w) for w in wavetables]
    num_tables = len(wavetables)
    table_len = len(wavetables[0])

    # Calculate morph parameters
    total_morphs = num_tables - 1  # only forward morphs
    morph_duration = total_morphs / morph_speed
    morph_samples = int(morph_duration * samplerate)
    hold_samples = int(hold_duration * samplerate)
    total_samples = hold_samples + morph_samples + hold_samples

    samples = np.zeros(total_samples, dtype=np.float32)

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

    # Hold at start (first wavetable)
    samples[:hold_samples] = generate_steady(
        wavetables[0], freq, samplerate, hold_samples
    )

    phase = 0.0
    table_index = 0
    morph_pos = 0.0
    morph_speed_per_sample = morph_speed / samplerate
    phase_inc = freq * table_len / samplerate

    for i in range(morph_samples):
        global_i = i + hold_samples
        next_index = table_index + 1

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
            table_index += 1
            if table_index >= num_tables - 1:
                # stop morphing once last wavetable reached
                break

    # Hold at end (last wavetable)
    samples[-hold_samples:] = generate_steady(
        wavetables[-1], freq, samplerate, hold_samples
    )

    # Stereo output
    stereo = np.column_stack([samples, samples])
    return stereo.astype(np.float32)


def generate_morphing_animation_frames(
    wavetables,
    morph_speed=100,
    hold_duration=1,
    frames_per_second=60,
):
    """
    Generate animation frames that morph forward through the wavetables once,
    with hold_duration seconds of hold at start and end.
    """

    wavetables = [np.asarray(w) for w in wavetables]
    num_tables = len(wavetables)
    table_len = len(wavetables[0])

    # Total morph segments = number of transitions between wavetables
    total_morphs = num_tables - 1

    # Duration of morphing in seconds (based on morph_speed in morphs per second)
    morph_duration = total_morphs / morph_speed

    # Total animation duration including holds
    total_duration = hold_duration + morph_duration + hold_duration

    total_frames = int(total_duration * frames_per_second)
    hold_frames = int(hold_duration * frames_per_second)
    morph_frames = total_frames - 2 * hold_frames

    frames = np.zeros((total_frames, table_len), dtype=np.float32)

    frames_per_morph = morph_frames / total_morphs

    def morph_waveforms(w1, w2, t):
        return w1 * (1 - t) + w2 * t

    # Hold first wavetable
    for i in range(hold_frames):
        frames[i] = wavetables[0]

    # Morph forward through the wavetables
    for frame_i in range(morph_frames):
        global_frame = frame_i + hold_frames

        morph_segment = int(frame_i // frames_per_morph)
        morph_progress = (frame_i % frames_per_morph) / frames_per_morph

        start_idx = morph_segment
        end_idx = start_idx + 1

        frames[global_frame] = morph_waveforms(
            wavetables[start_idx], wavetables[end_idx], morph_progress
        )

    # Hold last wavetable
    for i in range(hold_frames):
        frames[hold_frames + morph_frames + i] = wavetables[-1]

    return frames

def save_morphing_video(frames, audio, filename="output.mp4", fps=60, samplerate=44100):
    duration = len(audio) / samplerate
    wavetable_len = frames.shape[1]
    x = np.linspace(0, 2 * np.pi, wavetable_len)

    audio_clip = AudioArrayClip(audio, fps=samplerate)

    def make_frame(t):
        frame_idx = int(t * fps)
        if frame_idx >= len(frames):
            frame_idx = len(frames) - 1
        y = frames[frame_idx]

        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        ax.plot(x, y, color="dodgerblue")
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlim(0, 2 * np.pi)
        ax.axis("off")
        fig.tight_layout(pad=0)

        fig.canvas.draw()
        w, h = fig.canvas.get_width_height()
        buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8).reshape(h, w, 4)

        # Convert ARGB to RGB
        img = buf[:, :, [1, 2, 3]]

        plt.close(fig)
        return img

    video = VideoClip(make_frame, duration=duration)
    video = video.set_audio(audio_clip)
    video.write_videofile(filename, fps=fps, codec="libx264", audio_codec="aac")