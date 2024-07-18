import torch
import torchvision.models as models

model = models.resnet34(pretrained=True)

dummy_input = torch.randn(1, 3,16 ,224, 224) #here the first thing is showing input variable with 1 than color with 3 , than 16 is for no of frames and than height with 224 and width with 224 as well 
torch.onnx.export(model, dummy_input, "resnet-34_ki.onnx")

#here with this code we can easily get pretrained model in onnx form and get to now what different thinggs are doing

