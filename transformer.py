import torch
import torchvision

# Load your trained PyTorch model
model = torch.load("./runs/detect/train/weights/best.pt")
model.eval()  # Set the model to evaluation mode

# Create a dummy input for the model
# Adjust the dimensions as needed (batch_size, channels, height, width)
dummy_input = torch.randn(1, 3, 416, 416)

# Export the model to ONNX format
# The input_names and output_names are optional but recommended for clarity
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    verbose=True,
    input_names=["input"],
    output_names=["output"],
)
