# 디스코드 치즈 봇

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2888FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

![](screenshot.png?raw=true)

GitHub Actions를 통해 메이플스토리의 길드 컨텐츠 정산 결과를 디스코드 채널에 보내 주는 프로그램입니다.

<br>

## 사용법

1. 리포지토리를 포크합니다.
2. [Settings] - [Secrets and variables] - [Actions] - [New repository secret]
   - `API_KEY`: [NEXON Open API Key](https://openapi.nexon.com/ko/my-application/create-app/)를 발급받습니다.
   - `WEBHOOK_URL`: [채널 편집] - [연동] - [웹후크 만들기]
3. `main.py` 파일의 `guild_name`, `world_name` 변수를 길드에 맞춰 수정합니다.
