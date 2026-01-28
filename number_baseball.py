
import random

def generate_number():
    """3개의 겹치지 않는 숫자로 구성된 비밀 숫자를 생성합니다."""
    digits = list(range(10))
    random.shuffle(digits)
    # 첫 번째 숫자가 0이 아닌지 확인하고, 3자리 숫자를 만듭니다.
    while True:
        secret_number_list = [str(d) for d in digits[:3]]
        if secret_number_list[0] != '0':
            break
        random.shuffle(digits) # 다시 섞어서 첫 숫자가 0이 아닌지 확인
    return "".join(secret_number_list)

def get_guess():
    """사용자로부터 3자리 숫자를 입력받고 유효성을 검사합니다."""
    while True:
        guess = input("3자리 숫자를 입력하세요 (예: 123): ")
        if len(guess) == 3 and guess.isdigit():
            if len(set(list(guess))) == 3: # 겹치지 않는 숫자인지 확인
                return guess
            else:
                print("🚨 오류: 중복되지 않는 3자리 숫자를 입력해주세요.")
        else:
            print("🚨 오류: 3자리 숫자를 정확히 입력해주세요.")

def calculate_score(secret, guess):
    """비밀 숫자와 추측 숫자를 비교하여 스트라이크와 볼을 계산합니다."""
    strikes = 0
    balls = 0
    for i in range(3):
        if secret[i] == guess[i]:
            strikes += 1
        elif guess[i] in secret:
            balls += 1
    return strikes, balls

def play_game():
    """숫자 야구 게임을 플레이합니다."""
    secret_number = generate_number()
    attempts = 0
    print("⚾️ 숫자 야구 게임을 시작합니다! ⚾️")
    print("3개의 겹치지 않는 숫자로 구성된 비밀 숫자를 맞춰보세요.")
    print("--------------------------------------------------")

    while True:
        attempts += 1
        user_guess = get_guess()
        strikes, balls = calculate_score(secret_number, user_guess)

        print(f"결과: {strikes} 스트라이크, {balls} 볼")

        if strikes == 3:
            print(f"\n🎉 축하합니다! {attempts}번 만에 숫자를 맞췄습니다: {secret_number} 🎉")
            break
        elif strikes == 0 and balls == 0:
            print("아웃!")

        print("--------------------------------------------------")

if __name__ == "__main__":
    play_game()
