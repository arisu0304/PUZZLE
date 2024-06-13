import pygame
import sys
import random

# 화면 크기 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# 퍼즐 조각의 개수와 크기
ROWS = 3
COLS = 3
PIECE_SIZE = SCREEN_WIDTH // ROWS

# 색깔 정의
WHITE = (255, 255, 255)

# 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Puzzle Game")

clock = pygame.time.Clock()

# 이미지 파일 경로
image_path = r'C:\Users\bitcamp\Desktop\연습\06\images\test.jpg'

# 이미지 로드
try:
    original_image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Unable to load image: {image_path}")
    raise SystemExit(e)

# 이미지 크기 조정 (옵션)
image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 퍼즐 조각 생성
pieces = []
for i in range(ROWS):
    for j in range(COLS):
        # 퍼즐 조각의 위치 계산
        x = j * PIECE_SIZE
        y = i * PIECE_SIZE
        
        # 퍼즐 조각의 크기가 이미지를 벗어나지 않는지 확인
        if x + PIECE_SIZE <= SCREEN_WIDTH and y + PIECE_SIZE <= SCREEN_HEIGHT:
            piece = original_image.subsurface(pygame.Rect(x, y, PIECE_SIZE, PIECE_SIZE))
            pieces.append((piece, (j, i)))  # (이미지, 위치)
        else:
            print(f"Piece at ({j}, {i}) is outside the screen area.")

# 퍼즐 조각 섞기
random.shuffle(pieces)

# 빈 공간 위치 (오른쪽 하단)
empty_space = (ROWS - 1, COLS - 1)

# 유효한 이동 확인 함수
def is_valid_move(row, col):
    global empty_space
    empty_row, empty_col = empty_space
    
    # 클릭된 위치가 빈 공간 주변의 위치인지 확인
    if (row == empty_row and abs(col - empty_col) == 1) or (col == empty_col and abs(row - empty_row) == 1):
        return True
    return False

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 퍼즐 그리기
    for index, (piece, (row, col)) in enumerate(pieces):
        if (row, col) != empty_space:
            screen.blit(piece, (col * PIECE_SIZE, row * PIECE_SIZE))

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            clicked_col = mouse_x // PIECE_SIZE
            clicked_row = mouse_y // PIECE_SIZE

            # 클릭된 조각과 빈 공간의 위치 교환
            if is_valid_move(clicked_row, clicked_col):
                clicked_index = clicked_row * COLS + clicked_col
                empty_index = empty_space[0] * COLS + empty_space[1]
                
                pieces[empty_index], pieces[clicked_index] = pieces[clicked_index], pieces[empty_index]
                empty_space = (clicked_row, clicked_col)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
