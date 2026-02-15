from config import *

try:
    m = get_monitors()[0]
    # W, H = m.width, m.height
    W, H = 1920, 1080
except:
    W, H = 1920, 1080

class FastEncoder:
    def __init__(self):
        pygame.init()
        # We don't need a visible window for encoding
        self.screen = pygame.Surface((W, H))

    def encode(self, input_file):
        # 1. Read File & Convert to Bits (as before)
        raw_data = np.fromfile(input_file, dtype=np.uint8)
        bits = np.unpackbits(raw_data)
        pixels_per_frame = W * H
        total_frames = math.ceil(bits.size / pixels_per_frame) or 1

        # 2. Setup VideoWriter directly
        # Using 'IYUV' for raw lossless frames in AVI container
        temp_avi = VID_PATH / OUT_VIDEO_FILE
        fourcc = cv2.VideoWriter_fourcc(*'IYUV')
        video = cv2.VideoWriter(str(temp_avi), fourcc, FPS, (W, H))

        palette = np.array([BLACK, WHITE], dtype=np.uint8)

        # 3. Direct Loop with tqdm
        for i in tqdm(range(total_frames), desc="🎥 Encoding Directly to Video"):
            start = i * pixels_per_frame
            chunk = bits[start:start + pixels_per_frame]
            
            # Create Blue background frame
            frame_data = np.full((pixels_per_frame, 3), BLUE, dtype=np.uint8)
            
            # Fill data
            frame_data[:len(chunk)] = palette[chunk]
            
            # Reshape to (H, W, 3) - OpenCV's expected format
            # Note: No transpose needed if we reshape correctly for CV2
            frame = frame_data.reshape((H, W, 3))
            
            # Write directly to the video stream in RAM
            video.write(frame)

        video.release()
        print("Video encoding complete. Saved to:", temp_avi)

e = FastEncoder()
e.encode("hehe.mp4")