# AIW20A-59
## 개요
저기압, 고기압 중심 위치를 찾는 태스크
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (임의로 지정).
- input_file: 입/출력할 netcdf 파일의 경로
- PRMSL: 단일면 PRMSL(기압) 데이터 경로
- initial_alpha: 초기 step size(learning rate)
- output_task: 출력 경로
## 출력
저기압 중심을 -1로 표시하고 고기압 중심을 1로 표시한다.
## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2021070312gb2.nc INPUTDATA/PRMSL 0.001 task59
