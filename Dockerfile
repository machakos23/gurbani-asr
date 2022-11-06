# syntax=docker/dockerfile:1

FROM alpine as builder
RUN apk --update --no-cache add git gcc make g++ zlib-dev cmake boost-system boost-thread boost-program_options boost-dev eigen-dev zlib-dev bzip2-dev xz-libs
RUN git clone https://github.com/kpu/kenlm
RUN cd kenlm && mkdir -p build && cd build && cmake .. && make -j `nproc`
RUN git clone https://github.com/FFTW/fftw3 && cd fftw3 && mkdir build && cd build && cmake ..

FROM python:3.8
RUN apt-get update && apt-get --no-install-recommends --yes install ffmpeg libsndfile1-dev liblzma-dev libbz2-dev libzstd-dev libopenblas-dev libfftw3-dev libgflags-dev libgoogle-glog-dev build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev 
COPY requirements.txt requirements.txt
COPY --from=builder /kenlm /kenlm

RUN pip install --no-cache-dir --upgrade pip torch==1.10.2+cpu torchaudio==0.10.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html -r requirements.txt
RUN git clone https://github.com/pytorch/fairseq && cd fairseq && git checkout b3491ae9 && pip install --editable ./
RUN git clone https://github.com/flashlight/flashlight && export USE_CUDA=0 KENLM_ROOT=/kenlm USE_MKL=0 && cd flashlight/bindings/python && python3 setup.py bdist_wheel && cd dist && pip3 install flashlight-1.0.0-cp38-cp38-linux_x86_64.whl 

COPY src /app
COPY models /app/models
COPY start /app
WORKDIR /app
EXPOSE 8000

CMD ["sh", "/app/start"]
