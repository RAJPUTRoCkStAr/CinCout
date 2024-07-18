import torch
import torch.nn as nn

# Define the shape of the convolutional layer
out_channels = 64
in_channels = 3
kernel_size = (7, 7, 7)  # Kernel size along depth, height, and width dimensions

# Create the convolutional layer
conv_layer = nn.Conv3d(in_channels, out_channels, kernel_size)

# Initialize weights and bias for the convolutional layer (optional)
nn.init.xavier_uniform_(conv_layer.weight)
nn.init.zeros_(conv_layer.bias)

# Define the batch normalization parameters
num_features = 64  # Number of channels for batch normalization

# Create batch normalization layer
batch_norm = nn.BatchNorm3d(num_features)

# Initialize batch normalization parameters
nn.init.constant_(batch_norm.weight, 1)   # Set weights to 1
nn.init.constant_(batch_norm.bias, 0)     # Set bias to 0
nn.init.constant_(batch_norm.running_mean, 0)  # Set running mean to 0
nn.init.constant_(batch_norm.running_var, 1)   # Set running variance to 1

# Example input tensor shape (batch_size, channels, depth, height, width)
input_tensor = torch.randn(1, in_channels, 16, 224, 224)

# Forward pass through layers
output_tensor = conv_layer(input_tensor)
output_tensor = batch_norm(output_tensor)

print("Convolutional layer output shape:", output_tensor.shape)

# Export the model to ONNX
torch.onnx.export(
    nn.Sequential(conv_layer, batch_norm),
    input_tensor,
    "conv_batch_model.onnx",
    verbose=True
)

print("Model exported to 'conv_batch_model.onnx'")
