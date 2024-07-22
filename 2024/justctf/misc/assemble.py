import os

def reassemble_chunks(chunks_dir, output_file):
    chunk_files = sorted(os.listdir(chunks_dir))
    
    if not chunk_files:
        print(f"No chunks found in directory: {chunks_dir}")
        return

    with open(output_file, 'wb') as outfile:
        for chunk_file in chunk_files:
            chunk_path = os.path.join(chunks_dir, chunk_file)
            
            if not os.path.isfile(chunk_path):
                print(f"Chunk file not found: {chunk_path}")
                continue
            
            print(f"Processing chunk: {chunk_file}")
            with open(chunk_path, 'rb') as infile:
                data = infile.read()
                outfile.write(data)
    
    print(f"Reassembled file saved to {output_file}")

# Reassemble video and audio chunks
reassemble_chunks('test', 'video.mp4')
#reassemble_chunks('test_2', 'audio.aac')

print('Reassembled video saved to video.h264')
print('Reassembled audio saved to audio.aac')
