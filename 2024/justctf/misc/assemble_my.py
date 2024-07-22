import os
import re
import subprocess


def extract_number(filename): # order the files
    match = re.search(r'\((\d+)\)', filename)
    if match:
        return int(match.group(1))
    else:
        return 0

def reassemble_chunks_video(chunks_dir, number, video_dir):
    chunk_files = sorted(os.listdir(chunks_dir), key=lambda x: (not x.endswith('.mp4'), extract_number(x)))
    episode = f"episode_{number}"
    full_episode = f"episodes%2F{episode}"    
    output_file = episode + ".mp4"
    with open(os.path.join(video_dir, output_file), 'wb') as outfile: 
        for chunk_file in chunk_files:
            if ".mp4" in chunk_file: # check for .mp4 files
                if "video" in chunk_file: # check for video files
                    if full_episode + "_video" in chunk_file: # check for video files for that episode
                        
                        chunk_path = os.path.join(chunks_dir, chunk_file)
                        print(f"Processing chunk: {chunk_file}")
                        with open(chunk_path, 'rb') as file:
                            data = file.read()
                            outfile.write(data)

def reassemble_chunks_audio(chunks_dir, number, audio_dir):
    chunk_files = sorted(os.listdir(chunks_dir), key=lambda x: (not x.endswith('.mp4'), extract_number(x)))
    episode = f"episode_{number}"
    full_episode = f"episodes%2F{episode}"    
    output_file = episode + ".mp4"
    with open(os.path.join(audio_dir, output_file), 'wb') as outfile: 
        for chunk_file in chunk_files:
            if ".mp4" in chunk_file:
                if "audio" in chunk_file:
                    if full_episode + "_audio" in chunk_file:

                        chunk_path = os.path.join(chunks_dir, chunk_file)
                        print(f"Processing chunk: {chunk_file}")
                        with open(chunk_path, 'rb') as file:
                            data = file.read()
                            outfile.write(data)    

if not os.path.exists('video'):
    os.mkdir('video')

if not os.path.exists('audio'):
    os.mkdir('audio')


for i in range(32):
    reassemble_chunks_video('exported_http_objects', i, 'video')


for i in range(34):
    reassemble_chunks_audio('exported_http_objects', i , 'audio')


for i in range(34):
    # Construct the ffmpeg command
    input_video = f"video/episode_{i}.mp4"
    input_audio = f"audio/episode_{i}.mp4"
    output = f"episode_{i}.mp4"
    command = [
        'ffmpeg',
        '-i', input_video,
        '-i', input_audio,
        '-c:v', 'copy',
        '-c:a', 'aac',
        output
    ]
    
    # Execute the ffmpeg command
    try:
        subprocess.run(command, check=True)
        print(f'Conversion for {output} completed successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred: {e}')
