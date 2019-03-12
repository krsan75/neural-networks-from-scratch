import numpy as np

from math import sqrt

from .functional import sigmoid, sigmoid_prime


class Function:
    """
    Abstract model of a differentiable function.
    """
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        self.gradX_local = self.gradX(*args, **kwargs)
        self.output = self.forward(*args, **kwargs)
        return self.output

    def forward(self, *args, **kwargs):
        """
        Forward pass of the function. Calculates the output value and the
        gradient at the input as well.
        """
        pass

    def backward(self, *args, **kwargs):
        """
        Backward pass. Computes the local gradient at the input value
        after forward pass.
        """
        pass

    def gradX(self, *args, **kwargs):
        """
        Calculates the local derivative of the function at the given input.
        """
        pass


class Layer(Function):
    """
    Abstract model of a neural network layer. In addition to Function, a Layer
    also has weights and gradients with respect to the weights.
    """
    def init_weights(self, *args, **kwargs):
        pass

    def update_weights(self, *args, **kwargs):
        pass

    def gradW(self, x):
        pass


class Linear(Layer):
    __slots__ = ['weight', 'bias']

    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.init_weights(in_dim, out_dim)

    def init_weights(self, in_dim, out_dim):
        scale = 1 / sqrt(in_dim)
        self.weight = scale * (np.random.rand(in_dim, out_dim) - 0.5)
        self.bias = scale * (np.random.rand(1, out_dim) - 0.5)

    def update_weights(self, *args, **kwargs):
        pass

    def forward(self, x):
        """
        Forward pass for the Linear layer.

        Args:
            x: numpy.ndarray of shape (n_batch, in_dim) containing
                the input value.

        Returns:
            y: numpy.ndarray of shape of shape (n_batch, out_dim) containing
                the output value.
        """
        return np.dot(x, self.weight) + self.bias

    def backward(self, dy):
        """
        Backward pass for the Linear layer.

        Args:
            dy: numpy.ndarray of shape (n_batch, n_out). Global gradient
                backpropagated from the next layer.

        Returns:
            dx: numpy.ndarray of shape (n_batch, n_out). Global gradient
                of the Linear layer.
        """
        return dy.dot(self.weight.T)

    def gradX(self, x):
        """
        Local gradient of the Linear layer at x.

        Args:
            x: numpy.ndarray of shape (n_batch, in_dim) containing the
                input data.

        Returns:
            gradX: numpy.ndarray of shape (n_batch, in_dim), containing
                the local gradient at x.
        """
        return self.weight

    def gradW(self, x):
        pass


class Sigmoid(Layer):
    def forward(self, x):
        return sigmoid(x)

    def dx(self, x):
        return np.diag(sigmoid_prime(x).reshape(-1))


if __name__ == '__main__':
    linear = Linear(5, 2)
