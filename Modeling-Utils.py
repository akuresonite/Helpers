# ==================================================================
#                                 5
# ==================================================================
!pip install graphviz
!pip install git+https://github.com/mert-kurttutan/torchview.git
from torchview import draw_graph
import graphviz
graphviz.set_jupyter_format('png')
model_graph = draw_graph(model, input_size=(1, 3, 224, 224), expand_nested=True, save_graph=False)
model_graph.visual_graph.render(filename="model_architecture", format="svg", view=True)
model_graph.visual_graph

!pip install cairosvg pillow
from PIL import Image
import cairosvg
cairosvg.svg2png(url="model_architecture.svg", write_to="model_architecture.png", dpi=300)


# ==================================================================
#                                 4
# ==================================================================
!pip install torchinfo
from torchinfo import summary
summary(model=model,
        # input_data=images,
        input_size = (1,3,224,224),
        col_names = ["input_size", "output_size", "num_params", "trainable", "params_percent"],
        col_width=20,
        row_settings=["var_names"],
        depth = 1,
        # device=device
)


# ==================================================================
#                                 3
# ==================================================================
def format_time(t1, t2):
    elapsed_time = t2 - t1
    if elapsed_time < 60:
        return f"{elapsed_time:.2f} seconds"
    elif elapsed_time < 3600:
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        return f"{minutes:.0f} minutes {seconds:.2f} seconds"
    elif elapsed_time < 86400:
        hours = elapsed_time // 3600
        remainder = elapsed_time % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        return f"{hours:.0f} hours {minutes:.0f} minutes {seconds:.2f} seconds"
    else:
        days = elapsed_time // 86400
        remainder = elapsed_time % 86400
        hours = remainder // 3600
        remainder = remainder % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        return f"{days:.0f} days {hours:.0f} hours {minutes:.0f} minutes {seconds:.2f} seconds"


# ==================================================================
#                                 2
# ==================================================================def get_cuda_cores():
    device = torch.cuda.current_device()
    compute_capability = torch.cuda.get_device_capability(device)
    cores_per_sm = {2: 32, 3: 192, 5: 128, 6: 64, 7: 64, 8: 64}  # cores per streaming multiprocessor
    sm_count = torch.cuda.get_device_properties(device).multi_processor_count
    cores = sm_count * cores_per_sm[compute_capability[0]]
    return cores


# ==================================================================
#                                 1
# ==================================================================
from typing import Any
from argparse import Namespace
import typing
class DotDict(Namespace):
    """A simple class that builds upon `argparse.Namespace`
    in order to make chained attributes possible."""

    def __init__(self, temp=False, key=None, parent=None) -> None:
        self._temp = temp
        self._key = key
        self._parent = parent

    def __eq__(self, other):
        if not isinstance(other, DotDict):
            return NotImplemented
        return vars(self) == vars(other)

    def __getattr__(self, __name: str) -> Any:
        if __name not in self.__dict__ and not self._temp:
            self.__dict__[__name] = DotDict(temp=True, key=__name, parent=self)
        else:
            del self._parent.__dict__[self._key]
            raise AttributeError("No attribute '%s'" % __name)
        return self.__dict__[__name]

    def __repr__(self) -> str:
        item_keys = [k for k in self.__dict__ if not k.startswith("_")]

        if len(item_keys) == 0:
            return "DotDict()"
        elif len(item_keys) == 1:
            key = item_keys[0]
            val = self.__dict__[key]
            return "DotDict(%s=%s)" % (key, repr(val))
        else:
            return "DotDict(%s)" % ", ".join(
                "%s=%s" % (key, repr(val)) for key, val in self.__dict__.items()
            )

    @classmethod
    def from_dict(cls, original: typing.Mapping[str, any]) -> "DotDict":
        """Create a DotDict from a (possibly nested) dict `original`.
        Warning: this method should not be used on very deeply nested inputs,
        since it's recursively traversing the nested dictionary values.
        """
        dd = DotDict()
        for key, value in original.items():
            if isinstance(value, typing.Mapping):
                value = cls.from_dict(value)
            setattr(dd, key, value)
        return dd
