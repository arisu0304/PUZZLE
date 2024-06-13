import pygame
import sys
import random

# 화면 크기 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# 퍼즐 조각의 개수와 크기
ROWS = 2
COLS = 2
PIECE_SIZE = SCREEN_WIDTH // COLS

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
    image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Unable to load image: {image_path}")
    raise SystemExit(e)

# 이미지 크기 조정 (옵션)
image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 퍼즐 조각 생성
pieces = []
for i in range(ROWS):
    for j in range(COLS):
        piece_surface = image.subsurface(pygame.Rect(j * PIECE_SIZE, i * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE)).copy()
        pieces.append((piece_surface, (i, j)))  # 조각의 서피스와 위치를 저장

# 불일치 쌍 계산 함수
def count_inversions(pieces):
    inversions = 0
    for i in range(len(pieces)):
        for j in range(i + 1, len(pieces)):
            if pieces[i][1] != (ROWS - 1, COLS - 1) and pieces[j][1] != (ROWS - 1, COLS - 1):
                if pieces[i][1] > pieces[j][1]:
                    inversions += 1
    return inversions

# 퍼즐 조각 섞기
def shuffle_pieces(pieces):
    while True:
        random.shuffle(pieces)
        inversions = count_inversions(pieces)
        if inversions % 2 == 0:
            break

shuffle_pieces(pieces)

# 빈 공간 위치 (오른쪽 하단)
empty_space = (ROWS - 1, COLS - 1)

# 유효한 이동 확인 함수
def is_valid_move(row, col):
    empty_row, empty_col = empty_space
    # 클릭된 위치가 빈 공간 주변의 위치인지 확인
    if (row == empty_row and abs(col - empty_col) == 1) or (col == empty_col and abs(row - empty_row) == 1):
        return True
    return False

# 클리어 조건 확인 함수
def check_clear():
    for index, (_, (row, col)) in enumerate(pieces):
        if (index // COLS, index % COLS) != (row, col):
            return False
    return True

# 게임 루프
running = True
game_cleared = False
while running:
    screen.fill(WHITE)

    # 퍼즐 그리기
    for index, (piece_surface, (row, col)) in enumerate(pieces):
        if (index // 3, index % 3) != empty_space:
            screen.blit(piece_surface, (index // 3 * PIECE_SIZE, index % 3 * PIECE_SIZE))  # 조각의 서피스를 화면에 그림

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_cleared:
            mouse_x, mouse_y = event.pos
            clicked_row = mouse_x // PIECE_SIZE  # 마우스 클릭 좌표를 퍼즐 좌표로 변환
            clicked_col = mouse_y // PIECE_SIZE  # 마우스 클릭 좌표를 퍼즐 좌표로 변환

            # 클릭된 조각과 빈 공간의 위치 교환
            if is_valid_move(clicked_row, clicked_col):
                clicked_index = clicked_row * COLS + clicked_col
                empty_index = empty_space[0] * COLS + empty_space[1]

                # 조각의 서피스와 위치를 교환
                pieces[empty_index], pieces[clicked_index] = pieces[clicked_index], pieces[empty_index]
                empty_space = (clicked_row, clicked_col)

                # 클리어 조건 확인
                if check_clear():
                    game_cleared = True

    # 클리어 메시지 표시
    if game_cleared:
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
