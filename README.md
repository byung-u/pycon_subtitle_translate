Pycon 동영상 자막 번역하기
===========================

초벌 번역은 최대한 자동으로 하고
번역을 진행하여 작업 속도를 빠르게 하는것이 목적

Subtitle, Video download with youtube-dl
----------------------------------------
자막, 동영상 다운로드

`% youtube-dl --write-sub --sub-lang en --sub-format vtt $youtube_video_url`

USAGE
-----

1. 기존의 자막 파일의 영문을 1줄로 합침

  `subtitle_edit.py -f $file_name -m`

2. 자동으로 google translate 초벌번역

  `subtitle_edit.py -f $file_name --translate`

3. 번역된 것과 영어로 된 원문을 서로 합침 (번역이 올바른지 확인하기 위함)

  `subtitle_edit.py -f $file_name -i`

4. Vim을 이용해서 양쪽에 띄움

  `vim -O $origin_subtitle $step3_result_file`
  
   커서를 동시에 움직여야 하므로 `양쪽`화면에 바인딩 옵션 사용

   `:set scrollbind`

5. 번역시작


Release
-------
- 0.2.0 (current)
  - py-googletrans를 이용한 자동 번역 추가

- 0.1.0 (2017.01.06)
  - time record 제거 기능 추가
  - 2줄의 영문자막 한줄로 합침
  - 한글로 번역한 것과 기존의 영어 원문을 합치는 기능 추가
  - 수동 번역 후 --> 형식이 변경되어 다시 -->로 되돌리는 기능 추가
  

