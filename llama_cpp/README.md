# 🚀 llama.cpp on Android (Termux) Optimization Project

삼성 갤럭시 폴드 3(Snapdragon 888, Adreno 660) 환경에서 `llama.cpp`를 빌드하고 최적화하기 위한 작업 기록입니다.

## 📱 Device Specifications
- **Model:** Samsung Galaxy Fold 3
- **Chipset:** Qualcomm Snapdragon 888 (Adreno 660 GPU)
- **RAM:** 12GB
- **OS:** Android (Termux Environment)

---

## 🛠 Build & Implementation Status

현재 `llama.cpp`를 활용하여 다양한 백엔드 가속을 시도 중이며, 각 단계별 이슈와 해결 방안을 정리합니다.

### 1. CPU Only (Standard Build)
- **상태:** ✅ 성공 (안정적 실행 가능)
- **이슈:** Gemma 3 등 최신 모델 실행 시 `Jinja Exception` 발생.
- **대응:** 소스 코드를 최신 메인 브랜치로 업데이트하여 템플릿 지원 패치 적용.

### 2. OpenCL (Adreno GPU Acceleration)
- **상태:** ⚠️ 부분 성공 (디버깅 중)
- **이슈:** `clCreateBufferWithProperties` 관련 `undefined symbol` 오류 및 시스템 네임스페이스 접근 제한.
- **대응:** - 시스템 `/vendor/lib64`의 `libOpenCL.so`를 Termux 내부로 복사 후 강제 링크.
  - `CL_TARGET_OPENCL_VERSION`을 200/300으로 명시하여 헤더 호환성 확보.

### 3. CLBlast (Optimized OpenCL)
- **상태:** 🛠 빌드 시도 중
- **이슈:** 안드로이드용 공유 라이브러리(`.so`) 링크 실패.
- **대응:** `ndk-sysroot`를 활용해 Termux 내에서 직접 CLBlast를 빌드하고 `LD_LIBRARY_PATH` 경로 설정.

### 4. Vulkan (Universal GPU Acceleration)
- **상태:** ❌ 이슈 추적 중 (Segmentation Fault)
- **이슈:** 컴파일 시 `no viable overloaded '='` 오류 및 실행 직후 크래시.
- **대응:** Vulkan SDK(Android) 설치 및 `glslangValidator` 도구 연동 확인 중.

---

## 🐞 Common Issues & Troubleshooting

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Segmentation Fault** | 드라이버 충돌 또는 메모리 할당 오류 | `-ngl 0` 테스트 및 `strace`를 통한 시스템 콜 추적 필요 |
| **Jinja Exception** | 모델 템플릿 불일치 | `llama.cpp` 최신 버전 업데이트 및 재빌드 |
| **OpenCL Symbol Error** | 버전 불일치 및 접근 권한 | 라이브러리 로컬 복사 및 링크 경로 재설정 |

---

## 🌐 External Integration (OpenClaw)
- **Server:** `llama-server`를 활용한 API 호스팅 (Port: 56810)
- **Integration:** OpenClaw 연결 시 발생하는 무한 로딩 및 토큰 초과 문제를 파라미터 튜닝을 통해 해결.

---

## 📝 Future Plans
- [ ] Vulkan 빌드 시 발생하는 `Segmentation Fault` 원인 파악 및 수정
- [ ] `termux-chroot` 환경에서의 드라이버 접근성 테스트
- [ ] Gemma-3-270m 모델 최적 양자화(Q8_0 등) 성능 벤치마크 수행
