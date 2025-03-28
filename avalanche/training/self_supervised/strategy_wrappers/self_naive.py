from typing import Optional, Union, List, Callable

import torch
from torch.nn import Module
from torch.optim import Optimizer

from avalanche.core import SupervisedPlugin
from avalanche.training.plugins import EvaluationPlugin
from avalanche.training.plugins.evaluation import default_evaluator
from avalanche.training.templates.common_templates import SelfSupervisedTemplate
from avalanche.training.templates.strategy_mixin_protocol import CriterionType


class SelfNaive(SelfSupervisedTemplate):
    """Naive self-supervised fine-tuning.

        The simplest (and least effective) Continual Learning strategy. Naive just
        incrementally fine tunes a single model without employing any method
        to contrast the catastrophic forgetting of previous knowledge.
        This strategy does not use task identities.

        Naive is easy to set up and its results are commonly used to show the worst
        performing baseline.
        """

    def __init__(
            self,
            *,
            model: Module,
            optimizer: Optimizer,
            criterion: CriterionType,
            train_mb_size: int = 1,
            train_epochs: int = 1,
            eval_mb_size: Optional[int] = None,
            device: Union[str, torch.device] = "cpu",
            plugins: Optional[List[SupervisedPlugin]] = None,
            evaluator: Union[
                EvaluationPlugin, Callable[[], EvaluationPlugin]
            ] = default_evaluator,
            eval_every=-1,
            **base_kwargs
    ):
        """
        Creates an instance of the Naive strategy.

        :param model: The model.
        :param optimizer: The optimizer to use.
        :param criterion: The loss criterion to use.
        :param train_mb_size: The train minibatch size. Defaults to 1.
        :param train_epochs: The number of training epochs. Defaults to 1.
        :param eval_mb_size: The eval minibatch size. Defaults to 1.
        :param device: The device to use. Defaults to None (cpu).
        :param plugins: Plugins to be added. Defaults to None.
        :param evaluator: (optional) instance of EvaluationPlugin for logging
            and metric computations.
        :param eval_every: the frequency of the calls to `eval` inside the
            training loop. -1 disables the evaluation. 0 means `eval` is called
            only at the end of the learning experience. Values >0 mean that
            `eval` is called every `eval_every` epochs and at the end of the
            learning experience.
        :param base_kwargs: any additional
            :class:`~avalanche.training.BaseTemplate` constructor arguments.
        """

        super().__init__(
            model=model,
            optimizer=optimizer,
            criterion=criterion,
            train_mb_size=train_mb_size,
            train_epochs=train_epochs,
            eval_mb_size=eval_mb_size,
            device=device,
            plugins=plugins,
            evaluator=evaluator,
            eval_every=eval_every,
            **base_kwargs
        )

        self.supervision_type = "self_supervised"