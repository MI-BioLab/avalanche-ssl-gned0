import torch
from typing import Optional
import torch.nn.functional as F
from avalanche.models import avalanche_forward
from avalanche.training.templates.strategy_mixin_protocol import (
    SupervisedStrategyProtocol,
    TSGDExperienceType,
    TMBInput,
    TMBOutput,
    SelfSupervisedStrategyProtocol,
)


class SelfSupervisedProblem(
    SelfSupervisedStrategyProtocol[TSGDExperienceType, TMBInput, TMBOutput]
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def mb_x(self):
        """Current mini-batch input."""
        mbatch = self.mbatch
        assert mbatch is not None
        return mbatch[0]

    @property
    def mb_y(self) -> Optional[torch.Tensor]:
        """
        Current mini-batch target (optional).
        Returns None if no labels are found (i.e., the batch only has inputs).
        """
        mbatch = self.mbatch
        assert mbatch is not None
        if len(mbatch) > 1:
            return mbatch[1]
        return None

    @property
    def mb_task_id(self):
        """Current mini-batch task labels."""
        mbatch = self.mbatch
        assert mbatch is not None
        assert len(mbatch) >= 2, "Task label not found."  # no label
        return mbatch[-1]

    def criterion(self):
        """Loss function for self-supervised problems. If labels are present and the classifier
        was instantiated, the online classification loss is computed and added to the total loss."""
        ssl_loss = self._criterion(self.mb_output)
        y = self.mb_y
        if y is not None and "logits" in self.mb_output:
            cls_loss = F.cross_entropy(self.mb_output["logits"], y)
            return ssl_loss + cls_loss
        else:
            return ssl_loss

    def forward(self):
        """Compute the model's output given the current mini-batch."""
        # use task-aware forward only for task-aware benchmarks
        if hasattr(self.experience, "task_labels"):
            return avalanche_forward(self.model, self.mb_x, self.mb_task_id)
        else:
            print("Calling forward step in model")
            return self.model(self.mb_x)

    def _unpack_minibatch(self):
        mbatch = self.mbatch
        assert mbatch is not None

        if isinstance(mbatch, tuple):
            mbatch = list(mbatch)
            self.mbatch = mbatch

        for i in range(len(mbatch)):
            mbatch[i] = mbatch[i].to(self.device, non_blocking=True)  # type: ignore


__all__ = ["SelfSupervisedProblem"]
