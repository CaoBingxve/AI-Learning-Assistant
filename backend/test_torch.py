import torch

print("torch版本：", torch.__version__)
print("torch位置：", torch.__file__)
print("CUDA可用：", torch.cuda.is_available())

print("开始矩阵计算...")

x = torch.randn(100, 100)
y = x @ x.T

print("PyTorch计算成功")
print(y.shape)