# saju_naming
This project uses Gemma 2 fine-tuning to implement a model that explains dates of birth to interpret meanings of Sajupalja to users and generate related Korean names.

gemma 파인튜닝 모델입니다.

사주를 바탕으로 성별에 따른 한국 이름을 추천해주는 서비스입니다.

## 사용방법
스크린샷 몇 개 넣으면 좋을 듯..
날짜를 입력하세요 (형식: YYYY-MM-DD): 1980-01-02
성별을 입력하세요 (남자/여자): 남자


## 베이스 모델

9b 모델을 기반으로 파인튜닝을 진행하였으며,  "google/gemma-9b-it"의 한국어 버전인 "rtzr/ko-gemma-2-9b-it"을 사용하였습니다.
- gemma 한국어 버전 https://huggingface.co/rtzr/ko-gemma-2-9b-it

## 파인 튜닝
- LoRA 설정
lora_config = LoraConfig(
    lora_alpha = 8,
    lora_dropout = 0.1,
    r=16,
    target_modules=["k_proj", "o_proj", "v_proj", "q_proj", "gate_proj", "up_proj", "down_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)

lora_alpha = 8: lora_alpha는 LoRA의 학습 속도를 조절하는 하이퍼파라미터입니다. 큰 값일수록 학습 속도가 느려지며, 작은 값은 더 빠르게 학습됩니다. 보통 이 값은 LoRA의 업데이트 강도를 조절하는 스케일링 팩터로 사용됩니다.

lora_dropout = 0.1: 드롭아웃 확률을 의미합니다. 드롭아웃은 학습 중 일부 뉴런을 임시로 제거함으로써 모델의 일반화 능력을 향상시키는 방법입니다. 0.1은 10%의 뉴런을 드롭아웃 하겠다는 의미입니다.

r = 16: r은 LoRA에서 사용되는 저차원 행렬의 랭크(rank)를 나타냅니다. 이 값은 모델에 추가되는 저차원 행렬의 크기를 결정하며, 성능과 메모리 사용량에 영향을 미칩니다. 일반적으로 작은 값일수록 메모리 효율적입니다.

target_modules=["k_proj", "o_proj", "v_proj", "q_proj", "gate_proj", "up_proj", "down_proj"]: LoRA가 적용될 모듈 리스트입니다. 여기서 "k_proj", "o_proj", "v_proj", "q_proj" 등은 트랜스포머 모델의 다양한 투영(projection) 레이어를 의미합니다. 각각 키(key), 값(value), 쿼리(query) 등 주로 어텐션 메커니즘에 사용되는 레이어들입니다.

bias = "none": 편향(bias)을 추가할지 여부를 결정합니다. 여기서는 "none"으로 설정되어 있어 편향이 적용되지 않음을 나타냅니다.

task_type = "CAUSAL_LM": LoRA가 적용되는 작업 유형을 정의합니다. "CAUSAL_LM"은 인과적 언어 모델(Causal Language Modeling)을 의미합니다. 이는 GPT처럼 다음 단어를 예측하는 방식의 언어 모델에 해당합니다.

- 모델 설정
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    formatting_func=generate_prompt,
    max_seq_length=512,
    args=TrainingArguments(
        output_dir="./output",
        num_train_epochs = 1,
        max_steps=3000,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        optim="paged_adamw_8bit",
        warmup_steps=1,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=100,
        push_to_hub=False,
        report_to='none',
    ),
    peft_config=lora_config
)

model=model: 학습할 사전 훈련된 모델을 지정합니다. 여기서 model은 이전에 정의된 모델 객체를 참조하고 있습니다.

train_dataset=dataset: 학습에 사용할 데이터셋을 지정합니다. 이 데이터셋(dataset)에는 미리 준비된 학습용 데이터가 포함되어 있어야 합니다.

formatting_func=generate_prompt: 학습 데이터셋에서 각 샘플을 어떻게 포맷팅할지를 정의하는 함수입니다. 여기서 generate_prompt라는 함수가 각 데이터 샘플을 적절한 형식으로 변환하여 모델 입력으로 사용할 수 있도록 합니다.

max_seq_length=512: 각 입력 샘플의 최대 시퀀스 길이를 지정합니다. 여기서는 최대 512개의 토큰으로 시퀀스 길이를 제한하고 있습니다. 즉, 하나의 입력이 512개 이상의 토큰으로 이루어진 경우 잘리게 됩니다.

output_dir="/content/drive/MyDrive/Colab Notebooks/5KLetsGo/outputs-20241001-1530": 학습된 모델의 결과물을 저장할 디렉토리 경로입니다. 

num_train_epochs=1: 전체 데이터셋을 몇 번 반복하여 학습할지를 지정합니다.

max_steps=3000: 총 학습 스텝 수를 설정합니다.

per_device_train_batch_size=1: 한 번에 각 디바이스(GPU 또는 CPU)에서 학습할 배치 크기를 지정합니다.

gradient_accumulation_steps=4: 그라디언트를 축적하는 스텝 수를 지정합니다. 배치 크기가 작을 때 유용하며, 4번의 배치에 대해 그라디언트를 축적한 후, 업데이트가 이루어지도록 설정됩니다. 이를 통해 메모리 사용량을 줄이면서도 효과적인 학습을 할 수 있습니다.

optim="paged_adamw_8bit": 최적화 알고리즘으로 paged_adamw_8bit를 사용합니다. 이는 8비트 AdamW 최적화 알고리즘으로, 메모리 사용량을 줄여주면서도 효율적인 학습을 가능하게 합니다.

warmup_steps=1: 학습 초기에 워밍업 스텝을 1로 설정하여 학습 초기 단계에서 학습 속도를 천천히 증가시키는 기법입니다.

learning_rate=2e-4: 학습률을 설정합니다. 여기서는 2e-4로 매우 작은 값을 사용하여 안정적인 학습이 진행되도록 합니다.

fp16=True: 혼합 정밀도 학습을 사용하겠다는 설정입니다. FP16 (16-bit 부동 소수점)을 사용하여 학습 속도를 높이고, GPU 메모리 사용량을 줄일 수 있습니다.

logging_steps=100: 100 스텝마다 학습 로그를 출력합니다.

push_to_hub=False: 모델을 Hugging Face 허브로 업로드하지 않겠다는 설정입니다.

report_to='none': 학습 중에 보고할 툴을 설정합니다. 여기서는 아무 보고 툴도 사용하지 않겠다는 의미로 'none'으로 설정되어 있습니다.

peft_config=lora_config:LoRA(저차원 학습) 설정을 적용합니다. lora_config는 이전에 정의된 LoraConfig 객체로, LoRA를 이용하여 메모리 효율적인 학습을 수행하도록 설정합니다.

## 데이터
