# Game Title
__SlashBit__ : 2D 공간에서 몬스터를 처치하며 스테이지를 통과하고 보스를 처치하는 짧은 게임입니다.
게임 스펠렁키를 보고 아이디어를 생각하였습니다. 장애물과 몬스터의 공격으로부터 제한된 목숨으로 생존하여야 합니다.

![image](https://user-images.githubusercontent.com/70787160/99893430-8d8cec80-2cc3-11eb-9dc9-41f23795fb32.png)

# Game Scene
* __Main Menu__
  - 게임 시작 시 나오는 메인메뉴
  - 게임 타이틀과 게임 시작 버튼 (Press Spacebar)을 표시
  - Resource : image = background, text(font)
  - Events : Spacebar = change to game state, ESC = exit program.

* __Stages__ (1, 2, 3, Boss)
  - 게임을 시작하고 나면 진행되는 상태
  - 남은 목숨, 진행 시간, 필드, 몬스터(보스), 발사체, 캐릭터, 아이템(HP up, damage up, speed up), 문(stage end), 시간(timer)
  - Stage end -> 새로운 맵을 로드한다. (보스맵까지 총 4개)
  - Resource : image = background, tiles, character, monsters, projectiles, HP, items(apple, sword, shoes), boss
             sound = player attack, player death, jump, enemy attack, enemy death, boss attack, boss death, win sound
  - Animation = player move, player attack, monster(boss) move, projectiles move.
  - Events : move(left, right), jump(up), attack(shift key), enter door (spacebar)
  - 상황에 따라 각 스테이지를 각각의 Scene으로 구현할 수도 있음.
  - HP가 0이 되거나 boss의 HP가 0이 되면 Result page로 변경
  - 몬스터의 위치, 아이템의 위치는 랜덤으로 구현

* __Result page__ (death)
  - 게임에서 죽거나 보스를 물리치고 게임이 끝났을 때 표시해주는 결과창
  - 게임에서 경과한 시간을 표시. 죽어있는 캐릭터의 모습, 재시작, 게임 나가기
  - Restart -> 처음부터 다시시작, back to menu -> 메인메뉴로 돌아가기
  - Resource : image = character death, text(font)
  - Events : UP key, Down key to choose scene(restart, main menu), select scene (spacebar)
  - restart -> time, hp reset.

# Skills
* 다른 수업에서 배운 기술 : 랜덤함수
* 2D게임프로그래밍 : 적 AI 구현, 충돌 검사, 시간 측정, 애니메이션, 사운드, 이미지의 페이드 소멸(점점 흐려짐) 등
* 어려운 기술 : 맵의 타일들을 랜덤하게 재배치하는 기술(출구까지 막힌 길이 없어야 한다), 지진효과(화면이 흔들리는 효과)

# 게임 흐름
![게임 흐름](https://user-images.githubusercontent.com/70787160/95533692-d42dcc80-0a1e-11eb-8e10-44960f8c3475.png)

# 개발 범위
![개발범위](https://user-images.githubusercontent.com/70787160/99893454-d5137880-2cc3-11eb-9821-6c8170fd25a6.png)

# 개발 계획
![개발계획](https://user-images.githubusercontent.com/70787160/99893460-e52b5800-2cc3-11eb-8959-bb7a6070a3ac.png)

# Main State의 게임 오브젝트
* 



