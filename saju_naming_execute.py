# input.py에서 함수 임포트
import saju_naming_execute_input as inputs
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

base_model = "rtzr/ko-gemma-2-9b-it"

model = AutoModelForCausalLM.from_pretrained('5KLetsGo/saju-naming', device_map='auto', torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(base_model)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    model_kwargs={"torch_dtype": torch.bfloat16},
    tokenizer=tokenizer,
    device_map="auto",
)


# input.py에 정의된 함수들 호출
date_str, gender = inputs.get_user_input()
instruction_1, saju_date = inputs.generate_result(date_str, gender)

pipeline.model.eval()

messages_1 = [
    {"role": "user", "content": f"{instruction_1}"}
]

prompt_1 = pipeline.tokenizer.apply_chat_template(
    messages_1, 
    tokenize=False, 
    add_generation_prompt=True
)

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
]

outputs_1 = pipeline(
    prompt_1,
    max_new_tokens=2048,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)

# print(outputs_1[0]["generated_text"][len(prompt_1):])

first_output = outputs_1[0]["generated_text"][len(prompt_1):]

# 이름 추출하기
explain_part = instruction_1.split("일 때,")[0] + "입니다."
first_output = first_output.split("\n")
name_list = []
name_list.append(first_output[3] + "\n" + first_output[4] + "\n" + first_output[5])
name_list.append(first_output[7] + "\n" + first_output[8] + "\n" + first_output[9])
name_list.append(first_output[11] + "\n" + first_output[12] + "\n" + first_output[13])
name_list_without_elements = []
name_list_without_elements.append(first_output[3] + "\n" + first_output[4][:-8] + "\n" + first_output[5][:-8])
name_list_without_elements.append(first_output[7] + "\n" + first_output[8][:-8] + "\n" + first_output[9][:-8])
name_list_without_elements.append(first_output[11] + "\n" + first_output[12][:-8] + "\n" + first_output[13][:-8])

print()
print(first_output[2])
cnt = 1
for i in name_list_without_elements:
    print(f'{cnt}번')
    print(i)
    print()
    cnt += 1
    
selected_name = int(input('원하시는 이름을 번호만 입력하시오:'))

# 결과를 형식에 맞게 저장
instruction_2 = f"{name_list[selected_name - 1]}, 이 이름의 뜻 풀이해"

messages_2 = [
    {"role": "user", "content": f"{instruction_2}"}
]

prompt_2 = pipeline.tokenizer.apply_chat_template(
    messages_2, 
    tokenize=False, 
    add_generation_prompt=True
)

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
]

outputs_2 = pipeline(
    prompt_2,
    max_new_tokens=2048,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)

print()
print('----------------------------------------------')
print()
print(date_str)
print(f'{saju_date[0]}년 {saju_date[1]}월 {saju_date[2]}일')
print()
print(f'{explain_part} 이 사주는 ', end='')
for i in first_output[0].split(".")[:-3]:
    print(i, end='.')
print(f'이를 이용해 아래의 {gender} 이름을 추천합니다.')
print()
print(name_list_without_elements[selected_name - 1])
print()
print(f'이 이름은 {outputs_2[0]["generated_text"][len(prompt_2):-1]} 이란 뜻을 가집니다.')