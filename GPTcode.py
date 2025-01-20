import taichi as ti
import genesis as gs

gs.init(backend=gs.metal)

def main():
    # 1) Scene 생성
    #    show_viewer=True 로 설정하면 interactive viewer(화면 창)가 열립니다.
    scene = gs.Scene(show_viewer=True)

    # 2) 간단한 Box(박스) 모프 생성
    #    size=(1, 1, 1)은 x, y, z 각 방향으로 1m 크기의 정육면체 박스를 뜻합니다.
    box_morph = gs.morphs.Box(size=(1, 1, 1),
                              pos=(0, 0, 2),   # 2m 높이에서 시작
                              fixed=False)     # 고정(fixed=False)이므로 중력의 영향 받음

    # 3) 박스를 Scene에 추가
    #    material, surface를 생략하면 기본 RigidMaterial, Plastic 표면이 적용됨
    scene.add_entity(morph=box_morph)
    
    # 4) Scene 빌드 (시뮬레이션 준비)
    scene.build()
    
    # 5) 시뮬레이션 루프
    #    특정 횟수만큼 step()을 호출해도 되고, while 문 등 자유롭게 가능
    for step in range(300):
        scene.step()  # 1스텝 시뮬레이션 전진
        
    # (참고) 시뮬레이션 종료 후 직접 앱을 닫지 않았다면, ESC 누르면 창이 닫힙니다.

if __name__ == "__main__":
    main()
