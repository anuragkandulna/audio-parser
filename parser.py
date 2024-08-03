from pydub import AudioSegment
import os


def segment_audio(audio_file_path, dest_file_dir, segment_length_ms=300000):
    """
    Cut audio and save to file.
    """
    # Load the audio file
    audio = AudioSegment.from_mp3(audio_file_path)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(dest_file_dir):
        os.makedirs(dest_file_dir)

    # Get the total duration of the audio file in milliseconds
    total_duration_ms = len(audio)
    
    # Calculate the number of segments
    num_segments = total_duration_ms // segment_length_ms + (1 if total_duration_ms % segment_length_ms != 0 else 0)
    
    # Split the audio into segments
    for i in range(1):
        start_time = i * segment_length_ms
        end_time = start_time + segment_length_ms
        segment = audio[start_time:end_time]
        
        # Export the segment to a new file
        segment_filename = os.path.join(dest_file_dir, f"_part_{i + 1}.mp3")

        # Check if the output file already exists
        if os.path.exists(segment_filename):
            print(f"File {segment_filename} already exists!!! Skipping this segment...")
            continue

        segment.export(segment_filename, format="mp3")
        print(f"Segment {i + 1} saved as {dest_file_dir}_part_{i + 1}.mp3")
        

# Path to the audio file
# audio_file_path = "path_to_your_audio_file.mp3"

# Segment the audio file into 5-minute chunks
# segment_audio(audio_file_path)


def get_source_file_names(src_dir, dest_dir):
    """
    Parse filenames and return a list of (src_file_name, src_file_path, dest_file_dir).
    """
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
    
    return file_name_list


##################################################################
if __name__ == '__main__':
    currWorkDir = os.getcwd()
    sourceRecordsDir = os.path.join('{cwd}/records/'.format(cwd=currWorkDir))
    resultRecordsDir = os.path.join('{cwd}/output/'.format(cwd=currWorkDir))

    print(currWorkDir)
    print(sourceRecordsDir)
    print(resultRecordsDir)

    # Read all mp3 filenames from source.
    all_audio_files = get_source_file_names(src_dir=sourceRecordsDir, dest_dir=resultRecordsDir)
    
    # Segment the audio and store in new directory
    for audio_tuple in all_audio_files:
        segment_audio(audio_file_path=audio_tuple[1], dest_file_dir=resultRecordsDir[2])
    