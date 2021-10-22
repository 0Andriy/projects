python scripts/partition_dataset.py -x -i def_marker -o images -r 0.1
python scripts/generate_labelmap.py -i images/class-names.txt
python scripts/generate_tfrecord.py -x images/train -l annotations/label_map.pbtxt -o annotations/train.record
python scripts/generate_tfrecord.py -x images/test -l annotations/label_map.pbtxt -o annotations/test.record