import numpy as np
import matplotlib.pyplot as plt

class RealtimeVisualizer:
    def __init__(self, chunk_size=800):
        self.chunk_size = chunk_size
        self.loss_history = []
        
        # Interactive mode on
        plt.ion()
        self.fig, (self.ax_wave, self.ax_loss) = plt.subplots(2, 1, figsize=(10, 8))
        
        # 1. Waveform Plot
        self.x_axis = np.arange(chunk_size)
        self.line_input, = self.ax_wave.plot(self.x_axis, np.zeros(chunk_size), label='Input (Mic)', color='cyan', alpha=0.6)
        self.line_output, = self.ax_wave.plot(self.x_axis, np.zeros(chunk_size), label='Output (Model)', color='orange', alpha=0.8)
        
        self.ax_wave.set_ylim(-1.0, 1.0)
        self.ax_wave.set_title("Real-time Audio Waveform (Input vs Output)")
        self.ax_wave.legend(loc='upper right')
        self.ax_wave.grid(True, alpha=0.3)
        
        # 2. Loss Plot
        self.line_loss, = self.ax_loss.plot([], [], label='MSE Loss', color='red')
        self.ax_loss.set_xlim(0, 100) # Initial window
        self.ax_loss.set_ylim(0, 0.5)
        self.ax_loss.set_title("Learning Curve (MSE Loss)")
        self.ax_loss.set_xlabel("Steps (x10)")
        self.ax_loss.grid(True, alpha=0.3)
        
        plt.tight_layout()

    def update(self, input_data, output_data, current_loss):
        # Update Waveform
        self.line_input.set_ydata(input_data)
        self.line_output.set_ydata(output_data)
        
        # Update Loss History
        self.loss_history.append(current_loss)
        if len(self.loss_history) > 1000: # Keep last 1000 steps
            self.loss_history.pop(0)
            
        steps = np.arange(len(self.loss_history))
        self.line_loss.set_data(steps, self.loss_history)
        
        # Adjust Loss Axis dynamically
        if len(self.loss_history) > 10:
            self.ax_loss.set_xlim(0, len(self.loss_history))
            # Loss가 0일 경우를 대비해 최소 0.1의 범위를 확보합니다.
            current_max = max(self.loss_history) if self.loss_history else 0
            self.ax_loss.set_ylim(0, max(current_max * 1.1, 0.1))
        
        # [수정] 아래 두 줄을 지우고 plt.pause(0.001)로 교체하세요.
        # self.fig.canvas.draw()
        # self.fig.canvas.flush_events()
        
        plt.pause(0.001)  # 이 함수가 창을 갱신하고 유지시킵니다.