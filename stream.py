def bytes_to_binary_stream(in_path, out_path, chunk_size=4096):
    with open(in_path, 'rb') as fin, open(out_path, 'w') as fout:
        while True:
            chunk = fin.read(chunk_size)
            if not chunk:
                break
            # Convert chunk bytes to binary and write immediately
            fout.write(''.join(f"{b:08b}" for b in chunk))
            