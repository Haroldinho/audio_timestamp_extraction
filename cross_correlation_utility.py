import numpy as np
from moviepy import VideoFileClip
from scipy import signal
import cv2


def audio_cross_correlation(full_video_path, clip_path):
    """
    Use audio cross-correlation to find a clip within a full video.

    Args:
        full_video_path (str): Path to the full video file
        clip_path (str): Path to the clip video file

    Returns:
        tuple: (start_time, end_time) in seconds
    """
    print("Extracting audio from videos...")
    # Extract audio from both videos
    full_video = VideoFileClip(full_video_path)
    clip_video = VideoFileClip(clip_path)

    # Get audio arrays
    full_audio = full_video.audio.to_soundarray(fps=22050)
    clip_audio = clip_video.audio.to_soundarray(fps=22050)

    # Convert to mono if stereo
    if len(full_audio.shape) > 1 and full_audio.shape[1] > 1:
        full_audio = np.mean(full_audio, axis=1)
    if len(clip_audio.shape) > 1 and clip_audio.shape[1] > 1:
        clip_audio = np.mean(clip_audio, axis=1)

    # Normalize audio signals
    full_audio = full_audio / np.max(np.abs(full_audio))
    clip_audio = clip_audio / np.max(np.abs(clip_audio))

    print("Computing cross-correlation...")
    # Fast cross-correlation using FFT
    correlation = signal.correlate(full_audio, clip_audio, mode="valid", method="fft")

    # Find the best match
    best_offset = np.argmax(correlation)
    correlation_strength = correlation[best_offset] / len(clip_audio)

    # Convert to time
    start_time = best_offset / 22050  # Convert samples to seconds
    end_time = start_time + clip_video.duration

    return start_time, end_time


def frame_cross_correlation(full_video_path, clip_path, sample_rate=10):
    """
    Use frame-based cross-correlation to find a clip within a full video.

    Args:
        full_video_path (str): Path to the full video file
        clip_path (str): Path to the clip video file
        sample_rate (int): Sample every nth frame for efficiency

    Returns:
        tuple: (start_time, end_time) in seconds
    """
    # Open videos
    full_video = cv2.VideoCapture(full_video_path)
    clip_video = cv2.VideoCapture(clip_path)

    # Get video properties
    full_fps = full_video.get(cv2.CAP_PROP_FPS)
    clip_fps = clip_video.get(cv2.CAP_PROP_FPS)
    full_frame_count = int(full_video.get(cv2.CAP_PROP_FRAME_COUNT))
    clip_frame_count = int(clip_video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Extract frames
    full_frames = []
    clip_frames = []

    # Extract sampled frames from full video
    for i in range(0, full_frame_count, sample_rate):
        full_video.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = full_video.read()
        if not ret:
            break

        # Convert to grayscale and flatten
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize for efficiency
        resized = cv2.resize(gray, (160, 120))
        # Flatten to 1D array
        full_frames.append(resized.flatten())

    # Extract all frames from clip
    for i in range(0, clip_frame_count, sample_rate):
        clip_video.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = clip_video.read()
        if not ret:
            break

        # Convert to grayscale and flatten
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize for efficiency
        resized = cv2.resize(gray, (160, 120))
        # Flatten to 1D array
        clip_frames.append(resized.flatten())

    # Convert to numpy arrays
    full_features = np.array(full_frames)
    clip_features = np.array(clip_frames)

    print("Computing frame cross-correlation...")
    # Compute cross-correlation for each clip frame with the full video
    # Using sliding window approach
    window_size = len(clip_features)
    scores = []

    for i in range(len(full_features) - window_size + 1):
        # Get window from full video
        window = full_features[i : i + window_size]

        # Compute correlation for each frame pair and average
        frame_correlations = []
        for j in range(window_size):
            # Normalize vectors for better correlation
            full_norm = window[j] / np.linalg.norm(window[j])
            clip_norm = clip_features[j] / np.linalg.norm(clip_features[j])

            # Compute correlation
            corr = np.dot(full_norm, clip_norm)
            frame_correlations.append(corr)

        # Average correlation across all frames
        avg_corr = np.mean(frame_correlations)
        scores.append(avg_corr)

    # Find best match
    if not scores:
        print("No valid windows found")
        return None, None

    best_idx = np.argmax(scores)
    best_score = scores[best_idx]

    # Calculate timestamps
    start_frame = best_idx * sample_rate
    start_time = start_frame / full_fps
    end_time = start_time + (clip_frame_count / clip_fps)

    return start_time, end_time
