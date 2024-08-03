from pydub import AudioSegment

def segment_audio(audio_file_path, segment_length_ms=300000):
    # Load the audio file
    audio = AudioSegment.from_mp3(audio_file_path)
    
    # Get the total duration of the audio file in milliseconds
    total_duration_ms = len(audio)
    
    # Calculate the number of segments
    num_segments = total_duration_ms // segment_length_ms + (1 if total_duration_ms % segment_length_ms != 0 else 0)
    
    # Split the audio into segments
    for i in range(num_segments):
        start_time = i * segment_length_ms
        end_time = start_time + segment_length_ms
        segment = audio[start_time:end_time]
        
        # Export the segment to a new file
        segment.export(f"segment_{i + 1}.mp3", format="mp3")
        print(f"Segment {i + 1} saved as segment_{i + 1}.mp3")

# Path to the audio file
audio_file_path = "path_to_your_audio_file.mp3"

# Segment the audio file into 5-minute chunks
segment_audio(audio_file_path)