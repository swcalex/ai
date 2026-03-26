import torch
import torch.nn as nn
import torch.optim as optim
import pyaudio
import numpy as np
import model
import visualization_utils

# --- Configuration ---
CHUNK = 800           # 0.05 sec at 16kHz
RATE = 16000          # Sampling Rate
FORMAT = pyaudio.paFloat32 # -1.0 ~ 1.0 Float
CHANNELS = 1          # Mono

def main():
    print("=== Project AI v0.6.0: Real-time Audio Sensory System ===")
    
    # 1. Init Model
    net = model.AudioAutoencoder()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    
    # 2. Init Audio Stream
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"!! Audio Device Error: {e}")
        print("!! Please check your Microphone/Speaker settings.")
        return

    # 3. Init Visualizer
    visualizer = visualization_utils.RealtimeVisualizer(chunk_size=CHUNK)
    
    print(f">> Streaming started... (CHUNK={CHUNK}, RATE={RATE})")
    print(">> Speak into the microphone. Press Ctrl+C to stop.")

    step = 0
    
    try:
        while True:
            # --- A. SENSE (Input) ---
            # Read raw bytes from mic
            in_bytes = stream.read(CHUNK, exception_on_overflow=False)
            # Convert to numpy float32 (-1.0 ~ 1.0)
            in_data = np.frombuffer(in_bytes, dtype=np.float32)
            
            # Prepare Tensor
            # 안전하게 데이터를 복제하여 Writable 상태로 만듭니다.
            x = torch.from_numpy(in_data.copy()).float()

            # --- B. THINK & LEARN (Model Process) ---
            optimizer.zero_grad()
            
            # Forwardc
            y = net(x)
            
            # Loss Calculation (Self-Supervised: Target is Input)
            loss = criterion(y, x)
            
            # Backward & Update
            loss.backward()
            optimizer.step()
            
            # --- C. ACT (Output) ---
            # Convert Tensor back to numpy
            out_data = y.detach().numpy()
            
            # Play sound through speaker
            # (Make sure to wear headphones to avoid howling loop!)
            out_bytes = out_data.astype(np.float32).tobytes()
            stream.write(out_bytes)
            
            # --- D. OBSERVE (Visualization) ---
            # Update plot every 5 steps to reduce lag
            if step % 5 == 0:
                visualizer.update(in_data, out_data, loss.item())
            
            step += 1

    except KeyboardInterrupt:
        print("\n>> Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print(">> System Terminated.")

if __name__ == "__main__":
    main()