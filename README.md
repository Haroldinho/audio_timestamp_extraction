# Audio Timestamp Identification

A Python project that uses audio cross-correlation to identify the timestamp location of video clips within a larger video file. This tool is particularly useful for finding where specific clips appear in longer videos by analyzing their audio signatures.

## Overview

This project implements two main approaches for video clip identification:

1. **Audio Cross-Correlation**: Uses audio signal analysis to find clips within videos
2. **Frame Cross-Correlation**: Uses visual frame analysis (currently implemented but not used in main workflow)

The main workflow extracts audio from both the full video and the target clip, performs cross-correlation analysis, and returns the estimated start and end timestamps where the clip appears in the full video.

## Features

- Audio-based clip identification using cross-correlation
- Automatic timestamp extraction from clip filenames
- Performance evaluation with overlap metrics
- Support for multiple video formats (MP4, etc.)
- Efficient FFT-based correlation computation

## Project Structure

```
audio_timestamp_identification/
├── main.py                      # Main execution script
├── cross_correlation_utility.py # Core audio/frame correlation functions
├── extract_clip_from_movie.py   # Utility to create test clips
├── input_videos/                # Directory for full video files
├── input_clips/                 # Directory for test clip files
├── pyproject.toml              # Project dependencies and configuration
└── README.md                   # This file
```

## Installation and Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Make sure you have uv installed:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setting up the project:

1. **Clone or navigate to the project directory**
2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```
   This will create a virtual environment and install all required dependencies.

3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

### Dependencies

The project requires the following Python packages (managed by uv):

- `librosa>=0.11.0` - Audio analysis library
- `matplotlib>=3.10.6` - Plotting and visualization
- `moviepy>=2.2.1` - Video processing and audio extraction
- `opencv-python>=4.12.0.88` - Computer vision and video processing
- `seaborn>=0.13.2` - Statistical data visualization

## Usage

### Setting Up Input Data

Before running the analysis, you need to populate the `input_videos/` and `input_clips/` directories:

#### 1. Download the Source Video

Download the Planet Earth video from the Internet Archive:

```bash
# Create the input_videos directory if it doesn't exist
mkdir -p input_videos

# Download the video (this is a large file, ~1.5GB)
wget -O input_videos/planet_earth_01_from_pole_to_pole.mp4 \
  "https://ia800904.us.archive.org/8/items/planet_earth_1_bbc/planet_earth_01_from_pole_to_pole.mp4"
```

Alternatively, you can download it manually by visiting:
https://ia800904.us.archive.org/8/items/planet_earth_1_bbc/planet_earth_01_from_pole_to_pole.mp4

#### 2. Create Test Clips

Use the `extract_clip_from_movie.py` script to create test clips from the downloaded video:

```bash
# Create the input_clips directory if it doesn't exist
mkdir -p input_clips

# Run the clip extraction script
python extract_clip_from_movie.py
```

The script will create a clip file named `planet_earth_01_from_pole_to_pole_clip_2060_2075.mp4` in the `input_clips/` directory.

**To create additional clips with different timestamps:**

1. Edit `extract_clip_from_movie.py`:
   ```python
   # Change these values to your desired timestamps
   start_time = 130  # start time in seconds
   end_time = 145    # end time in seconds
   ```

2. Run the script again:
   ```bash
   python extract_clip_from_movie.py
   ```

This will create a new clip with the naming convention `planet_earth_01_from_pole_to_pole_clip_{start_time}_{end_time}.mp4`.

### Basic Usage

1. **Prepare your videos:**
   - Place the full video file in `input_videos/`
   - Place test clips in `input_clips/`
   - Ensure clip filenames follow the format: `video_name_{start_time}_{end_time}.mp4`

2. **Update the file paths in `main.py` (if using different filenames):**
   ```python
   VIDEO_PATH = "input_videos/your_video.mp4"
   CLIP_PATH_1 = "input_clips/your_clip_130_145.mp4"
   CLIP_PATH_2 = "input_clips/your_clip_2060_2075.mp4"
   ```

3. **Run the analysis:**
   ```bash
   python main.py
   ```

## How It Works

### Audio Cross-Correlation Process

1. **Audio Extraction**: 
   - Extracts audio from both the full video and the target clip
   - Converts to mono and normalizes the audio signals
   - Uses a sampling rate of 22,050 Hz

2. **Cross-Correlation**:
   - Performs FFT-based cross-correlation between the full video audio and clip audio
   - Finds the offset with the highest correlation score
   - Converts the offset to time coordinates

3. **Timestamp Calculation**:
   - Calculates start time based on the best correlation offset
   - Calculates end time by adding the clip duration to the start time

### Evaluation Metrics

The system evaluates performance using:

- **Euclidean Distance**: Measures the distance between estimated and ground truth timestamps
- **Overlap Ratio**: Calculates the percentage of overlap between estimated and ground truth time ranges

## API Reference

### `audio_cross_correlation(full_video_path, clip_path)`

Performs audio-based cross-correlation to find a clip within a full video.

**Parameters:**
- `full_video_path` (str): Path to the full video file
- `clip_path` (str): Path to the clip video file

**Returns:**
- `tuple`: (start_time, end_time) in seconds

### `extract_start_end_time_from_clip_path(clip_path)`

Extracts start and end times from a clip filename using regex pattern matching.

**Parameters:**
- `clip_path` (str): Path to the clip file

**Returns:**
- `tuple`: (start_time, end_time) as floats

**Raises:**
- `ValueError`: If the filename doesn't match the expected pattern

### `evaluate_overlap(gt_start_time, gt_end_time, est_start_time, est_end_time)`

Calculates the overlap ratio between ground truth and estimated time ranges.

**Parameters:**
- `gt_start_time` (float): Ground truth start time
- `gt_end_time` (float): Ground truth end time  
- `est_start_time` (float): Estimated start time
- `est_end_time` (float): Estimated end time

**Returns:**
- `float`: Overlap ratio (0.0 to 1.0)

## Example Output

```
Testing clip 1
Extracting audio from videos...
Computing cross-correlation...
Start time: 130.0, End time: 145.0
Euclidean distance: 0.0
Overlap: 1.0

Testing clip 2
Extracting audio from videos...
Computing cross-correlation...
Start time: 2060.0, End time: 2075.0
Euclidean distance: 0.0
Overlap: 1.0
```

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure video files exist in the specified paths
2. **Audio extraction failures**: Check that videos have audio tracks
3. **Memory issues**: For very large videos, consider using shorter clips or reducing sampling rate

### Performance Tips

- Use shorter clips for faster processing
- Ensure good audio quality in both source and target videos
- Consider the audio characteristics (music, speech, silence) for better correlation results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Dependencies Management with uv

### Adding New Dependencies

```bash
# Add a new dependency
uv add package_name

# Add a development dependency
uv add --dev package_name

# Add a specific version
uv add "package_name>=1.0.0"
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update a specific package
uv add package_name --upgrade
```

### Removing Dependencies

```bash
# Remove a dependency
uv remove package_name
```

### Environment Management

```bash
# Create a new environment
uv venv

# Activate environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Deactivate environment
deactivate

# Show installed packages
uv pip list

# Show dependency tree
uv pip show --tree
```
