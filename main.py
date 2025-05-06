import argparse
from audio_utils.file_input import analyze_file
from audio_utils.live_input import analyze_live

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synesthetic Stage: Audio Visualizer")
    parser.add_argument("--file", type=str, help="Path to an audio file (e.g., WAV, MP3)")
    parser.add_argument("--mic", action="store_true", help="Use live microphone input")
    parser.add_argument("--duration", type=int, default=5, help="Recording duration in seconds (for mic input)")

    args = parser.parse_args()

    if args.file:
        print(f"🎧 Analyzing audio file: {args.file}")
        analyze_file(args.file)

    elif args.mic:
        print(f"🎙 Using microphone for {args.duration} seconds...")
        analyze_live(args.duration)

    else:
        print("❗ Please provide either --file <audio.wav> or --mic to begin.")
