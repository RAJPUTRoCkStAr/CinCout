## requirements need to install
```bash
pip install -r requirements.txt
```
## to run harde file
```bash
python Videos.py --model resnet-34_kinetics.onnx --classes Actions.txt --yolo-cfg yolov3.cfg --yolo-weights yolov3.weights --yolo-classes coco.names
```
## to run har file
```bash
python Videos.py --model resnet-34_kinetics.onnx --classes Actions.txt --input media/boxing.mp4 --output output.mp4 --gpu 1 --yolo-cfg yolov3.cfg --yolo-weights yolov3.weights --yolo-classes coco.names
```
## how to view
```bash
netron resnet-34_kinetics.onnx 
```
## how to view attendance system
```bash
python app.py
```



