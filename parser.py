from pydub import AudioSegment
import os


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
# audio_file_path = "path_to_your_audio_file.mp3"

# Segment the audio file into 5-minute chunks
# segment_audio(audio_file_path)

# Main 
if __name__ == '__main__':
    currWorkDir = os.getcwd()
    sourceRecordsDir = os.path.join('{cwd}/records/'.format(cwd=currWorkDir))
    resultRecordsDir = os.path.join('{cwd}/output/'.format(cwd=currWorkDir))

    print(currWorkDir)
    print(sourceRecordsDir)
    print(resultRecordsDir)

    # Read all mp3 filenames from source.
    # (src_file_name, src_file_path, dest_file_dir)
    file_name_list = list()
    for file in os.listdir(sourceRecordsDir):
        if os.path.isfile(os.path.join(sourceRecordsDir, file)):
            src_fname, src_fextension = file.split('.', 1)
            # print(src_fname, file)
            src_fpath = os.path.join(sourceRecordsDir, file)
            dest_fdir = os.path.join(resultRecordsDir, src_fname)
            print(dest_fdir)
            
            # append tuple to existing list
            file_name_list.append((src_fname, src_fpath, dest_fdir))
    
    print(file_name_list)