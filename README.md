# saju_naming
Gemma 2 모델을 fine-tuning하여  
사용자의 생년월일과 성별로 사주를 풀이한 후,  
사용자에게 설명해주며 이를 보완할 수 있는 한국이름을 추천해주는 프로젝트다.

## Demo/Snapshot
아래의 영상은 해당 저장소에 있는 [saju_naming_server.ipynb](https://github.com/5KLetsGo/saju_naming/blob/main/saju_naming_fine_tuning.ipynb)를 Google Colab에서 실행하여 서버를 연 후,  
[saju_naming_web](https://5kletsgo.github.io/saju_naming_web/)에서 시연한 영상이다.  

https://github.com/user-attachments/assets/a7306b28-e6e2-4a9d-a131-136dcac0f8f7



아래의 사진은 해당 저장소에 있는 [saju_naming_execute.py](https://github.com/5KLetsGo/saju_naming/blob/main/saju_naming_execute.py)를 실행한 결과이다.

![saju_naming_cli](https://github.com/user-attachments/assets/6d75b356-b925-4780-b750-b7e2a1144051)


### Model Description
- **Developed by:** 강승곤, 유혁진, 이도건
- **Model type:** Casual Language Model
- **Language(s) (NLP):** Korean
- **License:** -
- **Finetuned from model [optional]:** rtzr/ko-gemma-2-9b-it

### Model Source
- **Hugging Face Repository:** https://huggingface.co/5KLetsGo/saju-naming

### Dataset
- crawled : 수집한 데이터
  - 한국 남자 이름
  - 한국 여자 이름
  - 인명 한자
  - 음양력 날짜
- prompt : 학습시킨 (질문, 답변) 형식의 prompt
  - 자원 오행 별 인명 한자 prompt
  - 자원 오행 해석 prompt
  - 한국 남자 이름 prompt
  - 한국 여자 이름 prompt
  - 자원 오행을 활용한 작명 prompt
  - 이름 의미 prompt

## 데이터
- 2008 ~ 2024년도 대한민국 신생아 이름 통계 [대한민국 법원 > 전자가족관계시스템](https://efamily.scourt.go.kr)
- 대한민국 인명용 한자 사전 [대한민국 법원](http://help.scourt.go.kr)
- 1950-01 ~ 2024-08 음양력 [공공데이터포털 한국천문연구원](https://www.data.go.kr/data/15012679/openapi.do)

## Reference
[사주팔자](https://ko.wikipedia.org/wiki/%EC%82%AC%EC%A3%BC%ED%8C%94%EC%9E%90)
