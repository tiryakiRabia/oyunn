import cv2
import mediapipe as mp

# Mediapipe El Modülü
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# Görüntü Yükle
image = cv2.imread(r"C:\Users\Dilanur\PycharmProjects\PythonProject\.venv\Scripts\el.jpg")
# örnek bir el fotoğrafı koy

# BGR'den RGB'ye çevir
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Elleri tespit et
results = hands.process(image_rgb)

# El bulunduysa çiz
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    print("El tespit edildi.")
else:
    print("El bulunamadı.")

# Sonucu göster
cv2.imshow("Sonuç", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
