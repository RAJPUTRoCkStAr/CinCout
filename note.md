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
py Video.py --model resnet-34_kinetics.onnx --classes Actions.txt --input videos/sample.mp4 --gpu 1 --output sampleoutput.mp4
```
## how to view
```bash
netron resnet-34_ki.onnx 
```