Pycon 동영상 자막 번역하기
===========================

초벌 번역은 최대한 자동으로 하고
번역을 진행하여 작업 속도를 빠르게 하는것이 목적

작업할 영상, 자막 다운로드
----------------------------------------
`% youtube-dl --write-sub --sub-lang en --sub-format vtt $youtube_video_url`

사용법
------------------------------------

- 기존의 자막 파일의 영문을 1줄로 합침
  `% subtitle_edit.py -f $file_name -m`

- 수동으로 google translate에서 파일 모드로 번역기 돌림

- 구글 번역기는 타임레코드 포멧을 바꿔버려서 이를 다시 원복해주어야함
  Google translate mess time record format like,
    00 : 37 : 24.250 -> 00 : 37 : 30.160
    00 : 37 : 24.250-> 00 : 37 : 30.160
    00 : 37 : 24,250 -> 00 : 37 : 30.160

  Origin time record format,
    00:00:30.570 --> 00:00:36.600
    
  `subtitle_edit.py -f ./$translated_file_by_google -t`

- Vim을 이용해서 양쪽에 띄움
  `vim -O $origin_subtitle $step3_result_file`
  
   커서를 동시에 움직여야 하므로 `양쪽`화면에 바인딩 옵션 사용
   `:set scrollbind`

- 번역시작
