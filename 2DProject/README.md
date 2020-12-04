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
![개발 범위](https://user-images.githubusercontent.com/70787160/101151597-398beb80-3665-11eb-90ae-2fb8db20abe0.png)

# 개발 계획
![개발 계획](https://user-images.githubusercontent.com/70787160/101151608-3bee4580-3665-11eb-8e44-1f8a495cc837.png)

# Commit 횟수
![커밋](https://user-images.githubusercontent.com/70787160/101151590-37c22800-3665-11eb-8403-5353bcfdfea7.png)

# Game State의 게임 오브젝트
* 배경화면 : Background 클래스 활용
* 구름 : HorzScrollBackground 활용 -> 구름이 왼쪽으로 흐르는 애니메이션을 보여줍니다.
* 플레이어 : 각 동작마다 State를 만들어 State를 변경하는 방식을 활용
* 적 : 플레이어와 비슷하게 State를 만들어서 구현하고 확률을 통한 랜덤 값을 받아 움직이도록 하였습니다.
* 타일 : Tile은 적과 플레이어와의 바운드박스 충돌 검사를 모든 방향에서 진행합니다. 화면에 그려져 있는 타일만 검사하도록 했습니다.
* 가시 : 가시는 플레이어와 충돌체크를 해서 서로 닿을 시 플레이어를 바로 사망하도록 처리하였습니다.
* 아이템 : (목숨, 빨간포션, 파란포션, 키) 플레이어와 충돌하면 해당하는 기능을 수행하도록 구현하였습니다.
           목숨 : 목숨 +1, 빨간포션 : 힘 +1, 파란포션 : +속도, 키 : 게임클리어 확인
* 게임오버, 게임 클리어 폰트 : 플레이어가 죽거나, 게임을 클리어하면 화면에 해당하는 문자를 그렸습니다. 
* 시간 : 게임오버 혹은 게임클리어 상황이 되면 그 때까지 흘렀던 시간을 초 단위로 보여줍니다.


# 어려웠던 부분
 - 캐릭터의 세세한 움직임을 구현하는 것과 다양한 상황에서 여러가지 키 입력을 다루는 게 쉽지 않았습니다.

