import time
import os
from src.parser import get_source_file_names, segment_audio, get_all_audio_files_in_dir, transcribe_audio, write_text_to_file
from src.custom_logger import get_logger


def main():
    """
    All starts from main() in here.
    """
    # Invoke Logger
    LOGGER = get_logger(__name__)

    # Get respective directories.
    currWorkDir = os.getcwd()
    sourceRecordsDir = os.path.join('{cwd}/records/'.format(cwd=currWorkDir))
    resultRecordsDir = os.path.join('{cwd}/output/'.format(cwd=currWorkDir))
    textRecordsDir = os.path.join('{cwd}/text/'.format(cwd=currWorkDir))

    # Read all mp3 filenames from source.
    all_audio_files = get_source_file_names(src_dir=sourceRecordsDir, dest_dir=resultRecordsDir, text_dir=textRecordsDir)

    # Segment the audio and store in new directory
    for audio_tuple in all_audio_files:
        segment_audio(audio_file_name=audio_tuple[0], audio_file_path=audio_tuple[1], dest_file_dir=audio_tuple[2])

    # Get segmented audio list and then transcribe and write to file
    for audio_tuple in all_audio_files:
        segmented_audio_files = get_all_audio_files_in_dir(audio_file_dir=audio_tuple[2])

        for seg_fname, seg_fpath in segmented_audio_files:
            # Get transcription for audio segment
            transcription = transcribe_audio(audio_file_name=seg_fname, audio_file_path=seg_fpath, duration_sec=300)

            # Write transcribed text to file
            write_text_to_file(text_data=transcription, audio_file_name=seg_fname, audio_file_path=seg_fpath, dest_text_dir=audio_tuple[3])


# ==================================================== INVOKE MAIN HERE ======================================================= #
if __name__ == '__main__':
    main()
