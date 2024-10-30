#    ._________________.
#    |.---------------.|
#    ||               ||
#    ||   -._ .-.     ||
#    ||   -._| | |    ||
#    ||   -._|"|"|    ||
#    ||   -._|.-.|    ||
#    ||_______________||
#    /.-.-.-.-.-.-.-.-.\
#   /.-.-.-.-.-.-.-.-.-.\
#  /.-.-.-.-.-.-.-.-.-.-.\
# /______/__________\___o_\ Windows XP Better >>>>>>>>>>>>>>>> Win 14 Pro Max

###################################################################################################
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import logging
import os
import time
###################################################################################################
logging.basicConfig(filename='output.log', level=logging.ERROR)
###################################################################################################
soupe_visage = mp.solutions.face_detection
poulet_mains = mp.solutions.hands
###################################################################################################
def lister_cameras():
    cameras = []
    for i in range(10):  
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append(i)
            cap.release()
    return cameras
###################################################################################################
cameras_disponibles = lister_cameras()
if not cameras_disponibles:
    logging.error("Erreur : Aucune webcam disponible.")
    raise Exception("Erreur : Aucune webcam disponible.")
###################################################################################################
camera_index = cameras_disponibles[0] 
cap = cv2.VideoCapture(camera_index)
###################################################################################################
if not cap.isOpened():
    logging.error("Erreur : Impossible d'ouvrir la webcam.")
    raise Exception("Erreur : Impossible d'ouvrir la webcam.")
###################################################################################################
#              ,----------------,              ,---------,
#         ,-----------------------,          ,"        ,"|
#       ,"                      ,"|        ,"        ,"  |
#      +-----------------------+  |      ,"        ,"    |
#      |  .-----------------.  |  |     +---------+      |
#      |  |                 |  |  |     | -==----'|      |
#      |  |  I LOVE LINUX   |  |  |     |         |      |
#      |  |  Bad command or |  |  |/----|`---=    |      |
#      |  |  L:/$_          |  |  |   ,/|==== ooo |      ;
#      |  |                 |  |  |  // |(((( [33]|    ,"
#      |  `-----------------'  |," .;'| |((((     |  ,"
#      +-----------------------+  ;;  | |         |,"     -BxB-
#         /_)______________(_/  //'   | +---------+
#    ___________________________/___  `,
#   /  oooooooooooooooo  .o.  oooo /,   \,"-----------
#  / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
# /_==__==========__==_ooo__ooo=_/'   /___________,"
###################################################################################################
detecteur_visage = soupe_visage.FaceDetection(min_detection_confidence=0.7)
detecteur_mains = poulet_mains.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
largeur_ecran, hauteur_ecran = pyautogui.size()
suivi_visage = True
suivi_mains = True
def capture_ecran():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshot_{timestamp}.png")
    print("Capture d'écran enregistrée :", f"screenshot_{timestamp}.png")
def traiter_flux_video():
    global suivi_visage, suivi_mains
    while True:
        ret, cadre = cap.read()
###################################################################################################
        if not ret:
            logging.error("Erreur : Impossible de lire le flux vidéo.")
            break
###################################################################################################
        cadre_rgb = cv2.cvtColor(cadre, cv2.COLOR_BGR2RGB)
        cadre_rgb.flags.writeable = False
        if suivi_visage:
            resultats_visage = detecteur_visage.process(cadre_rgb)
###################################################################################################
        if suivi_mains:
            resultats_mains = detecteur_mains.process(cadre_rgb)
        cadre_rgb.flags.writeable = True
        cadre_bgr = cv2.cvtColor(cadre_rgb, cv2.COLOR_RGB2BGR)
###################################################################################################
        if suivi_visage and resultats_visage.detections:
            for detection in resultats_visage.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = cadre.shape
                x1, y1, largeur, hauteur = (bboxC.xmin * w, bboxC.ymin * h, bboxC.width * w, bboxC.height * h)
                cv2.rectangle(cadre_bgr, (int(x1), int(y1)), (int(x1 + largeur), int(y1 + hauteur)), (255, 0, 0), 2)
