# 무인 매장 이상 행동 감지 알리미
## :computer: 프로젝트 소개
- 무인 매장의 수가 늘어갈 수록 무인 매장에서의 절도 사건이 증가한다.
- 문제에 대한 어떤 해결이 있을까
- CCTV의 행동 감지를 통해 정상 행동과 이상 행동을 구분하여 알림을 울리게 만드는 프로그램을 만들어보자.
 ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/f93e385c-dc12-4bc8-8395-c2c49498b714)
 ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/053f6e00-8f9a-4e4d-bb56-4a603de729a8)
 ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/609350cd-e28c-4a17-866b-a23f81257f36)
 ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/a9627b61-6119-4306-810d-f14ff448a9ec)




## :calendar: 일정 및 계획
  - 2023.12.12~2024.01.09
   ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/123e2336-8724-4ab3-b901-e22ed8c0ec6d)
## :pencil: 순서
-    ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/afa2d4b8-4389-4cde-bc9d-995a4f33d2a0)

   #### 1. 객체 탐지 및 추적

   
   #### 2. 행동 인식
    - Openpose 나 MediaPipe와 같은 키 포인트 추정 알고리즘을 사용해 사람의 자세나 움직임을 분석
        - OpenPose : CNN을 사용한 2D포즈 추정 알고리즘
        - PopseNet : 웹 브라우저에서 실행 가능한 TensorFlow.js 모델
        - AlphaPose : OpenPose와 비슷하지만 더 높은 정확도와 속도를 제공, 다중 사람 포즈 추정에 효과적
        - DeepCut and DeeperCut : CNN 사용 여러 사람의 포즈를 동시에 추정하는데 효과적
        - HRNet : 고해상도의 키포인트 추정, 신체의 세부적인 움직임까지 포착할 수 있는 높은 정확도
    - 특정 행동 패턴 식별 ex) 물건을 집거나, 무언가를 숨기는 동작
  
   #### 3. 이상 탐지
    - 정상적인 행동 패턴과 이상 행동 패턴을 구별
    - ex) 특정 시간 동안 같은 위치에 머무는 것, 불규칙한 움직임 패턴, 비정상적인 속도의 움직임
  
  #### 4. 실시간 분석 및 알람 시스템
  
    - 이상 행동이 감지되면 관리자에게 알림

# 모델 구축 및 적용
![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/648372c5-a6ad-4f24-a96f-a62ddf216f48)

  #### 고려사항
    - 프라이버시 보호 : CCTV 기반 시스템은 프라이버시 침해 위험이 있으므로, 법률과 규정을 준수
    - 데이터 처리 : 고성능 컴퓨터 필요
    - 정확도 및 신뢰성 : 잘못된 알림을 최소화하는게 관건일 듯
## :heavy_check_mark: 기술 스택
-   ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/0cd5184d-73dc-4b1b-8adb-c5792c7eabc7)

- YOLO : Object Detection, KeyPoint
- MediaPipe : KeyPoint 3D



  ![image](https://github.com/yknlwca/SeSac_Fianl_Prj/assets/145303968/e974fc5a-4d5d-4ddc-a1fb-ecefa4661884)

