from cross_correlation_utility import audio_cross_correlation
import numpy as np
from typing import Tuple
import re


VIDEO_PATH = "input_videos/planet_earth_01_from_pole_to_pole.mp4"
CLIP_PATH_1 = "input_clips/planet_earth_01_from_pole_to_pole_clip_130_145.mp4"
CLIP_PATH_2 = "input_clips/planet_earth_01_from_pole_to_pole_clip_2060_2075.mp4"


def extract_start_end_time_from_clip_path(clip_path: str) -> Tuple[float, float]:
    """
    Extract the start and end time from the clip path.
    """

    match = re.search(r"_(\d+)_(\d+)\.mp4", clip_path)
    if match:
        start_time = float(match.group(1))
        end_time = float(match.group(2))
        return start_time, end_time
    else:
        raise ValueError(f"Could not extract start and end time from clip path: {clip_path}")


def evaluate_overlap(
    gt_start_time: float, gt_end_time: float, est_start_time: float, est_end_time: float
) -> float:
    """
    Evaluate the overlap between the ground truth and estimated timestamps.
    """
    overlap = min(gt_end_time, est_end_time) - max(gt_start_time, est_start_time)
    return overlap / (gt_end_time - gt_start_time)


def test_estimating_clip_from_movie(clip_path: str):
    start_time, end_time = audio_cross_correlation(VIDEO_PATH, clip_path)
    # get gt start and end time from the clip path
    gt_start_time, gt_end_time = extract_start_end_time_from_clip_path(clip_path)
    print(f"Start time: {start_time}, End time: {end_time}")
    # Compare the timestamps with a simple euclidean distance
    euclidean_distance = np.sqrt((start_time - gt_start_time) ** 2 + (end_time - gt_end_time) ** 2)
    print(f"Euclidean distance: {euclidean_distance}")
    # Print the overlap
    overlap = evaluate_overlap(gt_start_time, gt_end_time, start_time, end_time)
    print(f"Overlap: {overlap}")


def main():
    print("Testing clip 1")
    test_estimating_clip_from_movie(CLIP_PATH_1)
    print("\n\nTesting clip 2")
    test_estimating_clip_from_movie(CLIP_PATH_2)


if __name__ == "__main__":
    main()