###################################################################################################
#                                  (O)
#                               __--|--__
#                       .------~---------~-----.
#                       | .------------------. |
#                       | |                  | |
#                       | |   .'''.  .'''.   | |
#                       | |   :    ''    :   | |
#                       | |   :          :   | |
#                       | |    '.      .'    | |
#                       | |      '.  .'      | |
# .------------.        | |        ''        | |  .------------.
# | O          |        | `------------------' |  |            |
# | O   .-----.|        `.____________________.'  |.-----.     |
# | O .'      ||          `-------.  .-------'    ||      `.   |
# |o*.'       ||   .--.      ____.'  `.____       ||       `.  |
# |.-'        || .-~--~-----~--------------~----. ||        `-.|
# ||          || |AST  .---------.|.--------.|()| ||          ||
# ||          || |     `---------'|`-o-=----'|  | ||          ||
# |`-._    AST|| |-*-*------------| *--  (==)|  | ||AST    _.-'|
# |    ~-.____|| |  Lester - AMC  |          |  | ||____.-~    |
###################################################################################################
        if suivi_mains and resultats_mains.multi_hand_landmarks:
            for main_landmarks in resultats_mains.multi_hand_landmarks:
                pointe_index = main_landmarks.landmark[poulet_mains.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = cadre.shape
                x = int(pointe_index.x * w)
                y = int(pointe_index.y * h)
                pyautogui.moveTo(largeur_ecran - (x * largeur_ecran / w), y * hauteur_ecran / h)
                mp.solutions.drawing_utils.draw_landmarks(cadre_bgr, main_landmarks, poulet_mains.HAND_CONNECTIONS)
                cv2.putText(cadre_bgr, f'Index: ({x}, {y})', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
###################################################################################################
        cv2.imshow("TACOS MIX + POUTIN + CHAWARMA", cadre_bgr)
###################################################################################################
        if cv2.waitKey(1) & 0xFF == ord('s'):
            capture_ecran()
###################################################################################################
#              ________________________________________________
#             /                       O                        \
#            |    _________________________________________     |
#            |   |                                         |    |
#            |   |  L:/home/$ sudo su                      |    |
#            |   |  [sudo] Mot de passe de bxb :           |    |
#            |   |  Désolé, essayez de nouveau.            |    |
#            |   |  [sudo] Mot de passe de bxb :           |    |
#            |   |  Désolé, essayez de nouveau.            |    |
#            |   |  [sudo] Mot de passe de bxb :           |    |
#            |   |  sudo: 3 saisies de mots de passe incor.|    |
#            |   |  L:/home/$ sudo rm -rf ./world/*        |    |
#            |   |                                         |    |
#            |   |                                         |    |
#            |   |                                         |    |
#            |   |                                         |    |
#            |   |_________________________________________|    |
#            |                                                  |
#             \_________________________________________________/
#                    \___________________________________/
#                 ___________________________________________
#              _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
#           _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
#        _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
#     _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
#  _-'.-.-.-.-.-. .---.-. .-------------------------. .-.---. .---.-.-.-.`-_
# :-------------------------------------------------------------------------:
# `---._.-------------------------------------------------------------._.---'



        if cv2.waitKey(1) & 0xFF == ord('v'): # Activer/désactiver les fonctionnalités avec 'v' et 'm'
            suivi_visage = not suivi_visage
            print("Suivi du visage :", "Activé" if suivi_visage else "Désactivé")

        if cv2.waitKey(1) & 0xFF == ord('m'):
            suivi_mains = not suivi_mains
            print("Suivi des mains :", "Activé" if suivi_mains else "Désactivé")
        if cv2.waitKey(1) & 0xFF == ord('q'): # Quitte la boucle si la touche 'q' est appuyée
            break


###################################################################################################
try:
    traiter_flux_video()
except Exception as e:
    logging.error(f"Erreur inattendue : {e}")
    print("Erreur inattendue :", e)
cap.release()
cv2.destroyAllWindows()
###################################################################################################

#   _______________                        |*\_/*|________
#  |  ___________  |     .-.     .-.      ||_/-\_|______  |
#  | |           | |    .****. .****.     | |           | |
#  | |   0   0   | |    .*****.*****.     | |   0   0   | |
#  | |     -     | |     .*********.      | |     -     | |
#  | |   \___/   | |      .*******.       | |   \___/   | |
#  | |___     ___| |       .*****.        | |___________| |
#  |_____|\_/|_____|        .***.         |_______________|
#    _|__|/ \|_|_.............*.............._|________|_
#   / ********** \                          / ********** \
#  /  ************  \                      /  ************  \
# --------------------                    --------------------

