# projects
Для запуску моделі в себе на компютері вам потрібно зміни на правильні пути в конфігураційних файлах вже натренованих моделях в папці models/pre_train а саме у файлі pipeline.config, а саме:

fine_tune_checkpoint: "C:/Users/PC/Desktop/projects/pre-diploma practice/DP-main/models/pre_train/efficientdet_d0_coco17_tpu-32/checkpoint/ckpt-0"
label_map_path: "C:/Users/PC/Desktop/projects/pre-diploma practice/DP-main/annotations/label_map.pbtxt"

Train:
input_path: "C:/Users/PC/Desktop/projects/pre-diploma practice/DP-main/annotations/train.record"
label_map_path: "C:/Users/PC/Desktop/projects/pre-diploma practice/DP-main/annotations/label_map.pbtxt"

Test:
label_map_path: "C:/Users/PC/Desktop/projects/pre-diploma practice/DP-main/annotations/label_map.pbtxt"
input_path: "C:/Users/PC/Desktopprojects/pre-diploma practice/DP-main/annotations/test.record"


Запустити навчання командами #5 - #6, потрібно з деректорії pre-diploma practice

