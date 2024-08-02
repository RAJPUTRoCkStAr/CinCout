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
py Videos.py --model resnet-34_kinetics.onnx --classes Actions.txt --input media/yoga1.mp4 --gpu 1 --output yogaout.mp4
```
## how to view
```bash
netron resnet-34_kinetics.onnx 
```
## how to view attendance system
```bash
python app.py
```



