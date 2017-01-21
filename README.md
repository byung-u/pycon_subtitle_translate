# Pycon 동영상 자막 번역하기
초벌 번역은 최대한 자동으로 하고
번역을 진행하여 작업 속도를 빠르게 하는것이 목적

# Subtitle, Video download with youtube-dl
`% youtube-dl --write-sub --sub-lang en --sub-format vtt $youtube_video_url`

# `subtitle_edit.py` 스크립트 사용하기

1. 기존의 자막 파일의 영문을 1줄로 합침
  `subtitle_edit.py -f $file_name -m`

2. 수동으로 google translate에서 파일 모드로 번역기 돌림

3. 구글 번역기는 타임레코드 포멧을 바꿔버려서 이를 다시 원복해주어야함
  Google translate mess time record format like,
    00 : 37 : 24.250 -> 00 : 37 : 30.160
    00 : 37 : 24.250-> 00 : 37 : 30.160
    00 : 37 : 24,250 -> 00 : 37 : 30.160

  Origin time record format,
    00:00:30.570 --> 00:00:36.600
    
  `subtitle_edit.py -f ./$translated_file_by_google -t`

4. 저같은 경우에는 Vim을 이용해서 양쪽에 띄움
  `vi -O $origin_subtitle $step3_result_file'

5. 번역시작
