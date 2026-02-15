from config import *

class FastDecoder:

    def decode_helper(self, video_file=None):
        pixel_chunks = []
        cap = cv2.VideoCapture(str(video_file))
        
        while True:
            success, frame = cap.read()
            if not success: break
            
            # # OpenCV is BGR. Convert to RGB for consistency with your Encoder
            # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # In the encoder, you transposed (H, W, 3) -> (W, H, 3) 
            # But OpenCV frames are (H, W, 3). 
            # To get the linear bitstream back, just flatten the H, W
            pixels = frame.reshape(-1, 3)

            # FUZZY Stop Signal Check (Important for Video!)
            is_blue = (pixels[:, 0] < 50) & (pixels[:, 1] < 50) & (pixels[:, 2] > 200)
            stop_index = np.argmax(is_blue)

            if stop_index == 0 and not is_blue[0]:
                stop_index = len(pixels)

            pixel_chunks.append(pixels[:stop_index])

            if stop_index < len(pixels):
                break
                
        cap.release()
        return np.vstack(pixel_chunks) if pixel_chunks else np.array([]).reshape(0, 3)
    
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