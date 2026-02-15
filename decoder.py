from config import *

class FastDecoder:
    def __init__(self):
        pygame.init()

    def decode_helper(self, video_file=None):
        # 1. Use a LIST to store chunks (much faster than repeated concatenation)
        pixel_chunks = []
        
        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            raise RuntimeError("Cannot open video")
        
        success, frame = cap.read()
        while success:
            # Convert BGR (OpenCV) -> RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w = rgb.shape[:2]

            # Create a pygame Surface from the raw bytes
            surf = pygame.image.frombuffer(rgb.tobytes(), (w, h), "RGB")

            # Standard Decode Logic
            arr = pygame.surfarray.array3d(surf)
            arr = np.transpose(arr, (1, 0, 2))
            pixels = arr.reshape(-1, 3)

            # Check for Blue Stop Signal
            is_blue = (pixels[:, 0] == 0) & (pixels[:, 1] == 0) & (pixels[:, 2] == 255)
            stop_index = np.argmax(is_blue)

            # Handle full-frame case
            if stop_index == 0 and not is_blue[0]:
                stop_index = len(pixels)

            # 3. Append the valid data to our list
            pixel_chunks.append(pixels[:stop_index])

            # Optional: If we found a stop signal that isn't the end of the frame,
            # we can technically stop processing future files here.
            if stop_index < len(pixels):
                 print(f"Stop signal found in, decoding complete, starting final assembly...")
                 break
            success, frame = cap.read()
        cap.release()

        # 4. Combine all chunks into one massive NumPy array at once
        if pixel_chunks:
            return np.vstack(pixel_chunks)
        else:
            return np.array([]).reshape(0, 3)
    
    def decode(self, fin, fout):
        valid_pixels = self.decode_helper(fin)
        
        if valid_pixels.size == 0:
            print("No data decoded.")
            return

        # Convert to bits (Look at Red channel)
        bits = (valid_pixels[:, 0] > 127).astype(np.uint8)

        # Pack and Save
        byte_data = np.packbits(bits)
        byte_data.tofile(fout)
        print(f"Decoded {len(byte_data)} bytes to {fout}")

# --- Usage ---
Decoder = FastDecoder()
Decoder.decode(VID_OUT_DIR / Path("out_video.avi"), "output_file.mp4")