"""Audio parser script source code."""

import time
import os
import speech_recognition as sr
from pydub import AudioSegment
from src.custom_logger import get_logger


# Invoke Logger
LOGGER = get_logger()


# --------------------------- Supporting functions start here ------------------------------- #
def get_source_file_names(src_dir, dest_dir, text_dir):
    """
    Parse filenames and return a list of (src_file_name, src_file_path, dest_file_dir, text_path).
    """
    file_name_list = list()

    # Iterate through all files/directories and add the mp3 file names to a list
    try:
        os.path.isdir(src_dir)
        os.path.isdir(dest_dir)
        os.path.isdir(text_dir)

    except Exception as ex:
        LOGGER.critical(f'Exception occurred when accessing {src_dir}: {ex}')
        raise UnknownValueError(f'Exception occurred when accessing {src_dir}: {ex}')

    for file in os.listdir(src_dir):
        if os.path.isfile(os.path.join(src_dir, file)):
            src_fname, src_fextension = file.split('.', 1)
            src_fpath = os.path.join(src_dir, file)
            dest_fdir = os.path.join(dest_dir, src_fname)
            text_path = os.path.join(text_dir, src_fname)
            
            # append tuple to existing list
            file_name_list.append((src_fname, src_fpath, dest_fdir, text_path))

    # print(f'All file names in here: {file_name_list}')
    LOGGER.info(f'Source dir details {src_dir}: {file_name_list}')
    return file_name_list


def get_all_audio_files_in_dir(audio_file_dir, file_extension=".mp3"):
    """
    Read all files in a directory and return list of audio files.
    """
    audio_files = list()

    # List all files first and then sort
    files = os.listdir(audio_file_dir)
    
    for file_name in files:
        file_path = os.path.join(audio_file_dir, file_name)
        if os.path.isfile(file_path):
            if (os.path.splitext(file_path)[1].lower() == file_extension):
                audio_files.append((file_name, file_path))
    
    # print(f'All *{file_extension} file in {audio_file_dir}: {audio_files}')
    LOGGER.info(f'List of all *{file_extension} files in {audio_file_dir}: {audio_files}')
    return audio_files


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
        segment_file_string = f"{audio_file_name}_part_{i + 1}.mp3"
        segment_filename = os.path.join(dest_file_dir, segment_file_string)

        # Check if the output file already exists
        if os.path.exists(segment_filename):
            print(f"File {segment_filename} already exists!!! Skipping this segment...")
            continue

        segment.export(segment_filename, format="wav")
        print(f"Segment {i + 1} saved as {segment_file_string}")


def transcribe_audio(audio_file_name, audio_file_path, duration_sec=300):
    """
    Transcribe audio.wav to hindi language text.
    """
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Load the audio file
    audio = AudioSegment.from_mp3(audio_file_path)

    # Export this segment to a temporary WAV file
    # epoch = int(time.time())
    # fname, fext = audio_file_name.split('.', 1)
    # temp_file_name = f"temp_{fname}_{epoch}.wav"
    # audio.export(temp_file_name, format="wav")
    # print(f'Successfully created temp wav audio file {temp_file_name}')
    # time.sleep(1)

    # Transcribe the audio file
    with sr.AudioFile(audio_file_path) as source:
        audio_text = r.record(source)

        try:
            # Using Google speech recognition to transcribe in Hindi
            # text = r.recognize_sphinx(audio_text, language="hi-IN")
            text = r.recognize_google(audio_text, language="hi-IN")
        # except sr.UnknownValueError:
        #     text = "Sorry, I did not understand the audio."
        # except sr.RequestError:
        #     text = "Sorry, my speech service is down."
        except Exception as ex:
            text = f"Exception occurred while processing file {audio_file_path}: {ex}"

    # Delete temp WAV file
    # try:
    #     os.remove(temp_file_name)
    # except Exception as ex:
    #     print(f'Exception occurred upon {temp_file_name} deletion: {ex}')

    return '' if 'Exception' in text else text


def write_text_to_file(text_data, audio_file_name, audio_file_path, dest_text_dir):
    """
    Write hindi language text to file.
    """
    # Define the Hindi language string
    # hindi_text = "प्रिय मित्रो, स्वागत है आपका हमारे इस कार्यक्रम सत्य वचन में।"

    # Create output directory if it doesn't exist
    if not os.path.exists(dest_text_dir):
        os.makedirs(dest_text_dir)

    # Define the path to the text file
    fname, fext = audio_file_name.split('.', 1)
    text_file_path = f"{dest_text_dir}/{fname}.txt"

    # Write the Hindi string to the text file
    with open(text_file_path, "w", encoding="utf-8") as file:
        file.write(text_data)

    print(f"Audio {audio_file_path} text written to {text_file_path}")
