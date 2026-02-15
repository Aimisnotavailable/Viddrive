from config import *

try:
    m = get_monitors()[0]
    W, H = m.width, m.height
    # W, H = 300, 420
except:
    W, H = 1920, 1080

class FastEncoder:
    def __init__(self):
        pygame.init()
        # We don't need a visible window for encoding
        self.screen = pygame.Surface((W, H))

    def encode(self, input_file):
        # 1. Read File & Convert to Bits
        try:
            # Read as raw bytes
            raw_data = np.fromfile(input_file, dtype=np.uint8)
        except FileNotFoundError:
            print("Input file not found.")
            return

        # Unpack bits (Byte 255 -> [1, 1, 1, 1, 1, 1, 1, 1])
        bits = np.unpackbits(raw_data)
        total_bits = bits.size
        
        # 2. Calculate Capacity
        pixels_per_frame = W * H
        # How many frames (images) do we need?
        total_frames = math.ceil(total_bits / pixels_per_frame)
        
        # If file is empty or fits in one frame but needs padding
        if total_frames == 0: total_frames = 1

        print(f"Encoding {total_bits} bits into {total_frames} frames ({W}x{H})...")

        # 3. Process Chunk by Chunk
        for i in range(total_frames):
            start = i * pixels_per_frame
            end = start + pixels_per_frame
            
            # Extract the bits for THIS frame
            chunk = bits[start:end]
            
            # Create a Blue canvas (Stop Signal background)
            # Shape: (Total Pixels, 3) -> Flattened for easy filling
            frame_data = np.full((pixels_per_frame, 3), BLUE, dtype=np.uint8)
            
            # Map bits to colors (0->Black, 1->White)
            # This uses the "Fancy Indexing" we discussed:
            # We create a palette and just index into it.
            palette = np.array([BLACK, WHITE])
            colors = palette[chunk]
            
            # Fill the frame data with the colors
            # We only fill up to the length of the chunk (in case it's the last partial frame)
            frame_data[:len(chunk)] = colors
            
            # Reshape to (Width, Height, 3) for Pygame
            # Note: We reshape to (H, W) first, then transpose, to match the Decoder's reading order
            frame_image = frame_data.reshape(H, W, 3)
            frame_image = np.transpose(frame_image, (1, 0, 2))
            
            # Save
            pygame.surfarray.blit_array(self.screen, frame_image)
            
            # Filename: 000.png, 001.png (Padding ensures correct sorting in Decoder)
            filename = os.path.join(IMG_OUT_DIR, f"{i:05d}.png")
            pygame.image.save(self.screen, filename)
            print(f"Saved frame {i+1}/{total_frames}: {filename}")


        print("Encoding complete. Generating video...")
        self.generate_video(VID_PATH / OUT_VIDEO_FILE)
        
    def generate_video(self, output_file):
        imgs = sorted(os.listdir(IMG_PATH))
        if not imgs:
            print("No images found in", IMG_PATH)
            return

        first_img_path = IMG_PATH / imgs[0]
        first_frame = cv2.imread(str(first_img_path))
        if first_frame is None:
            print("First image unreadable:", first_img_path)
            return

        height, width = first_frame.shape[:2]
        video = cv2.VideoWriter(str(output_file), CODEC, FPS, (width, height))

        for name in imgs:
            img_path = IMG_PATH / name
            frame = cv2.imread(str(img_path))
            if frame is None:
                print("Skipping unreadable file:", img_path)
                continue
            video.write(frame)

        video.release()
        print(f"Video saved to {output_file}")

e = FastEncoder()
e.encode("hehe.mp4")