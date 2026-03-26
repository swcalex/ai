# Algorithm Specification: v0.0.0 (Real-time Audio Sensory)

## 1. 시스템 개요 (System Overview)
본 모델은 마이크로 입력된 소리 파형을 실시간으로 압축(Encoding)하고 재구성(Decoding)하는 **Autoencoder** 구조를 갖는다.
입력 자체가 정답이 되는 **Self-Supervised Learning**을 통해 소리의 구조적 특징을 학습한다.

### 1.1 데이터 제원 (Data Specification)
* **Sampling Rate**: $16,000 \text{ Hz}$
* **Buffer Size (Chunk)**: $0.05 \text{ sec}$ (50ms)
* **Input Dimension**: $N = 16,000 \times 0.05 = 800$ samples

## 2. 모델 정의 (Model Definition)
$$
f: \mathbb{R}^{800} \rightarrow \mathbb{R}^{800}
$$

### 2.1 구조 (Architecture)
* **Input Layer**: $\mathbf{x} \in [-1, 1]^{800}$
* **Hidden Layer (Bottleneck)**: $\mathbf{h} \in [-1, 1]^{100}$ (Compression Ratio: 1/8)
* **Output Layer**: $\mathbf{y} \in [-1, 1]^{800}$

### 2.2 순전파 수식 (Forward Propagation)
$$
\begin{aligned}
\mathbf{h} &= \tanh(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) \\
\mathbf{y} &= \tanh(\mathbf{W}_2 \mathbf{h} + \mathbf{b}_2)
\end{aligned}
$$
* **Activation**: Hyperbolic Tangent ($\tanh$)를 사용하여 오디오 신호의 위상($\pm$)과 범위를 보존한다.

## 3. 학습 알고리즘 (Learning Algorithm)
모델은 0.05초마다 들어오는 데이터 스트림에 대해 즉각적인 역전파를 수행한다 (Online Learning).

### 3.1 손실 함수 (Loss Function)
입력 파형과 재구성된 파형 사이의 차이를 최소화한다.
$$
L = \frac{1}{N} \sum_{i=1}^{N} (y_i - x_i)^2 \quad (\text{Mean Squared Error})
$$

### 3.2 최적화 (Optimization)
* **Optimizer**: Adam (Learning Rate: $1e-3$)
* **Process**: `Forward` $\rightarrow$ `Loss Calculation` $\rightarrow$ `Backpropagation` $\rightarrow$ `Weight Update` within 50ms.