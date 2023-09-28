# Human Feedback is not Gold Standard

Tom Hosking, Phil Blunsom, Max Bartolo

## Description

Human feedback has become the de facto standard for evaluating the performance of Large Language Models, and is increasingly being used as a training objective. However, it is not clear which properties of a generated output this single `preference' score captures. We hypothesise that preference scores are subjective and open to undesirable biases. We critically analyse the use of human feedback for both training and evaluation, to verify whether it fully captures a range of crucial error criteria. We find that while preference scores have fairly good coverage, they under-represent important aspects like factuality. We further hypothesise that both preference scores and error annotation may be affected by confounders, and leverage instruction-tuned models to generate outputs that vary along two possible confounding dimensions: assertiveness and complexity. We find that the assertiveness of an output skews the perceived rate of factuality errors, indicating that human annotations are not a fully reliable evaluation metric or training objective. Finally, we offer preliminary evidence that using human feedback as a training objective disproportionately increases the assertiveness of model outputs. We encourage future work to carefully consider whether preference scores are well aligned with the desired objective.

## Repo Overview

`./interface` contains our modified version of Potato and the configs used for annotation.

`./notebooks` contains the notebooks used to sample from the models, filter the datasets, and run the analysis:
`DataPreparation.ipynb` for data preprocessing
`AnalysisPart1.ipynb` for analysis and plot generation for the first set of experiments
`AnalysisPart2.ipynb` for analysis and plot generation for the second set of experiments

`./results` contains the annotated datasets.


## Datasets

For Part 1, the continuations from `output_merged_{system}.jsonl` were used to generate annotation batches.

The unaggregated ratings are available in the following files:

```sh
./results/batch_v1/prolific_results/unbiased_full.parquet
./results/batch_v1/prolific_results/granular_full.parquet
```

The aggregrated ratings with distractors removed are in `./results/batch_v1/prolific_results/combined_filtered.parquet`

Part 1 data also contains subjective scores, which were unused:
Detail, Clarity, Creativity, Usefuless, Style and Confidence

For Part 2, the continuations in `augmented_v2_{system}.jsonl` + `augmented_v2_part2_{system}.jsonl` were used, and combined into `output_augmented_merged.jsonl`, which was used to generate the annotation batches.

The unaggregated and aggregated+filtered annotations are in `./results/batch_controlled/prolific_results/`.

The `prolific_*` files are the batches used as input to Potato. The `prolific_results/annotated_instances_*` files are the raw output from Potato.

## API keys for inference

For generating completions, API keys should be available as environment variables, eg:

```sh
HF_HUB_KEY=hf_????
COHERE_API_KEY=???
```

## Annotation interface

The relevant interface configs are:
For Part 1:
`granular-eval-detailed` for errors
`granular-eval-unbiased` for unbiased quality scores

Part 2:
`confound-errors` for errors
`confound-grouping` for assertiveness/complexity ratings
`confound-unbiased` for unbiased quality scores
`granular-eval-detailed-verification` for expert annotations

Start Potato with a command like `python potato/potato/flask_server.py start confound-grouping/confound-grouping.yaml -p 15000`

## Citation

TBC