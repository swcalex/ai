# Project AI: Mathematical Foundation for AGI

## 1. 개요 (Overview)
본 프로젝트는 **"지능의 알고리즘을 수학적으로 규명하고 구현하는 것"**을 목표로 한다.
**v0.0.0** 단계에서는 정적 데이터 처리를 넘어, 연속적인 시간 속에서 감각 정보(청각)를 받아들이고 실시간으로 처리하는 지능의 기초를 다진다.

## 2. 프로젝트 구조 (Structure)

### 📄 문서 (Documents)
* **`algorithm_spec.md`**: **[핵심]** AI 모델의 수학적 정의 및 논리 설계도. (Updated for Audio Autoencoder)
* **`ai_rule.md`**: Architect(User)와 Engine(AI)의 협업 프로토콜.

### 🛠 구현체 (Implementation)
* `model.py`: `algorithm_spec.md`의 수식을 PyTorch로 번역한 신경망 모듈.
* `realtime_processor.py`: 마이크 입력, 모델 추론, 스피커 출력, 학습을 0.05초 루프로 수행하는 메인 엔진.
* `visualization_utils.py`: 실시간 파형 및 손실 그래프를 그리는 대시보드 도구.

## 3. 현재 단계: v0.0.0 (Real-time Audio Sensory)
* **Objective**: 소리 자체(Raw Audio)를 입력받아 압축(Think)하고 재구성(Act)하는 End-to-End 모델.
* **Key Features**:
    * **Architecture**: Input(800) $\to$ Hidden(100) $\to$ Output(800) with Tanh.
    * **Mechanism**: Online Learning (Real-time Feedback Loop).
    * **Environment**: Windows Laptop (Microphone + Headphone).