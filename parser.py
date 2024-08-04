from pydub import AudioSegment
import os
import speech_recognition as sr


def segment_audio(audio_file_name, audio_file_path, dest_file_dir, segment_length_ms=300000):
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
    for i in range(num_segments):
        start_time = i * segment_length_ms
        end_time = start_time + segment_length_ms
        segment = audio[start_time:end_time]
        
        # Export the segment to a new file
        segment_filename = os.path.join(dest_file_dir, f"{audio_file_name}_part_{i + 1}.wav")

        # Check if the output file already exists
        if os.path.exists(segment_filename):
            print(f"File {segment_filename} already exists!!! Skipping this segment...")
            continue

        segment.export(segment_filename, format="wav")
        print(f"Segment {i + 1} saved as {dest_file_dir}_part_{i + 1}.mp3")


def transcribe_audio(audio_file_path, duration_sec=300):
    """
    Transcribe audio.wav to hindi language text.
    """
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Load the audio file
    # audio = AudioSegment.from_mp3(file_path)

    # Extract the first 5 minutes (300 seconds) of the audio file
    # audio_segment = audio[:duration_sec * 1000]

    # Export this segment to a temporary WAV file
    # audio_segment.export("temp.wav", format="wav")

    # Transcribe the audio file
    with sr.AudioFile(audio_file_path) as source:
        audio_text = r.record(source)
        
        try:
            # Using Google speech recognition to transcribe in Hindi
            text = r.recognize_google(audio_text, language="hi-IN")
        except sr.UnknownValueError:
            text = "Sorry, I did not understand the audio."
        except sr.RequestError:
            text = "Sorry, my speech service is down."

    return text


def get_source_file_names(src_dir, dest_dir, text_dir):
    """
    Parse filenames and return a list of (src_file_name, src_file_path, dest_file_dir, text_path).
    """
    file_name_list = list()
    for file in os.listdir(sourceRecordsDir):
        if os.path.isfile(os.path.join(sourceRecordsDir, file)):
            src_fname, src_fextension = file.split('.', 1)
            # print(src_fname, file)
            src_fpath = os.path.join(sourceRecordsDir, file)
            dest_fdir = os.path.join(resultRecordsDir, src_fname)
            text_path = os.path.join(text_dir, src_fname)
            # print(dest_fdir)
            
            # append tuple to existing list
            file_name_list.append((src_fname, src_fpath, dest_fdir, text_path))
    
    return file_name_list


def write_text_to_file(text_data, audio_file_path, dest_text_dir):
    """
    Write hindi language text to file.
    """
    # Define the Hindi language string
    # hindi_text = "प्रिय मित्रो, स्वागत है आपका हमारे इस कार्यक्रम सत्य वचन में।"

    # Create output directory if it doesn't exist
    if not os.path.exists(dest_text_dir):
        os.makedirs(dest_text_dir)

    # Define the path to the text file
    afile_arr = audio_file_path.split('/')
    fname, fext = afile_arr[-1].split('.', 1)
    text_file_path = f"{dest_file_dir}/{fname}.txt"

    # Write the Hindi string to the text file
    with open(text_file_path, "w", encoding="utf-8") as file:
        file.write(text_data)

    print(f"Hindi text written to {text_file_path}")


##################################################################
if __name__ == '__main__':
    currWorkDir = os.getcwd()
    sourceRecordsDir = os.path.join('{cwd}/records/'.format(cwd=currWorkDir))
    resultRecordsDir = os.path.join('{cwd}/output/'.format(cwd=currWorkDir))

    # print(currWorkDir)
    # print(sourceRecordsDir)
    # print(resultRecordsDir)

    # Read all mp3 filenames from source.
    # all_audio_files = get_source_file_names(src_dir=sourceRecordsDir, dest_dir=resultRecordsDir)
    # print(all_audio_files)

    # Segment the audio and store in new directory
    # for audio_tuple in all_audio_files:
    #     segment_audio(audio_file_name=audio_tuple[0], audio_file_path=audio_tuple[1], dest_file_dir=audio_tuple[2])

    audio_file_path = '/Users/anurag/Projects/audio-parser/output/Timothy_1/Timothy_1_part_1.mp3'
    transcription = transcribe_audio(file_path=audio_file_path, duration_sec=300)
    print(transcription)
    