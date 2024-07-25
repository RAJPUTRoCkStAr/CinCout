## requirements need to install
```bash
pip install -r requirements.txt
```
## to run harde file
```bash
python Opencv.py --model resnet-34_kinetics.onnx --classes Actions.txt
```
## to run har file
```bash
py Video.py --model resnet-34_kinetics.onnx --classes Actions.txt --input media/sample.mp4 --gpu 1 --output sampleoutput.mp4
```
## how to view
```bash
netron resnet-34_kinetics.onnx 
```
## how to detect face using image
```bash
python detect_faces_image.py --image me.jpg --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel
```
## how to detect face using webcam
```bash
python detect_faces_video.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel
```

## how to run the one with casccader
```bash
py face.py
```

## how to run image classification
```bash
py image_activity.py 
```